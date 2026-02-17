"""Actionable messages with direct links."""
import streamlit as st

def show_prerequisite_message(current_step: str, required_step: str, required_action: str):
    """
    Show a message when a prerequisite is not met, with actionable link.
    
    Args:
        current_step: The step user is trying to access (e.g., "OS2")
        required_step: The step that must be completed first (e.g., "OS1")
        required_action: The action that must be taken (e.g., "Calculer les features")
    """
    st.error(f"""
    🔒 **{current_step} bloqué** : Prérequis non satisfait
    
    Vous devez d'abord **{required_action}** dans **{required_step}**.
    """)
    
    if st.button(f"➡️ Aller à {required_step}", type="primary"):
        if current_step.startswith("OS"):
            st.session_state["os_level"] = required_step
        else:
            # For guided mode
            step_mapping = {
                "OS1": 2,
                "OS2": 3,
                "OS3": 4,
                "OS4": 5
            }
            st.session_state["guided_step"] = step_mapping.get(required_step, 1)
        st.rerun()

def show_success_message(action: str, next_step: str = None):
    """
    Show a success message with optional link to next step.
    
    Args:
        action: The action that was completed (e.g., "Features calculées")
        next_step: Optional next step to suggest (e.g., "OS2")
    """
    st.success(f"✅ **{action}** avec succès !")
    
    if next_step:
        st.info(f"💡 **Prochaine étape** : {next_step}")
        
        if st.button(f"➡️ Continuer vers {next_step}", type="primary"):
            if next_step.startswith("OS"):
                st.session_state["os_level"] = next_step
            else:
                step_mapping = {
                    "Simulation": 3,
                    "Gouvernance": 4,
                    "Rapport": 5
                }
                st.session_state["guided_step"] = step_mapping.get(next_step, st.session_state.get("guided_step", 1) + 1)
            st.rerun()

def show_config_locked_message():
    """
    Show a message when configuration is locked in guided mode.
    """
    st.warning("""
    ⚠️ **Configuration verrouillée**
    
    La configuration est verrouillée pour garantir la cohérence du workflow guidé.
    
    Pour modifier la configuration, retournez à l'étape 1 (Configuration).
    """)
    
    if st.button("⬅️ Retour à la configuration", key="unlock_config"):
        st.session_state["guided_step"] = 1
        st.rerun()

def show_export_success(artifact_path: str):
    """
    Show a success message after artifact export.
    
    Args:
        artifact_path: Path to the exported artifact
    """
    st.success(f"✅ **Artefact exporté** : `{artifact_path}`")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Télécharger", key="download_artifact"):
            # Trigger download
            with open(artifact_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger le fichier",
                    data=f,
                    file_name=artifact_path.split("/")[-1],
                    mime="application/json"
                )
    
    with col2:
        if st.button("📊 Voir dans OS4", key="view_in_os4"):
            st.session_state["os_level"] = "OS4"
            st.rerun()
