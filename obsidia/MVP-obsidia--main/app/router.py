"""Router pour la navigation entre les niveaux OS."""
import streamlit as st
from app.config import OS_LEVELS

def select_os_level() -> str:
    """Affiche le sélecteur de niveau OS dans la sidebar."""
    return st.sidebar.radio("OS Level", OS_LEVELS, index=0)

def get_os_key(os_level: str) -> str:
    """Extrait la clé OS (OS0, OS1, etc.) du label complet."""
    return os_level.split(" ")[0]
