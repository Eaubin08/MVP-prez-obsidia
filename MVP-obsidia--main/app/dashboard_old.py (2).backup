"""Main dashboard for Obsidia - Professional Application."""
import streamlit as st
import hashlib
import time
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Obsidia",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports locaux
import sys
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import BASE_DIR, BUILD_VERSION, BUILD_HASH
from app.ui.styles import inject_custom_css

# Import des vues
from app.views import os0_invariants, os1_observation, os2_simulation, os3_governance, os5_autorun, os6_exploration
from app.views import os4_reports_extended as os4_reports
from app.views import dashboard_home, domain_analytics

# Inject custom CSS
inject_custom_css()

# Session state initialization
if "app_mode" not in st.session_state:
    st.session_state["app_mode"] = "Expert"  # Default to Expert mode

if "run_id" not in st.session_state:
    st.session_state.run_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

if "build_hash" not in st.session_state:
    st.session_state.build_hash = BUILD_HASH

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"

if "seed" not in st.session_state:
    st.session_state["seed"] = 42

if "tau" not in st.session_state:
    st.session_state["tau"] = 10.0

if "domain" not in st.session_state:
    st.session_state["domain"] = "trading"

if "os_level" not in st.session_state:
    st.session_state["os_level"] = "OS0"

# Configuration object
config = {
    "domain": st.session_state.get("domain", "trading"),
    "mode": "proof" if st.session_state.get("seed", 42) == 42 else "free",
    "seed": st.session_state.get("seed", 42),
    "tau": st.session_state.get("tau", 10.0),
    "run_id": st.session_state.run_id,
    "build_hash": st.session_state.build_hash
}

# ========================================
# MODE TOGGLE (En haut de la page principale)
# ========================================

# Toggle Mode Guidé / Expert
col_toggle1, col_toggle2, col_toggle3 = st.columns([1, 2, 1])
with col_toggle2:
    mode = st.radio(
        "",
        ["🎓 Mode Guidé", "⚡ Mode Expert"],
        horizontal=True,
        index=0 if st.session_state.get("app_mode", "Expert") == "Guidé" else 1,
        key="mode_toggle"
    )
    st.session_state["app_mode"] = "Guidé" if "Guidé" in mode else "Expert"

st.markdown("---")

# ========================================
# MODE GUIDÉ : Workflow pédagogique
# ========================================

if st.session_state["app_mode"] == "Guidé":
    from app.views import guided_workflow
    guided_workflow.render(BASE_DIR, config)
    st.stop()  # Ne pas afficher le reste (sidebar expert)

# ========================================
# SIDEBAR FIXE (Navigation + Config) - MODE EXPERT
# ========================================
with st.sidebar:
    st.title("🏛️ OBSIDIA")
    st.caption("Gouvernance Transparente IA")
    
    st.markdown("---")
    
    # NAVIGATION PRINCIPALE
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🔍 Analyse", "📊 Simulation", 
         "⚖️ Gouvernance", "📄 Rapports", "🧪 Stress Tests", "📊 Domaines"],
        label_visibility="collapsed",
        key="main_nav"
    )
    
    # Update current page
    st.session_state["current_page"] = page.split(" ", 1)[1]
    
    st.markdown("---")
    
    # CONFIG RAPIDE
    st.markdown("### ⚙️ Configuration")
    
    domain_options = ["Trading (ERC-8004)", "Medical-AI", "Legal-Contracts", "Auto-Drive", "Factory-Control"]
    domain_selected = st.selectbox(
        "Domaine",
        domain_options,
        help="Sélectionnez le domaine d'application"
    )
    st.session_state["domain"] = domain_selected.split(" ")[0].lower()
    
    st.session_state["seed"] = st.number_input(
        "Seed",
        min_value=0,
        max_value=9999,
        value=st.session_state.get("seed", 42),
        help="Graine aléatoire pour reproductibilité"
    )
    
    st.session_state["tau"] = st.slider(
        "Délai τ (s)",
        min_value=0.0,
        max_value=30.0,
        value=st.session_state.get("tau", 10.0),
        step=0.5,
        help="Délai de sécurité X-108"
    )
    
    st.markdown("---")
    
    # NIVEAU OS (Mode Expert)
    with st.expander("🔬 Mode Expert (OS Levels)"):
        os_level = st.radio(
            "OS Level",
            ["OS0 — Invariants", "OS1 — Exploration", "OS2 — Simulation", 
             "OS3 — Gouvernance", "OS4 — Rapports", "OS5 — Démo Auto", "OS6 — Stress"],
            label_visibility="collapsed"
        )
        st.session_state["os_level"] = os_level.split(" ")[0]
        
        if st.button("➡️ Aller au niveau OS", use_container_width=True):
            st.session_state["current_page"] = "Expert Mode"
            st.rerun()

# ========================================
# ZONE PRINCIPALE (Tabs + Contenu)
# ========================================

current_page = st.session_state.get("current_page", "Dashboard")

if current_page == "Dashboard":
    dashboard_home.render()

elif current_page == "Analyse":
    st.markdown("### 🔍 Analyse (OS1 — Exploration)")
    st.markdown("Explorez les données et extrayez les features sans prendre de décision.")
    st.markdown("---")
    os1_observation.render(BASE_DIR, config)

elif current_page == "Simulation":
    st.markdown("### 📊 Simulation (OS2 — Projection)")
    st.markdown("Projetez les scénarios futurs possibles via simulation Monte Carlo.")
    st.markdown("---")
    os2_simulation.render(BASE_DIR, config)

elif current_page == "Gouvernance":
    st.markdown("### ⚖️ Gouvernance (OS3 — Décision)")
    st.markdown("Appliquez les 3 gates de validation et la politique ROI pour émettre un intent.")
    st.markdown("---")
    os3_governance.render(BASE_DIR, config)

elif current_page == "Rapports":
    st.markdown("### 📄 Rapports (OS4 — Audit)")
    st.markdown("Consultez tous les artefacts générés et exportez les résultats.")
    st.markdown("---")
    os4_reports.render(BASE_DIR, config)

elif current_page == "Stress Tests":
    st.markdown("### 🧪 Stress Tests (OS6 — Validation)")
    st.markdown("Générez des scénarios aléatoires pour tester la robustesse du système.")
    st.markdown("---")
    os6_exploration.render(BASE_DIR, config)

elif current_page == "Domaines":
    domain_analytics.render()

elif current_page == "Expert Mode":
    # Mode Expert : Afficher le niveau OS sélectionné
    os_level = st.session_state.get("os_level", "OS0")
    
    if os_level == "OS0":
        st.markdown("### ⚖️ OS0 — Invariants (Lois Fondamentales)")
        os0_invariants.render(BASE_DIR, config)
    elif os_level == "OS1":
        st.markdown("### 🔍 OS1 — Exploration")
        os1_observation.render(BASE_DIR, config)
    elif os_level == "OS2":
        st.markdown("### 📊 OS2 — Simulation")
        os2_simulation.render(BASE_DIR, config)
    elif os_level == "OS3":
        st.markdown("### ⚖️ OS3 — Gouvernance")
        os3_governance.render(BASE_DIR, config)
    elif os_level == "OS4":
        st.markdown("### 📄 OS4 — Rapports")
        os4_reports.render(BASE_DIR, config)
    elif os_level == "OS5":
        st.markdown("### 🎬 OS5 — Démo Auto")
        os5_autorun.render(BASE_DIR, config)
    elif os_level == "OS6":
        st.markdown("### 🧪 OS6 — Stress Tests")
        os6_exploration.render(BASE_DIR, config)
