"""Console lock management for guided mode."""
import streamlit as st

def is_console_locked(section: str) -> bool:
    """
    Check if a console section should be locked in guided mode.
    
    Args:
        section: Section name ("config", "temporal", "scenarios", "display")
    
    Returns:
        True if locked, False otherwise
    """
    if st.session_state.get("app_mode") != "guided":
        return False  # Never lock in expert mode
    
    current_step = st.session_state.get("guided_step", 1)
    
    # Règles de verrouillage
    lock_rules = {
        "config": current_step > 1,  # Lock après étape 1 (Configuration)
        "temporal": current_step > 1,  # Lock après étape 1
        "scenarios": current_step > 1,  # Lock après étape 1
        "display": False,  # Jamais verrouillé (préférences utilisateur)
    }
    
    return lock_rules.get(section, False)

def render_lock_message(section: str):
    """
    Render a lock message for a locked section.
    
    Args:
        section: Section name
    """
    messages = {
        "config": "🔒 Configuration verrouillée. Retournez à l'étape 1 pour modifier.",
        "temporal": "🔒 Paramètres temporels verrouillés. Retournez à l'étape 1 pour modifier.",
        "scenarios": "🔒 Scénarios verrouillés. Retournez à l'étape 1 pour modifier.",
    }
    
    st.info(messages.get(section, "🔒 Section verrouillée"))

def check_config_changed() -> bool:
    """
    Check if configuration has changed since last validation.
    
    Returns:
        True if config changed, False otherwise
    """
    if "validated_config" not in st.session_state:
        return False
    
    validated = st.session_state["validated_config"]
    current = {
        "mode": st.session_state.get("mode", "Free"),
        "domain": st.session_state.get("domain", "Trading"),
        "seed": st.session_state.get("seed", 42),
        "tau": st.session_state.get("tau", 10.0)
    }
    
    return validated != current

def mark_config_validated():
    """Mark current configuration as validated."""
    st.session_state["validated_config"] = {
        "mode": st.session_state.get("mode", "Free"),
        "domain": st.session_state.get("domain", "Trading"),
        "seed": st.session_state.get("seed", 42),
        "tau": st.session_state.get("tau", 10.0)
    }

def render_change_warning():
    """Render warning if config changed after validation."""
    if check_config_changed():
        st.warning("⚠️ **Configuration modifiée** : Les changements ne seront pas pris en compte. Retournez à l'étape 1 pour valider.")
