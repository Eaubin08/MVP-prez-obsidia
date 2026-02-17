"""OS2 — Simulation / Projection (zéro exécution)."""
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

from src.core_pipeline import run_simulation
from src.utils import read_artifact
from src.visualization import plot_simulation_distribution
from src.state_manager import get_unique_key, mark_simulation_done, is_features_valid

def render(base_dir: Path, config: dict):
    """Affiche l'interface de simulation."""
    st.subheader("OS2 — Simulation / Projection (SIM-LITE)")
    st.caption("⚠️ Runs projection. No execution here.")
    
    # Vérifier que les features existent ET sont valides
    if not is_features_valid():
        st.error("🔒 **Étape 2 bloquée** : Calculez d'abord les features en Étape 1 (Exploration)")
        st.info("👉 Retournez à l'étape 1 pour calculer les features avec la configuration actuelle.")
        return
    
    if "features" not in st.session_state or "returns" not in st.session_state:
        st.warning("⚠️ No features found. Please go to OS1 and compute features first.")
        return
    
    features = st.session_state["features"]
    returns = st.session_state["returns"]
    
    st.markdown("#### ⚙️ Simulation Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n_sims = st.slider("N scenarios", 50, 500, 200, 50)
    
    with col2:
        horizon = st.slider("Horizon steps", 5, 50, 20, 5)
    
    if st.button("🚀 Run SIM-LITE", type="primary"):
        with st.spinner("Running Monte Carlo simulation..."):
            sim_result = run_simulation(returns, base_dir, n_sims=n_sims, horizon=horizon)
            
            st.success("✅ Simulation completed!")
            
            # Graphique de distribution avec key unique
            fig_dist = plot_simulation_distribution(sim_result)
            dist_key = get_unique_key("os2_dist_chart")
            st.plotly_chart(fig_dist, use_container_width=True, key=dist_key)
            
            # Afficher les résultats
            st.markdown("#### 📊 Simulation Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Mean Return (μ)", f"{sim_result['mu']:.4f}")
                st.metric("Std Dev (σ)", f"{sim_result['sigma']:.4f}")
            
            with col2:
                st.metric("P(DD > threshold)", f"{sim_result['p_dd']:.2%}")
                st.metric("P(Ruin)", f"{sim_result['p_ruin']:.2%}")
            
            with col3:
                st.metric("CVaR 95%", f"{sim_result['cvar_95']:.4f}")
                verdict = sim_result.get("verdict", "UNKNOWN")
                
                if verdict == "OK":
                    st.success(f"Verdict: **{verdict}**")
                elif verdict == "UNCERTAIN":
                    st.warning(f"Verdict: **{verdict}**")
                else:
                    st.error(f"Verdict: **{verdict}**")
            
            # JSON complet
            st.markdown("---")
            st.markdown("#### 📋 Full Simulation Data")
            st.json(sim_result)
            
            # Sauvegarder dans session state
            st.session_state["simulation"] = sim_result
            
            # Marquer comme terminé
            mark_simulation_done()
    
    # Afficher la simulation existante si disponible
    if "simulation" in st.session_state:
        st.markdown("---")
        st.markdown("#### 📋 Current Simulation (from session)")
        sim = st.session_state["simulation"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("μ", f"{sim['mu']:.4f}")
        with col2:
            st.metric("P(Ruin)", f"{sim['p_ruin']:.2%}")
        with col3:
            verdict = sim.get("verdict", "UNKNOWN")
            if verdict == "OK":
                st.success(f"**{verdict}**")
            elif verdict == "UNCERTAIN":
                st.warning(f"**{verdict}**")
            else:
                st.error(f"**{verdict}**")
