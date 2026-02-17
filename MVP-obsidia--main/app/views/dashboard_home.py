"""Professional operational dashboard as home page."""
import streamlit as st
import pandas as pd
from datetime import datetime

def render():
    """Render the operational dashboard."""
    
    # HEADER COMPACT
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.title("Dashboard Obsidia")
    with col2:
        st.metric("Domaine", st.session_state.get("domain", "Trading").capitalize())
    with col3:
        st.metric("Seed", st.session_state.get("seed", 42))
    with col4:
        st.metric("Délai τ", f"{st.session_state.get('tau', 10.0)}s")
    
    st.markdown("---")
    
    # DERNIÈRES SIMULATIONS
    st.subheader("📊 Dernières Simulations")
    
    # Tableau récapitulatif (données fictives pour démo)
    data = {
        "Run ID": ["#20c88a56", "#1a2b3c4d", "#9f8e7d6c"],
        "Date": [
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            "2026-02-15 14:32",
            "2026-02-14 09:15"
        ],
        "μ (Return)": [0.5706, 0.4821, 0.6234],
        "P(Ruin)": ["0.00%", "2.15%", "0.00%"],
        "Decision": ["✅ EXECUTE", "⚠️ HOLD", "✅ EXECUTE"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ACTIONS RAPIDES
    st.subheader("⚡ Actions Rapides")
    col_a, col_b, col_c, col_d = st.columns(4)
    
    with col_a:
        if st.button("🔍 Nouvelle Analyse", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "Analyse"
            st.rerun()
    
    with col_b:
        if st.button("📊 Lancer Simulation", use_container_width=True):
            st.session_state["current_page"] = "Simulation"
            st.rerun()
    
    with col_c:
        if st.button("📄 Voir Rapports", use_container_width=True):
            st.session_state["current_page"] = "Rapports"
            st.rerun()
    
    with col_d:
        if st.button("🧪 Tests Stress", use_container_width=True):
            st.session_state["current_page"] = "Stress Tests"
            st.rerun()
    
    st.markdown("---")
    
    # STATUT SYSTÈME
    st.subheader("⚖️ Statut Système")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Lois Fondamentales**")
        st.success("✅ BLOCK > HOLD > ALLOW")
        st.success("✅ X-108 Temporal Lock")
        st.success("✅ Séparation des rôles")
    
    with col2:
        st.markdown("**Gates Status**")
        st.success("✅ Gate 1: Integrity")
        st.success("✅ Gate 2: X-108")
        st.success("✅ Gate 3: Risk Killswitch")
    
    with col3:
        st.markdown("**Configuration**")
        st.info(f"🎯 Domaine: {st.session_state.get('domain', 'Trading').capitalize()}")
        st.info(f"🎲 Seed: {st.session_state.get('seed', 42)}")
        st.info(f"🔒 Délai τ: {st.session_state.get('tau', 10.0)}s")
