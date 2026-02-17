"""Navigation components: header, breadcrumb, stepper."""
import streamlit as st

def render_permanent_header(mode: str = "expert", step: int = None):
    """
    Render permanent header with navigation links.
    
    Args:
        mode: "guided" or "expert"
        step: Current step number (for guided mode)
    """
    if mode == "guided":
        mode_display = f"<b>Mode Guidé</b> | Étape <b>{step}</b>/5"
    else:
        mode_display = "<b>Mode Expert</b>"
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #1e1e1e 0%, #2e2e2e 100%);
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    ">
        <div style="display: flex; align-items: center; gap: 20px;">
            <span style="font-size: 24px;">🏛️</span>
            <span style="color: #7c9fff; font-size: 18px; font-weight: bold;">OBSIDIA</span>
            <span style="color: #9E9E9E;">|</span>
            <span style="color: #fff; font-size: 14px;">{mode_display}</span>
        </div>
        <div style="display: flex; gap: 15px; align-items: center;">
            <a href="?reset=1" style="
                color: #7c9fff;
                text-decoration: none;
                font-size: 14px;
                padding: 6px 12px;
                border-radius: 4px;
                background: rgba(124, 159, 255, 0.1);
                transition: all 0.3s;
            " onmouseover="this.style.background='rgba(124, 159, 255, 0.2)'" 
               onmouseout="this.style.background='rgba(124, 159, 255, 0.1)'">
                🏠 Accueil
            </a>
            <span style="color: #9E9E9E;">|</span>
            <a href="#" style="
                color: #9E9E9E;
                text-decoration: none;
                font-size: 14px;
            ">💡 Aide</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Gérer le reset
    if st.query_params.get("reset") == "1":
        st.session_state["app_mode"] = None
        if "guided_step" in st.session_state:
            del st.session_state["guided_step"]
        st.query_params.clear()
        st.rerun()

def render_breadcrumb(steps: list, current: int):
    """
    Render breadcrumb navigation.
    
    Args:
        steps: List of step names
        current: Current step index (0-based)
    """
    breadcrumb_html = '<div style="margin-bottom: 15px; font-size: 14px; color: #9E9E9E;">'
    breadcrumb_html += '🏠 <a href="?reset=1" style="color: #7c9fff; text-decoration: none;">Accueil</a>'
    
    for i, step in enumerate(steps):
        if i <= current:
            breadcrumb_html += f' > <span style="color: #fff;">{step}</span>'
        else:
            breadcrumb_html += f' > <span style="color: #5E5E5E;">{step}</span>'
    
    breadcrumb_html += '</div>'
    st.markdown(breadcrumb_html, unsafe_allow_html=True)

def render_enhanced_stepper(steps: list, current: int, completed: list = None):
    """
    Render enhanced stepper with icons and status.
    
    Args:
        steps: List of (icon, label) tuples
        current: Current step index (0-based)
        completed: List of completed step indices
    """
    if completed is None:
        completed = []
    
    cols = st.columns(len(steps))
    
    for i, (icon, label) in enumerate(steps):
        with cols[i]:
            if i in completed:
                # Completed
                st.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <div style="
                        width: 50px;
                        height: 50px;
                        margin: 0 auto 8px;
                        border-radius: 50%;
                        background: linear-gradient(135deg, #4CAF50, #45a049);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.4);
                    ">
                        ✓
                    </div>
                    <div style="color: #4CAF50; font-weight: bold; font-size: 12px;">
                        {label}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif i == current:
                # Current/Active
                st.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <div style="
                        width: 50px;
                        height: 50px;
                        margin: 0 auto 8px;
                        border-radius: 50%;
                        background: linear-gradient(135deg, #FF9800, #F57C00);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                        box-shadow: 0 2px 8px rgba(255, 152, 0, 0.4);
                        animation: pulse 2s infinite;
                    ">
                        {icon}
                    </div>
                    <div style="color: #FF9800; font-weight: bold; font-size: 12px;">
                        ▶️ {label}
                    </div>
                </div>
                <style>
                @keyframes pulse {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.05); }}
                }}
                </style>
                """, unsafe_allow_html=True)
            else:
                # Locked/Future
                st.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <div style="
                        width: 50px;
                        height: 50px;
                        margin: 0 auto 8px;
                        border-radius: 50%;
                        background: #3e3e3e;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 20px;
                        color: #7E7E7E;
                        border: 2px dashed #5E5E5E;
                    ">
                        🔒
                    </div>
                    <div style="color: #7E7E7E; font-size: 12px;">
                        {label}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Progress bar
    progress = (current + len(completed)) / len(steps) if steps else 0
    st.progress(progress)
    
    st.markdown("---")

def render_navigation_buttons(
    show_previous: bool = True,
    show_next: bool = True,
    next_enabled: bool = True,
    next_label: str = "Suivant ➡️",
    previous_label: str = "⬅️ Précédent",
    on_previous = None,
    on_next = None,
    disabled_message: str = None
):
    """
    Render navigation buttons (Previous/Next).
    
    Args:
        show_previous: Show previous button
        show_next: Show next button
        next_enabled: Enable next button
        next_label: Label for next button
        previous_label: Label for previous button
        on_previous: Callback for previous button
        on_next: Callback for next button
        disabled_message: Message to show when next is disabled
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if show_previous:
            if st.button(previous_label, use_container_width=True):
                if on_previous:
                    on_previous()
    
    with col3:
        if show_next:
            if next_enabled:
                if st.button(next_label, type="primary", use_container_width=True):
                    if on_next:
                        on_next()
            else:
                st.button(next_label, disabled=True, use_container_width=True)
                if disabled_message:
                    st.caption(f"⚠️ {disabled_message}")
