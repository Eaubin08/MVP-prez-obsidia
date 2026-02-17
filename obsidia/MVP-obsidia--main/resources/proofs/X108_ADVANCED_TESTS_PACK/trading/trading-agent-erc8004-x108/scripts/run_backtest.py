import argparse, json
import numpy as np
from pathlib import Path
from collections import deque

from src.data import load_prices_csv
from src.features.features import extract_features
from src.simulation.sim_lite import sim_lite_bootstrap
from src.score.score import compute_score
from src.gates.gate1_integrity import gate1_validate_intent
from src.gates.gate2_x108_temporal import gate2_x108_temporal
from src.gates.gate3_risk_killswitch import gate3_risk_kill
from src.roi_policy.roi import roi_init, roi_decide
from src.execution.erc8004 import build_trade_intent
from src.execution.dry_executor import execute_dry
from src.utils import append_jsonl, now_iso

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--asset", default="BTC")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    close, returns = load_prices_csv(args.csv)

    logs_dir = Path("logs")
    decision_log = logs_dir / "decision_log.jsonl"
    sim_log = logs_dir / "simulation_log.jsonl"
    roi_log = logs_dir / "roi_log.jsonl"
    orders_log = logs_dir / "orders_log.jsonl"

    # state
    state = {
        "last_invest_ts": 0.0,
        "equity_curve": [1.0],
        "consecutive_losses": 0,
        "cooldown_remaining": 0
    }
    roi = roi_init(cfg["roi"])
    scores_window = deque(maxlen=100)

    equity = 1.0
    position = 0.0  # simple scalar position
    entry_price = None

    # iterate over time steps
    for t in range(60, len(returns)):
        # cooldown decrement
        if state["cooldown_remaining"] > 0:
            state["cooldown_remaining"] -= 1

        r_hist = returns[:t]
        feats = extract_features(r_hist)
        projected = sim_lite_bootstrap(
            r_hist,
            n_sims=cfg["simulation"]["n_sims"],
            horizon=cfg["simulation"]["horizon"],
            bootstrap_window=cfg["simulation"]["bootstrap_window"],
            dd_threshold=cfg["score"]["dd_threshold"]
        )

        append_jsonl(sim_log, {
            "ts": now_iso(),
            "step": t,
            "features": feats,
            "projected": projected
        })

        # build candidate intent (BUY if coherence high, SELL if low; minimal)
        side = "BUY" if feats["coherence"] >= cfg["coherence_threshold"] else "SELL"
        amount = max(0.0, roi.risk_level)  # risk_level is position sizing proxy
        intent_candidate = {
            "asset": args.asset,
            "side": side,
            "amount": float(amount),
            "timestamp": float(t),
            "coherence": float(feats["coherence"]),
        }

        # Gate 1
        ok1, r1 = gate1_validate_intent(intent_candidate)
        if not ok1:
            append_jsonl(decision_log, {"ts": now_iso(), "step": t, "gate": 1, "pass": False, "reason": r1, "intent": intent_candidate})
            continue

        # Score
        x_bonus = 1.0 if feats["coherence"] >= cfg["coherence_threshold"] else 0.0
        S = compute_score(projected, feats, x_bonus, cfg["score"]["weights"], cfg["score"]["dd_threshold"])
        scores_window.append(S)
        mean_score = float(np.mean(scores_window)) if scores_window else 0.0

        # Gate 2 (X-108 long horizon check)
        ok2, r2 = gate2_x108_temporal(state, float(t), cfg["hold_seconds"], float(feats["coherence"]), cfg["coherence_threshold"])
        if not ok2:
            append_jsonl(decision_log, {"ts": now_iso(), "step": t, "gate": 2, "pass": False, "reason": r2, "score": S, "intent": intent_candidate})
            continue

        # Gate 3 (risk/kill)
        ok3, r3 = gate3_risk_kill(state, r_hist, cfg["gate3"])
        if not ok3:
            # Roi decides safe exit on kill triggers
            roi_action = roi_decide(roi, t, mean_score, cfg["roi"], gate3_reason=r3)
            append_jsonl(roi_log, {"ts": now_iso(), "step": t, "action": roi_action, "roi": roi.__dict__, "reason": r3})
            append_jsonl(decision_log, {"ts": now_iso(), "step": t, "gate": 3, "pass": False, "reason": r3, "score": S})
            continue

        # Roi sovereign decisions (rare)
        roi_action = roi_decide(roi, t, mean_score, cfg["roi"])
        if roi_action != "NOOP":
            append_jsonl(roi_log, {"ts": now_iso(), "step": t, "action": roi_action, "roi": roi.__dict__, "mean_score": mean_score})

        if roi.safe_mode:
            append_jsonl(decision_log, {"ts": now_iso(), "step": t, "pass": False, "reason": "roi_safe_mode", "score": S})
            continue

        # Build ERC-8004 TradeIntent + execute (dry)
        intent = build_trade_intent(
            asset=intent_candidate["asset"],
            side=intent_candidate["side"],
            amount=intent_candidate["amount"],
            timestamp=float(t),
            metadata={
                "score": S,
                "features": feats,
                "projected": projected,
                "roi": roi.__dict__,
                "regime": feats["regime"]
            }
        )

        ok, info = execute_dry(intent)
        append_jsonl(orders_log, {"ts": now_iso(), "step": t, "ok": ok, "info": info, "intent": intent})

        # Update investment timestamp for X-108 gate2 (investment-level action)
        state["last_invest_ts"] = float(t)

        # Update toy PnL / equity
        # (position sizing proxy; purely for demo curves)
        step_ret = returns[t-1]
        signed = (1 if intent_candidate["side"] == "BUY" else -1) * intent_candidate["amount"]
        pnl = signed * step_ret
        equity *= (1.0 + pnl)
        state["equity_curve"].append(float(equity))

        if pnl < 0:
            state["consecutive_losses"] += 1
        else:
            state["consecutive_losses"] = 0

        append_jsonl(decision_log, {
            "ts": now_iso(),
            "step": t,
            "pass": True,
            "score": S,
            "roi_action": roi_action,
            "intent_candidate": intent_candidate,
            "equity": equity
        })

    print("DONE. logs written to ./logs")

if __name__ == "__main__":
    main()
