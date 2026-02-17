"""Guided workflow for step-by-step user experience."""
import streamlit as st
from pathlib import Path
from app.views import os1_observation, os2_simulation, os3_governance, os4_reports_extended
from app.ui.navigation import render_permanent_header, render_breadcrumb, render_enhanced_stepper
from app.ui.console_x108 import render_console_x108
from src.state_manager import init_config_state, get_data_flags

def render(base_dir: Path, config: dict):
    """Affiche le workflow guidé."""
    
    # Initialiser state
    init_config_state()
    
    # Initialiser l'étape si nécessaire
    if "guided_step" not in st.session_state:
        st.session_state["guided_step"] = 1
    
    current_step = st.session_state["guided_step"]
    
    # Header permanent
    render_permanent_header(mode="guided", step=current_step)
    
    # Breadcrumb
    step_names = ["Mode Guidé", "Configuration", "Exploration", "Simulation", "Gouvernance", "Rapport"]
    render_breadcrumb(step_names[:current_step+1], current_step)
    
    # Stepper amélioré
    steps = [
        ("⚙️", "Configuration"),
        ("🔍", "Exploration"),
        ("🎲", "Simulation"),
        ("⚖️", "Gouvernance"),
        ("📊", "Rapport")
    ]
    
    # Déterminer les étapes complétées
    flags = get_data_flags()
    completed = []
    if current_step > 1:
        completed.append(0)  # Config toujours complétée après étape 1
    if flags["features_computed"] and current_step > 2:
        completed.append(1)  # Exploration complétée
    if flags["simulation_done"] and current_step > 3:
        completed.append(2)  # Simulation complétée
    if flags["governance_tested"] and current_step > 4:
        completed.append(3)  # Gouvernance complétée
    
    render_enhanced_stepper(steps, current_step - 1, completed)
    
    # Console X-108 dans une colonne latérale
    col_main, col_console = st.columns([3, 1])
    
    with col_console:
        render_console_x108()
    
    with col_main:
        # Contenu selon l'étape
        if current_step == 1:
            render_step1_config(config)
        elif current_step == 2:
            render_step2_exploration(base_dir, config)
        elif current_step == 3:
            render_step3_simulation(base_dir, config)
        elif current_step == 4:
            render_step4_governance(base_dir, config)
        elif current_step == 5:
            render_step5_report(base_dir, config)

def render_guided_stepper(current_step: int):
    """Affiche le stepper du mode guidé."""
    steps = [
        ("1", "Configuration", "⚙️"),
        ("2", "Exploration", "🔍"),
        ("3", "Simulation", "🎲"),
        ("4", "Gouvernance", "⚖️"),
        ("5", "Rapport", "📊")
    ]
    
    cols = st.columns(5)
    
    for i, (num, label, icon) in enumerate(steps, 1):
        with cols[i-1]:
            if i < current_step:
                st.markdown(f"<div style='text-align: center; color: #4CAF50;'>{icon}<br><strong>✓ {label}</strong></div>", unsafe_allow_html=True)
            elif i == current_step:
                st.markdown(f"<div style='text-align: center; color: #FF9800;'>{icon}<br><strong>▶️ {label}</strong></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: center; color: #9E9E9E;'>{icon}<br>{label}</div>", unsafe_allow_html=True)
    
    st.markdown("---")

def render_step1_config(config: dict):
    """Étape 1: Configuration."""
    from src.console_lock import mark_config_validated
    
    st.markdown("## ⚙️ Étape 1 : Configuration")
    
    st.markdown("""
    **Objectif** : Configurer les paramètres de base pour l'analyse de gouvernance.
    
    **Paramètres clés** :
    - **Domaine d'application** : Trading, Santé, Juridique, Véhicules, Industrie
    - **Délai de sécurité τ** : Temps d'attente obligatoire avant action irréversible (X-108)
    - **Graine aléatoire (Seed)** : Garantit la reproductibilité des résultats
    """)
    
    # Afficher la configuration actuelle
    st.markdown("### 📋 Configuration Actuelle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🎯 Domaine", config["domain"])
        st.metric("🎲 Seed", config["seed"])
    
    with col2:
        st.metric("🔒 Délai τ", f"{config['tau']}s")
        st.metric("🎭 Mode", config["mode"])
    
    st.markdown("---")
    
    # Marquer config comme validée
    mark_config_validated()
    
    st.success("✅ **Configuration validée**")
    st.caption("Les paramètres sont verrouillés pour garantir la cohérence du workflow. Retournez à cette étape pour les modifier.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Retour au menu", use_container_width=True):
            st.session_state["app_mode"] = None
            del st.session_state["guided_step"]
            st.rerun()
    
    with col3:
        if st.button("Suivant ➡️", type="primary", use_container_width=True):
            st.session_state["guided_step"] = 2
            st.rerun()

