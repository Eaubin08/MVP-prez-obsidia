"""Enhanced UI components for better UX."""
import streamlit as st
from typing import Dict, List, Tuple

def render_progress_stepper(current_os: str, session_state: dict) -> None:
    """Affiche un stepper horizontal montrant la progression dans le workflow."""
    
    # Définir les étapes et leurs statuts
    steps = [
        ("OS0", "Invariants", "always"),
        ("OS1", "Explore", "required"),
        ("OS2", "Simulate", "depends_os1"),
        ("OS3", "Govern", "depends_os1_os2"),
        ("OS4", "Reports", "always"),
        ("OS5", "Demo", "always"),
        ("OS6", "Stress", "always")
    ]
    
    # Vérifier l'état de complétion
    has_features = "features" in session_state
    has_simulation = "simulation" in session_state
    
    # CSS pour le stepper
    st.markdown("""
    <style>
    .stepper-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        position: relative;
    }
    .step-number {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 8px;
        z-index: 2;
    }
    .step-label {
        font-size: 12px;
        text-align: center;
        color: white;
        font-weight: 500;
    }
    .step-active {
        background: #4CAF50;
        color: white;
        box-shadow: 0 0 15px rgba(76, 175, 80, 0.6);
    }
    .step-completed {
        background: #2196F3;
        color: white;
    }
    .step-locked {
        background: #9E9E9E;
        color: white;
    }
    .step-available {
        background: white;
        color: #667eea;
    }
    .step-connector {
        position: absolute;
        top: 20px;
        left: 50%;
        width: 100%;
        height: 2px;
        background: rgba(255,255,255,0.3);
        z-index: 1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Construire le HTML du stepper
    stepper_html = '<div class="stepper-container">'
    
    for i, (os_key, label, status) in enumerate(steps):
        # Déterminer la classe CSS
        if os_key == current_os:
            step_class = "step-active"
            icon = "✓"
        elif status == "always":
            step_class = "step-available"
            icon = os_key[-1]
        elif status == "required":
            step_class = "step-available" if not has_features else "step-completed"
            icon = "✓" if has_features else "1"
        elif status == "depends_os1":
            if not has_features:
                step_class = "step-locked"
                icon = "🔒"
            else:
                step_class = "step-completed" if has_simulation else "step-available"
                icon = "✓" if has_simulation else "2"
        elif status == "depends_os1_os2":
            if not has_features or not has_simulation:
                step_class = "step-locked"
                icon = "🔒"
            else:
                step_class = "step-available"
                icon = "3"
        else:
            step_class = "step-available"
            icon = os_key[-1]
        
        stepper_html += f'''
        <div class="step">
            {f'<div class="step-connector"></div>' if i < len(steps) - 1 else ''}
            <div class="step-number {step_class}">{icon}</div>
            <div class="step-label">{label}</div>
        </div>
        '''
    
    stepper_html += '</div>'
    
    st.markdown(stepper_html, unsafe_allow_html=True)

def render_os_badge(os_key: str, session_state: dict) -> str:
    """Retourne un badge HTML pour un niveau OS."""
    
    has_features = "features" in session_state
    has_simulation = "simulation" in session_state
    
    badges = {
        "OS0": ("✅ Toujours accessible", "success"),
        "OS1": ("🎯 Démarrez ici", "warning"),
        "OS2": ("🔒 Nécessite OS1" if not has_features else "✅ Disponible", "error" if not has_features else "success"),
        "OS3": ("🔒 Nécessite OS1+OS2" if not (has_features and has_simulation) else "✅ Disponible", 
                "error" if not (has_features and has_simulation) else "success"),
        "OS4": ("✅ Toujours accessible", "success"),
        "OS5": ("✅ Mode démo", "success"),
        "OS6": ("✅ Tests avancés", "success")
    }
    
    text, badge_type = badges.get(os_key, ("", "info"))
    
    colors = {
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#F44336",
        "info": "#2196F3"
    }
    
    color = colors.get(badge_type, colors["info"])
    
    return f'<span style="background-color: {color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;">{text}</span>'

def show_toast(message: str, icon: str = "ℹ️", duration: int = 3):
    """Affiche une notification toast."""
    st.toast(f"{icon} {message}", icon=icon)

def render_help_tooltip(text: str) -> str:
    """Retourne un tooltip HTML."""
    return f'''
    <span style="cursor: help; color: #2196F3; font-weight: bold;" title="{text}">
        ℹ️
    </span>
    '''

def render_section_header(title: str, description: str, icon: str = "📋"):
    """Affiche un en-tête de section amélioré."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; 
                border-radius: 10px; 
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2 style="color: white; margin: 0; font-size: 24px;">
            {icon} {title}
        </h2>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 14px;">
            {description}
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_info_card(title: str, content: str, icon: str = "💡", color: str = "#2196F3"):
    """Affiche une carte d'information."""
    st.markdown(f"""
    <div style="background: white; 
                border-left: 4px solid {color}; 
                padding: 15px; 
                border-radius: 5px; 
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 24px; margin-right: 10px;">{icon}</span>
            <strong style="font-size: 16px; color: {color};">{title}</strong>
        </div>
        <p style="margin: 0; color: #555; line-height: 1.6;">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_workflow_guide(current_step: int = 1):
    """Affiche un guide de workflow étape par étape."""
    steps = [
        ("Configuration", "Choisissez votre domaine et vos paramètres"),
        ("Exploration", "Visualisez les données et calculez les features"),
        ("Simulation", "Projetez les risques avec Monte Carlo"),
        ("Gouvernance", "Évaluez les gates et émettez un intent"),
        ("Rapport", "Exportez et analysez les résultats")
    ]
    
    st.markdown("### 🧭 Guide du Workflow")
    
    for i, (title, desc) in enumerate(steps, 1):
        if i < current_step:
            icon = "✅"
            color = "#4CAF50"
        elif i == current_step:
            icon = "▶️"
            color = "#FF9800"
        else:
            icon = "⏸️"
            color = "#9E9E9E"
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 10px; margin: 5px 0; 
                    background: {'#f0f0f0' if i != current_step else '#fff3e0'}; 
                    border-radius: 5px;">
            <span style="font-size: 20px; margin-right: 15px; color: {color};">{icon}</span>
            <div>
                <strong style="color: {color};">Étape {i}: {title}</strong><br>
                <small style="color: #666;">{desc}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_navigation_buttons(prev_os: str = None, next_os: str = None, next_disabled: bool = False):
    """Affiche des boutons de navigation entre les OS."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if prev_os:
            if st.button(f"⬅️ {prev_os}", use_container_width=True):
                st.session_state["navigate_to"] = prev_os
                st.rerun()
    
    with col3:
        if next_os:
            if st.button(f"{next_os} ➡️", use_container_width=True, disabled=next_disabled):
                st.session_state["navigate_to"] = next_os
                st.rerun()
