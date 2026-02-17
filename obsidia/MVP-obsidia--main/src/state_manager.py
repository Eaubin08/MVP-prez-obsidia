"""State management for Streamlit app with proper synchronization."""
import streamlit as st
from typing import Any, Dict

def init_config_state():
    """Initialize configuration state if not exists."""
    if "config" not in st.session_state:
        st.session_state.config = {
            "seed": 42,
            "tau": 10.0,
            "domain": "Trading (ERC-8004)",
            "mode": "Proof (Deterministic)"
        }
    
    # Initialize data computation flags
    if "data_flags" not in st.session_state:
        st.session_state.data_flags = {
            "features_computed": False,
            "simulation_done": False,
            "governance_tested": False,
            "features_hash": None,  # Pour détecter les changements
            "simulation_hash": None,
            "governance_hash": None
        }

def update_config(key: str, value: Any) -> bool:
    """
    Update configuration and invalidate dependent data if needed.
    Returns True if data needs to be recomputed.
    """
    if key not in st.session_state.config:
        return False
    
    old_value = st.session_state.config[key]
    
    if old_value != value:
        st.session_state.config[key] = value
        
        # Invalider les données dépendantes
        if key in ["seed", "domain"]:
            # Ces paramètres affectent les features
            st.session_state.data_flags["features_computed"] = False
            st.session_state.data_flags["simulation_done"] = False
            st.session_state.data_flags["governance_tested"] = False
            
            # Supprimer les données en cache
            if "features" in st.session_state:
                del st.session_state["features"]
            if "simulation" in st.session_state:
                del st.session_state["simulation"]
            if "gates_result" in st.session_state:
                del st.session_state["gates_result"]
            
            return True
        
        elif key == "tau":
            # τ affecte seulement la gouvernance
            st.session_state.data_flags["governance_tested"] = False
            if "gates_result" in st.session_state:
                del st.session_state["gates_result"]
            return True
    
    return False

def get_config() -> Dict[str, Any]:
    """Get current configuration."""
    init_config_state()
    return st.session_state.config

def get_data_flags() -> Dict[str, bool]:
    """Get data computation flags."""
    init_config_state()
    return st.session_state.data_flags

def mark_features_computed():
    """Mark features as computed."""
    st.session_state.data_flags["features_computed"] = True
    # Générer un hash pour détecter les changements
    cfg = st.session_state.config
    st.session_state.data_flags["features_hash"] = f"{cfg['seed']}_{cfg['domain']}"

def mark_simulation_done():
    """Mark simulation as done."""
    st.session_state.data_flags["simulation_done"] = True
    cfg = st.session_state.config
    st.session_state.data_flags["simulation_hash"] = f"{cfg['seed']}_{cfg['domain']}"

def mark_governance_tested():
    """Mark governance as tested."""
    st.session_state.data_flags["governance_tested"] = True
    cfg = st.session_state.config
    st.session_state.data_flags["governance_hash"] = f"{cfg['seed']}_{cfg['domain']}_{cfg['tau']}"

def is_features_valid() -> bool:
    """Check if features are valid for current config."""
    if not st.session_state.data_flags["features_computed"]:
        return False
    
    cfg = st.session_state.config
    expected_hash = f"{cfg['seed']}_{cfg['domain']}"
    return st.session_state.data_flags.get("features_hash") == expected_hash

def is_simulation_valid() -> bool:
    """Check if simulation is valid for current config."""
    if not st.session_state.data_flags["simulation_done"]:
        return False
    
    cfg = st.session_state.config
    expected_hash = f"{cfg['seed']}_{cfg['domain']}"
    return st.session_state.data_flags.get("simulation_hash") == expected_hash

def is_governance_valid() -> bool:
    """Check if governance is valid for current config."""
    if not st.session_state.data_flags["governance_tested"]:
        return False
    
    cfg = st.session_state.config
    expected_hash = f"{cfg['seed']}_{cfg['domain']}_{cfg['tau']}"
    return st.session_state.data_flags.get("governance_hash") == expected_hash

def get_unique_key(base: str) -> str:
    """Generate unique key for widgets based on current config."""
    cfg = st.session_state.config
    return f"{base}_{cfg['seed']}_{cfg['domain']}_{cfg['tau']}"