def render_step2_exploration(base_dir: Path, config: dict):
    """Étape 2: Exploration."""
    st.markdown("## 🔍 Étape 2 : Exploration des Données")
    
    st.markdown("""
    **Objectif** : Extraire les features (caractéristiques) des données de marché pour alimenter la simulation.
    
    **Processus** :
    1. Visualisation des données (prix, volatilité)
    2. Calcul des métriques (cohérence, stabilité, friction)
    3. Export vers features.json
    
    **Rôle** : Explorer (séparation des rôles). Aucune action irréversible possible.
    """)
    
    st.markdown("---")
    
    # Appeler la vue OS1
    os1_observation.render(base_dir, config)
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Précédent", use_container_width=True):
            st.session_state["guided_step"] = 1
            st.rerun()
    
    with col3:
        # Vérifier si les features sont calculées
        has_features = "features" in st.session_state
        
        if st.button("Suivant ➡️", type="primary", use_container_width=True, disabled=not has_features):
            if has_features:
                st.session_state["guided_step"] = 3
                st.rerun()
            else:
                st.warning("⚠️ Veuillez d'abord calculer les features en cliquant sur '🧮 Compute Features'")

def render_step3_simulation(base_dir: Path, config: dict):
    """Étape 3: Simulation."""
    st.markdown("## 🎲 Étape 3 : Simulation Monte Carlo")
    
    st.markdown("""
    **Objectif** : Projeter les scénarios futurs possibles via simulation Monte Carlo.
    
    **Méthode** : Génération de N scénarios stochastiques sur horizon H.
    
    **Métriques clés** :
    - μ (expected return), σ (volatility)
    - CVaR 95% (Conditional Value at Risk)
    - P(DD > threshold), P(Ruin)
    
    **Sortie** : simulation.json avec verdict (OK/UNCERTAIN/DESTRUCTIVE).
    """)
    
    st.markdown("---")
    
    # Appeler la vue OS2
    os2_simulation.render(base_dir, config)
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Précédent", use_container_width=True):
            st.session_state["guided_step"] = 2
            st.rerun()
    
    with col3:
        has_simulation = "simulation" in st.session_state
        
        if st.button("Suivant ➡️", type="primary", use_container_width=True, disabled=not has_simulation):
            if has_simulation:
                st.session_state["guided_step"] = 4
                st.rerun()
            else:
                st.warning("⚠️ Veuillez d'abord exécuter la simulation")

def render_step4_governance(base_dir: Path, config: dict):
    """Étape 4: Gouvernance."""
    st.markdown("## ⚖️ Étape 4 : Gouvernance et Décision")
    
    st.markdown("""
    **Objectif** : Évaluer les gates de validation et appliquer la politique ROI.
    
    **Gates** :
    - G1 (Integrity) : Cohérence des données
    - G2 (X-108) : Temporal Lock (τ seconds)
    - G3 (Risk) : Killswitch sur CVaR
    
    **Composition** : max(BLOCK, HOLD, ALLOW) → Priorité BLOCK > HOLD > ALLOW
    
    **Sortie** : gates.json + erc8004_intent.json (paper intent)
    """)
    
    st.markdown("---")
    
    # Appeler la vue OS3
    os3_governance.render(base_dir, config)
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Précédent", use_container_width=True):
            st.session_state["guided_step"] = 3
            st.rerun()
    
    with col3:
        if st.button("Suivant ➡️", type="primary", use_container_width=True):
            st.session_state["guided_step"] = 5
            st.rerun()

def render_step5_report(base_dir: Path, config: dict):
    """Étape 5: Rapport."""
    st.markdown("## 📊 Étape 5 : Rapport et Export")
    
    st.markdown("""
    **Objectif** : Consulter les artefacts et exporter les résultats pour audit.
    
    **Artefacts disponibles** :
    - features.json, simulation.json, gates.json
    - erc8004_intent.json (paper intent)
    - os0_snapshot.json (configuration)
    
    **Formats d'export** : JSON (structured), JSONL (streaming), ZIP (archive)
    
    **Traçabilité** : Run ID + Seed + Build Hash garantissent la reproductibilité.
    """)
    
    st.markdown("---")
    
    # Appeler la vue OS4
    os4_reports_extended.render(base_dir, config)
    
    st.markdown("---")
    
    # Navigation finale
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Précédent", use_container_width=True):
            st.session_state["guided_step"] = 4
            st.rerun()
    
    with col2:
        if st.button("🔄 Recommencer", use_container_width=True):
            st.session_state["guided_step"] = 1
            # Nettoyer le session state
            for key in ["features", "simulation", "gates_result", "roi_decision"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col3:
        if st.button("⚡ Mode Expert", type="primary", use_container_width=True):
            st.session_state["app_mode"] = "expert"
            del st.session_state["guided_step"]
            st.rerun()
