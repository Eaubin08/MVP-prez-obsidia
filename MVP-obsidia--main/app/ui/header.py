"""Header component for both Guided and Expert modes."""
import streamlit as st

def render_header_guided():
    """
    Render header for Guided Mode with progress bar.
    """
    col1, col2, col3 = st.columns([2, 6, 2])
    
    with col1:
        st.markdown("### 🏛️ OBSIDIA")
    
    with col2:
        st.markdown("### MODE GUIDÉ")
    
    with col3:
        if st.button("⚡ Mode Expert", use_container_width=True):
            st.session_state["app_mode"] = "expert"
            st.rerun()
    
    st.markdown("---")
    
    # Progress bar
    current_step = st.session_state.get("guided_step", 1)
    steps = ["1.Config", "2.Exploration", "3.Simulation", "4.Gouvernance", "5.Rapport"]
    
    progress_html = '<div style="padding: 10px; background: #f0f2f6; border-radius: 8px; margin-bottom: 20px;">'
    progress_html += '<div style="font-weight: bold; margin-bottom: 8px;">📍 VOTRE PROGRESSION</div>'
    progress_html += '<div style="display: flex; gap: 8px; align-items: center;">'
    
    for i, step in enumerate(steps, 1):
        if i < current_step:
            progress_html += f'<span style="color: green;">✅ {step}</span>'
        elif i == current_step:
            progress_html += f'<span style="color: blue; font-weight: bold;">▶️ {step}</span>'
        else:
            progress_html += f'<span style="color: gray;">{step}</span>'
        
        if i < len(steps):
            progress_html += '<span style="color: gray;">→</span>'
    
    progress_html += '</div></div>'
    
    st.markdown(progress_html, unsafe_allow_html=True)

def render_header_expert():
    """
    Render header for Expert Mode with switch to Guided.
    """
    col1, col2 = st.columns([8, 2])
    
    with col1:
        # Breadcrumb
        current_os = st.session_state.get("os_level", "OS0")
        os_names = {
            "OS0": "Invariants",
            "OS1": "Exploration",
            "OS2": "Simulation",
            "OS3": "Gouvernance",
            "OS4": "Rapports",
            "OS5": "Démo Auto",
            "OS6": "Tests Stress"
        }
        st.markdown(f"### 🏛️ OBSIDIA › {current_os} — {os_names.get(current_os, '')}")
    
    with col2:
        if st.button("🎓 Mode Guidé", use_container_width=True):
            st.session_state["app_mode"] = "guided"
            st.session_state["guided_step"] = 1
            st.rerun()
    
    st.markdown("---")
