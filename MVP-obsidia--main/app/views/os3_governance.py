"""OS3 — Governance (filtrage de l'irréversible)."""
import streamlit as st
import time
from pathlib import Path

from src.core_pipeline import evaluate_gates, emit_erc8004_intent
from src.score.human_algebra import gates_explainer
from src.utils import zip_last_run
from src.visualization import plot_gates_timeline
from src.state_manager import get_unique_key, mark_governance_tested, is_simulation_valid

def render(base_dir: Path, config: dict):
    """Affiche l'interface de gouvernance."""
    st.subheader("OS3 — Governance (Gates + X-108 + Roi)")
    st.caption("⚠️ Only here an intent can be emitted (paper).")
    
    # Vérifier les prérequis
    if not is_simulation_valid():
        st.error("🔒 **Étape 3 bloquée** : Effectuez d'abord la simulation en Étape 2")
        st.info("👉 Retournez à l'étape 2 pour exécuter la simulation Monte Carlo avec la configuration actuelle.")
        return
    
    if "features" not in st.session_state or "simulation" not in st.session_state:
        st.warning("⚠️ Missing artifacts. Please run OS1 then OS2 first.")
        return
    
    features = st.session_state["features"]
    sim_result = st.session_state["simulation"]
    returns = st.session_state.get("returns")
    
    # Intent Form
    st.markdown("#### 📝 Intent (Paper)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        asset = st.selectbox("Asset", ["BTC", "ETH", "SPY"], index=0)
        side = st.selectbox("Side", ["BUY", "SELL"], index=0)
    
    with col2:
        amount = st.number_input("Amount", min_value=0.0, value=100.0, step=10.0)
        irreversible = st.checkbox("Irreversible", value=True)
    
    with col3:
        st.markdown("##### X-108 Timer")
        
        if "hold_started_ts" not in st.session_state:
            st.session_state.hold_started_ts = None
        
        if st.button("⏱️ Start HOLD Timer"):
            st.session_state.hold_started_ts = time.time()
            st.success("✅ HOLD timer started!")
        
        if st.session_state.hold_started_ts:
            elapsed = time.time() - st.session_state.hold_started_ts
            st.write(f"Elapsed: **{elapsed:.1f}s**")
            
            tau = config.get("tau", 10.0)
            if elapsed < tau:
                st.warning(f"⏳ HOLD active (τ={tau}s)")
            else:
                st.success(f"✅ HOLD released (>{tau}s)")
    
    # Créer l'intent
    intent = {
        "asset": asset,
        "side": side,
        "amount": float(amount),
        "timestamp": time.time(),
        "coherence": features.get("coherence", 0.0),
        "irreversible": irreversible
    }
    
    st.markdown("---")
    st.markdown("#### 🚦 Gates Evaluation")
    
    if st.button("🔍 Evaluate Gates", type="primary"):
        with st.spinner("Evaluating gates..."):
            # State pour gate3
            state = {
                "last_invest_ts": st.session_state.hold_started_ts or 0.0,
                "equity_curve": [1.0],  # Simplified
                "consecutive_losses": 0,
                "cooldown_remaining": 0
            }
            
            gates_result = evaluate_gates(
                intent=intent,
                features=features,
                sim_result=sim_result,
                hold_started_ts=st.session_state.hold_started_ts or 0.0,
                tau_seconds=config.get("tau", 10.0),
                state=state,
                returns=returns,
                base_dir=base_dir
            )
            
            st.session_state["gates_result"] = gates_result
            
            # Marquer comme testé
            mark_governance_tested()
            
            st.success("✅ Gates evaluated!")
    
    # Afficher les résultats des gates
    if "gates_result" in st.session_state:
        gates = st.session_state["gates_result"]
        
        # Timeline visuelle avec key unique
        fig_timeline = plot_gates_timeline(gates)
        timeline_key = get_unique_key("os3_timeline_chart")
        st.plotly_chart(fig_timeline, use_container_width=True, key=timeline_key)
        
        st.markdown("##### Gates Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            g1 = gates["gate1"]
            if g1["ok"]:
                st.success(f"✅ Gate1: {g1['reason']}")
            else:
                st.error(f"❌ Gate1: {g1['reason']}")
        
        with col2:
            g2 = gates["gate2"]
            if g2["ok"]:
                st.success(f"✅ Gate2: {g2['reason']}")
            else:
                st.warning(f"⏳ Gate2: {g2['reason']}")
        
        with col3:
            g3 = gates["gate3"]
            if g3["ok"]:
                st.success(f"✅ Gate3: {g3['reason']}")
            else:
                st.error(f"❌ Gate3: {g3['reason']}")
        
        # Décision finale
        st.markdown("---")
        st.markdown("##### Final Decision")
        
        decision = gates["decision"]
        
        if decision == "EXECUTE":
            st.success(f"🟢 **{decision}**: Action admissible")
        elif decision == "HOLD":
            st.warning(f"🟡 **{decision}**: Waiting for X-108")
        else:
            st.error(f"🔴 **{decision}**: Action blocked")
        
        # Explication
        st.code(gates_explainer(gates), language="text")
        
        # Émettre l'intent
        st.markdown("---")
        st.markdown("#### 📤 Emit TradeIntent (ERC-8004 Paper)")
        
        if st.button("📨 Emit Intent", type="primary"):
            result = emit_erc8004_intent(intent, gates, base_dir)
            
            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                st.success("✅ Intent emitted (paper)!")
                st.json(result)
                
                # Créer le ZIP
                zpath = zip_last_run(base_dir)
                st.info(f"📦 Artifacts zipped: `{zpath}`")
