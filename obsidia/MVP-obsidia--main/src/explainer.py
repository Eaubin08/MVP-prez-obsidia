"""Module d'explications en algèbre humaine temps réel."""
from typing import Dict, Any

def explain_features_realtime(features: Dict[str, Any]) -> str:
    """Génère une explication narrative des features."""
    vol = features.get("volatility", 0.5)
    coh = features.get("coherence", 0.5)
    friction = features.get("friction", 0.5)
    regime = features.get("regime", "unknown")
    
    # Symboles algébriques
    vol_symbol = "V↑↑" if vol > 0.4 else "V↑" if vol > 0.2 else "V→"
    coh_symbol = "C↑" if coh > 0.6 else "C→" if coh > 0.3 else "C↓↓"
    friction_symbol = "F↑" if friction > 0.4 else "F→"
    
    explanation = f"""
**Market State Analysis (Human Algebra)**

📊 **Regime**: {regime.upper()}

🔍 **Volatility** ({vol_symbol}): {vol:.2f}
- The market is {'very unstable' if vol > 0.4 else 'moderately volatile' if vol > 0.2 else 'stable'}.
- {'⚠️ High risk of sudden price swings' if vol > 0.3 else '✅ Predictable price movements'}.

🧭 **Coherence** ({coh_symbol}): {coh:.2f}
- Market direction is {'clear and consistent' if coh > 0.6 else 'mixed with noise' if coh > 0.3 else 'chaotic and unreliable'}.
- {'✅ Safe to act' if coh > 0.6 else '⚠️ Caution required' if coh > 0.3 else '❌ High risk of false signals'}.

⚙️ **Friction** ({friction_symbol}): {friction:.2f}
- Transaction costs and slippage are {'high' if friction > 0.4 else 'moderate' if friction > 0.2 else 'low'}.

**🎯 Recommendation**:
"""
    
    # Logique de recommandation
    if vol > 0.35 or coh < 0.3:
        explanation += "❌ **BLOCK** - Market conditions are too risky. Wait for stabilization."
    elif vol > 0.25 or coh < 0.5:
        explanation += "⏸️ **HOLD** - Conditions are uncertain. X-108 timer should be activated."
    else:
        explanation += "✅ **ALLOW** - Conditions are favorable. Proceed to simulation."
    
    return explanation

def explain_simulation_realtime(sim_result: Dict[str, Any]) -> str:
    """Génère une explication narrative de la simulation."""
    verdict = sim_result.get("verdict", "UNKNOWN")
    p_ruin = sim_result.get("p_ruin", 0.0)
    p_dd = sim_result.get("p_dd", 0.0)
    cvar = sim_result.get("cvar_95", 0.0)
    
    explanation = f"""
**Simulation Analysis (Monte Carlo Projection)**

🎲 **Verdict**: {verdict}

📉 **Risk Metrics**:
- **P(Ruin)**: {p_ruin:.2%} - Probability of catastrophic loss
- **P(Drawdown)**: {p_dd:.2%} - Probability of significant drawdown
- **CVaR 95%**: {cvar:.4f} - Worst-case expected loss (95% confidence)

**📖 Human Translation**:
"""
    
    if verdict == "DESTRUCTIVE":
        explanation += f"""
❌ **DESTRUCTIVE Scenario Detected**

The simulation projects that this intent has a **{p_ruin:.1%} chance of ruin** and a **{p_dd:.1%} chance of severe drawdown**.

In human terms: **"This is like betting your house on a coin flip."**

The system will **BLOCK** this intent to prevent catastrophic loss.
"""
    elif verdict == "RISKY":
        explanation += f"""
⚠️ **RISKY Scenario Detected**

The simulation shows elevated risk levels. While not catastrophic, the potential for loss is significant.

In human terms: **"This is like driving in heavy rain - possible, but dangerous."**

The system will likely **HOLD** this intent for further review (X-108).
"""
    else:
        explanation += f"""
✅ **SAFE Scenario**

The simulation projects acceptable risk levels. The intent is within safe boundaries.

In human terms: **"This is like walking on a clear sidewalk - safe to proceed."**

The system will **ALLOW** this intent to pass to governance gates.
"""
    
    return explanation

def explain_gates_realtime(gates_result: Dict[str, Any]) -> str:
    """Génère une explication narrative des gates."""
    decision = gates_result.get("decision", "UNKNOWN")
    reason = gates_result.get("reason", "")
    
    gate1 = gates_result.get("gate1", {})
    gate2 = gates_result.get("gate2", {})
    gate3 = gates_result.get("gate3", {})
    
    explanation = f"""
**Gates Evaluation (Governance Pipeline)**

🚦 **Final Decision**: {decision}
📝 **Reason**: {reason}

**Gate-by-Gate Analysis**:

1️⃣ **Gate 1 - Integrity Check**: {'✅ PASS' if gate1.get('ok') else '❌ FAIL'}
   - Verifies that the intent is well-formed and complete
   - {'All fields are valid' if gate1.get('ok') else 'Missing or invalid fields detected'}

2️⃣ **Gate 2 - X-108 Temporal Lock**: {'✅ PASS' if gate2.get('ok') else '❌ FAIL'}
   - Enforces mandatory delay (τ) for irreversible intents
   - {'Timer elapsed, action is allowed' if gate2.get('ok') else f"Timer active: {gate2.get('reason', 'HOLD required')}"}

3️⃣ **Gate 3 - Risk Killswitch**: {'✅ PASS' if gate3.get('ok') else '❌ FAIL'}
   - Final safety check based on simulation and market state
   - {gate3.get('reason', 'Risk within acceptable limits') if gate3.get('ok') else gate3.get('reason', 'Risk too high')}

**🎯 Human Translation**:
"""
    
    if decision == "BLOCK":
        explanation += f"""
🛑 **BLOCKED**

The intent has been **permanently blocked** because {reason}.

In human terms: **"The system said NO and will not reconsider."**

This is the highest priority decision, protecting against catastrophic outcomes.
"""
    elif decision == "HOLD":
        explanation += f"""
⏸️ **HELD**

The intent is **temporarily held** because {reason}.

In human terms: **"The system said WAIT, not NO."**

After the mandatory delay (X-108), the intent can be re-evaluated.
"""
    else:
        explanation += f"""
✅ **EXECUTE (Paper Intent)**

All gates have **passed**. The intent is cleared for execution.

In human terms: **"The system said YES, proceed safely."**

A paper trade intent (ERC-8004) will be emitted for audit trail.
"""
    
    return explanation

def explain_decision_flow(features: Dict[str, Any], sim_result: Dict[str, Any], 
                         gates_result: Dict[str, Any]) -> str:
    """Génère une explication narrative complète du flux de décision."""
    
    return f"""
# 📖 Complete Decision Flow Explanation

## 🔍 Step 1: Market Observation (OS1)

{explain_features_realtime(features)}

---

## 🎲 Step 2: Risk Projection (OS2)

{explain_simulation_realtime(sim_result)}

---

## 🚦 Step 3: Governance Gates (OS3)

{explain_gates_realtime(gates_result)}

---

## 🎯 Final Outcome

**Decision**: {gates_result.get('decision', 'UNKNOWN')}

**Why this matters**: The system didn't just "decide" - it **explained every step** of its reasoning. This is **transparent AI governance** in action.

From raw market data → risk projection → safety gates → final decision, every step is auditable and explainable.
"""
