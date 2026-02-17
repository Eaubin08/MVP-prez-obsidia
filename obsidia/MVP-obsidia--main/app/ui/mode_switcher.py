"""Mode switcher component for Guidé ↔ Expert navigation."""
import streamlit as st

def render_mode_switcher():
    """
    Render a prominent mode switcher in the sidebar.
    Allows users to switch between Guided and Expert modes.
    """
    current_mode = st.session_state.get("app_mode", "expert")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔄 Mode de Travail")
    
    # Display current mode with icon
    if current_mode == "guided":
        st.sidebar.info("📍 **Mode actuel** : 🎓 Guidé")
        switch_label = "⚡ Passer en Mode Expert"
        switch_help = "Accès direct à tous les niveaux OS0-OS6"
    else:
        st.sidebar.success("📍 **Mode actuel** : ⚡ Expert")
        switch_label = "🎓 Passer en Mode Guidé"
        switch_help = "Workflow structuré en 5 étapes"
    
    # Switch button
    if st.sidebar.button(switch_label, help=switch_help, use_container_width=True, type="secondary"):
        # Toggle mode
        new_mode = "expert" if current_mode == "guided" else "guided"
        st.session_state["app_mode"] = new_mode
        
        # Reset guided step if switching to guided
        if new_mode == "guided":
            st.session_state["guided_step"] = 1
        
        st.rerun()
    
    st.sidebar.markdown("---")

def render_quick_mode_info():
    """
    Render quick info about current mode.
    """
    current_mode = st.session_state.get("app_mode", "expert")
    
    if current_mode == "guided":
        st.sidebar.caption("🎓 **Mode Guidé** : Workflow structuré en 5 étapes avec validation automatique")
    else:
        st.sidebar.caption("⚡ **Mode Expert** : Navigation libre dans l'architecture OS0-OS6")
