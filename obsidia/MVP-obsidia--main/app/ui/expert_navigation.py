"""Navigation sidebar for Expert Mode with OS0-OS6."""
import streamlit as st

def render_expert_sidebar():
    """
    Render the fixed sidebar navigation for Expert Mode.
    Returns the selected OS level.
    """
    with st.sidebar:
        st.markdown("### 📍 NAVIGATION OS")
        
        # OS Level selection with radio buttons styled as list
        os_options = {
            "OS0": "OS0 — Invariants (Lois)",
            "OS1": "OS1 — Exploration (Découv.)",
            "OS2": "OS2 — Simulation (Projet.)",
            "OS3": "OS3 — Gouvernance (Décis.)",
            "OS4": "OS4 — Rapports (Audit)",
            "OS5": "OS5 — Démo Auto (Scénarios)",
            "OS6": "OS6 — Tests Stress (Avancé)"
        }
        
        # Get current selection from session state
        current_os = st.session_state.get("os_level", "OS0")
        
        # Radio buttons for OS selection
        selected_os = st.radio(
            "Navigation",
            options=list(os_options.keys()),
            format_func=lambda x: os_options[x],
            index=list(os_options.keys()).index(current_os),
            label_visibility="collapsed"
        )
        
        # Update session state
        if selected_os != current_os:
            st.session_state["os_level"] = selected_os
            st.rerun()
        
        st.markdown("---")
        
        # Configuration section
        st.markdown("### ⚙️ CONFIGURATION")
        
        # Domain selector
        domain = st.selectbox(
            "🎯 Domaine",
            ["Trading (ERC-8004)", "Medical-AI", "Legal-Contracts", "Auto-Drive", "Factory-Control"],
            help="Sélectionnez le domaine d'application"
        )
        
        # Seed input
        seed = st.number_input(
            "🎲 Seed",
            min_value=0,
            max_value=9999,
            value=st.session_state.get("seed", 42),
            help="Graine aléatoire pour reproductibilité"
        )
        
        # Tau slider
        tau = st.slider(
            "🔒 Délai τ (s)",
            min_value=0.0,
            max_value=30.0,
            value=st.session_state.get("tau", 10.0),
            step=0.5,
            help="Délai de sécurité X-108"
        )
        
        # Update session state
        st.session_state["seed"] = seed
        st.session_state["tau"] = tau
        st.session_state["domain"] = domain.split(" ")[0].lower()
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### 🔗 ACCÈS RAPIDE")
        
        if st.button("⚖️ Lois Fondamentales", use_container_width=True):
            st.session_state["os_level"] = "OS0"
            st.rerun()
        
        if st.button("📊 Dashboard Domaines", use_container_width=True):
            st.session_state["show_domain_analytics"] = True
            st.rerun()
        
        return selected_os
