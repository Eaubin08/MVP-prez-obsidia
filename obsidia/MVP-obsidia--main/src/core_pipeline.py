"""Pipeline core qui orchestre features → simulation → gates → roi → intent."""
import time
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple

from src.features.features import extract_features
from src.simulation.sim_lite import sim_lite_bootstrap
from src.gates.gate1_integrity import gate1_validate_intent
from src.gates.gate2_x108_temporal import gate2_x108_temporal
from src.gates.gate3_risk_killswitch import gate3_risk_kill
from src.roi_policy.roi import roi_decide, RoiState
from src.execution.erc8004 import build_trade_intent
from src.utils import save_artifact, log_jsonl

def run_observation(returns: np.ndarray, base_dir: Path) -> Dict[str, Any]:
    """OS1: Observation - Calcul des features."""
    features = extract_features(returns)
    
    # Sauvegarder
    save_artifact(base_dir, "features.json", {"features": features})
    log_jsonl(base_dir, "decision_log", {
        "stage": "OS1",
        "event": "features_computed",
        "features": features
    })
    
    return features

def run_simulation(returns: np.ndarray, base_dir: Path, n_sims: int = 200, horizon: int = 20) -> Dict[str, Any]:
    """OS2: Simulation - Projection Monte Carlo."""
    sim_result = sim_lite_bootstrap(returns, n_sims=n_sims, horizon=horizon)
    
    # Verdict
    if sim_result["p_ruin"] > 0.10 or sim_result["p_dd"] > 0.25:
        sim_result["verdict"] = "DESTRUCTIVE"
    elif sim_result["p_ruin"] > 0.05 or sim_result["p_dd"] > 0.15:
        sim_result["verdict"] = "UNCERTAIN"
    else:
        sim_result["verdict"] = "OK"
    
    # Sauvegarder
    save_artifact(base_dir, "simulation.json", {"simulation": sim_result})
    log_jsonl(base_dir, "simulation_log", {
        "stage": "OS2",
        "event": "simulation_completed",
        "verdict": sim_result["verdict"],
        "p_ruin": sim_result["p_ruin"],
        "p_dd": sim_result["p_dd"]
    })
    
    return sim_result

def evaluate_gates(
    intent: Dict[str, Any],
    features: Dict[str, Any],
    sim_result: Dict[str, Any],
    hold_started_ts: float,
    tau_seconds: float,
    state: Dict[str, Any],
    returns: np.ndarray,
    base_dir: Path
) -> Dict[str, Any]:
    """OS3: Governance - Évaluation des gates."""
    now_ts = time.time()
    
    # Gate 1: Integrity
    g1_ok, g1_reason = gate1_validate_intent(intent)
    
    # Gate 2: X-108 Temporal
    g2_ok, g2_reason = gate2_x108_temporal(
        state=state,
        now_ts=now_ts,
        hold_seconds=tau_seconds,
        coherence=features.get("coherence", 0.0),
        coherence_threshold=0.3
    )
    
    # Gate 3: Risk Killswitch
    cfg_gate3 = {
        "max_drawdown": 0.15,
        "max_volatility": 0.50,
        "max_consecutive_losses": 5,
        "cooldown_steps": 10
    }
    g3_ok, g3_reason = gate3_risk_kill(state, returns, cfg_gate3)
    
    # Composition: BLOCK > HOLD > ALLOW
    laws = []
    if not g1_ok:
        decision = "BLOCK"
        reason = g1_reason
        laws.append("Gate1: Integrity violation → D ⟂")
    elif not g3_ok:
        decision = "BLOCK"
        reason = g3_reason
        laws.append("Gate3: Risk killswitch → D ⟂")
    elif not g2_ok:
        decision = "HOLD"
        reason = g2_reason
        laws.append(f"X-108: T < τ ({tau_seconds}s) → D ⟂ (HOLD)")
    elif sim_result.get("verdict") == "DESTRUCTIVE":
        decision = "BLOCK"
        reason = "simulation_destructive"
        laws.append("Simulation: destructive projection → D ⟂")
    else:
        decision = "EXECUTE"
        reason = "pass"
        laws.append("All gates PASS → action admissible")
    
    gates_result = {
        "gate1": {"ok": g1_ok, "reason": g1_reason},
        "gate2": {"ok": g2_ok, "reason": g2_reason},
        "gate3": {"ok": g3_ok, "reason": g3_reason},
        "decision": decision,
        "reason": reason,
        "laws": laws
    }
    
    # Sauvegarder
    save_artifact(base_dir, "gates.json", {
        "intent": intent,
        "gates": gates_result
    })
    log_jsonl(base_dir, "roi_log", {
        "stage": "OS3",
        "event": "gates_evaluated",
        "decision": decision,
        "reason": reason
    })
    
    return gates_result

def emit_erc8004_intent(
    intent: Dict[str, Any],
    gates_result: Dict[str, Any],
    base_dir: Path
) -> Dict[str, Any]:
    """Émet un TradeIntent ERC-8004 (paper)."""
    if gates_result["decision"] != "EXECUTE":
        return {"error": f"Intent not emitted. Decision = {gates_result['decision']}"}
    
    erc8004_intent = build_trade_intent(
        asset=intent["asset"],
        side=intent["side"],
        amount=intent["amount"],
        timestamp=intent["timestamp"],
        metadata={
            "gates": gates_result,
            "run_ref": "last_run"
        }
    )
    
    # Sauvegarder
    save_artifact(base_dir, "erc8004_intent.json", {
        "erc8004": erc8004_intent
    })
    log_jsonl(base_dir, "intents_log", {
        "stage": "OS3",
        "event": "intent_emitted",
        "asset": intent["asset"],
        "side": intent["side"],
        "amount": intent["amount"]
    })
    
    return erc8004_intent
