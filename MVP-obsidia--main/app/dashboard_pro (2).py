"""
Obsidia Pro - Application Complète de Gouvernance IA
====================================================
Version professionnelle avec:
- Base de données SQLite pour l'historique
- Authentification utilisateurs
- Notifications email
- Exports PDF/Excel/JSON
"""
import streamlit as st
import hashlib
import time
from pathlib import Path
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Obsidia Pro - Gouvernance IA",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports locaux
import sys
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import BASE_DIR, BUILD_VERSION, BUILD_HASH
from app.database import (
    init_database, create_run, complete_run, save_features, save_simulation,
    save_decision, save_intent, get_all_runs, get_statistics, get_run,
    get_features, get_simulation, get_decision, get_intent
)
from app.auth import (
    init_auth_session, is_authenticated, get_current_user, render_login_form,
    render_user_menu, require_admin
)
from app.notifications import notify_execute_decision, render_notifications_panel
from app.exporters import render_export_buttons

# Initialiser la base de données et l'authentification
init_database()
init_auth_session()

# ============================================================
# STYLES CSS PROFESSIONNELS
# ============================================================
st.markdown("""
<style>
    /* Sidebar professionnelle */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(124, 159, 255, 0.2);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .status-completed { background: rgba(76, 175, 80, 0.2); color: #4CAF50; }
    .status-pending { background: rgba(255, 152, 0, 0.2); color: #FF9800; }
    .status-locked { background: rgba(100, 100, 100, 0.2); color: #888; }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# INITIALISATION SESSION STATE
# ============================================================
def init_session_state():
    """Initialise l'état de session avec valeurs par défaut."""
    defaults = {
        "run_id": hashlib.sha256(str(time.time()).encode()).hexdigest()[:12],
        "build_hash": BUILD_HASH,
        "current_page": "accueil",
        "domain": "trading",
        "seed": 42,
        "tau": 10.0,
        "features": None,
        "simulation": None,
        "gates_result": None,
        "intent_emitted": None,
        "pipeline_status": {
            "analysis": "pending",
            "simulation": "locked",
            "decision": "locked",
            "report": "locked"
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
def render_sidebar():
    """Rend la sidebar de navigation professionnelle."""
    
    # Logo et titre
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 40px; margin-bottom: 8px;">🏛️</div>
        <div style="font-size: 20px; font-weight: bold; color: #7c9fff;">OBSIDIA</div>
        <div style="font-size: 11px; color: #888; margin-top: 4px;">Gouvernance Transparente IA</div>
        <div style="font-size: 10px; color: #4CAF50; margin-top: 4px;">● Pro</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Navigation principale
    current = st.session_state["current_page"]
    
    pages = [
        ("accueil", "🏠", "Accueil"),
        ("analyse", "🔍", "Analyse"),
        ("simulation", "🎲", "Simulation"),
        ("decision", "⚖️", "Décision"),
        ("rapports", "📊", "Rapports"),
    ]
    
    for page_id, icon, label in pages:
        is_active = current == page_id
        btn_type = "primary" if is_active else "secondary"
        
        if st.sidebar.button(
            f"{icon} {label}",
            key=f"nav_{page_id}",
            use_container_width=True,
            type=btn_type
        ):
            st.session_state["current_page"] = page_id
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Configuration rapide
    st.sidebar.markdown("#### ⚙️ Configuration")
    
    domain = st.sidebar.selectbox(
        "Domaine",
        ["Trading", "Medical-AI", "Legal", "Auto-Drive", "Factory"],
        index=0
    )
    st.session_state["domain"] = domain.lower()
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        seed = st.sidebar.number_input("Seed", min_value=0, max_value=9999, value=st.session_state["seed"])
        st.session_state["seed"] = seed
    with col2:
        tau = st.sidebar.slider("τ (s)", min_value=0.0, max_value=30.0, value=st.session_state["tau"], step=1.0)
        st.session_state["tau"] = tau
    
    st.sidebar.markdown("---")
    
    # Status du pipeline
    st.sidebar.markdown("#### 📈 Pipeline")
    status = st.session_state["pipeline_status"]
    status_icons = {"completed": "✅", "pending": "⏳", "locked": "🔒"}
    
    for step, state in status.items():
        st.sidebar.markdown(f"{status_icons.get(state, '⚪')} {step.capitalize()}")
    
    # Menu utilisateur
    render_user_menu()

# ============================================================
# PAGES
# ============================================================

def page_accueil():
    """Page d'accueil avec dashboard opérationnel."""
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🏛️ Obsidia Pro")
        st.caption("Plateforme de gouvernance et d'audit pour agents autonomes")
    with col2:
        user = get_current_user()
        if user:
            st.metric("Utilisateur", user["username"])
        st.caption(f"v{BUILD_VERSION} • {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    st.markdown("---")
    
    # Statistiques globales
    stats = get_statistics()
    
    st.subheader("📊 Statistiques Globales")
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Total Runs", stats.get("total_runs", 0))
    with cols[1]:
        st.metric("Utilisateurs", stats.get("total_users", 0))
    with cols[2]:
        st.metric("Runs Aujourd'hui", stats.get("runs_today", 0))
    with cols[3]:
        decisions = stats.get("decisions", {})
        executes = decisions.get("EXECUTE", 0)
        st.metric("Intents Approuvés", executes)
    
    st.markdown("---")
    
    # Pipeline visuel
    st.subheader("🔄 Pipeline de Gouvernance")
    
    status = st.session_state["pipeline_status"]
    
    cols = st.columns(4)
    steps = [
        ("analysis", "🔍", "Analyse", "Extraction des features"),
        ("simulation", "🎲", "Simulation", "Projection Monte Carlo"),
        ("decision", "⚖️", "Décision", "Validation des gates"),
        ("report", "📊", "Rapport", "Audit et export")
    ]
    
    for i, (key, icon, title, desc) in enumerate(steps):
        with cols[i]:
            state = status.get(key, "locked")
            if state == "completed":
                st.success(f"**{icon} {title}**\n{desc}")
            elif state == "pending":
                st.info(f"**{icon} {title}**\n{desc}")
            else:
                st.markdown(f"**{icon} {title}**\n*{desc}*")
    
    st.markdown("---")
    
    # Actions rapides
    st.subheader("⚡ Actions Rapides")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Nouvelle Analyse", key="qa_analyse", use_container_width=True, type="primary"):
            # Créer un nouveau run dans la base de données
            user = get_current_user()
            user_id = user["id"] if user else None
            create_run(
                st.session_state["run_id"],
                user_id,
                st.session_state["domain"],
                st.session_state["seed"],
                st.session_state["tau"]
            )
            st.session_state["current_page"] = "analyse"
            st.rerun()
    
    with col2:
        if st.button("📊 Voir l'Historique", key="qa_history", use_container_width=True):
            st.session_state["current_page"] = "rapports"
            st.rerun()
    
    with col3:
        if st.button("🔔 Notifications", key="qa_notif", use_container_width=True):
            st.session_state["show_notifications"] = True
            st.rerun()
    
    # Afficher les notifications si demandé
    if st.session_state.get("show_notifications"):
        st.markdown("---")
        user = get_current_user()
        if user:
            render_notifications_panel(user["id"])
    
    st.markdown("---")
    
    # Derniers runs
    st.subheader("📋 Derniers Runs")
    
    runs_df = get_all_runs(limit=10)
    if not runs_df.empty:
        st.dataframe(runs_df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun run enregistré. Commencez par une nouvelle analyse !")


def page_analyse():
    """Page d'analyse (OS1)."""
    from app.views import os1_observation
    
    st.title("🔍 Analyse des Données")
    st.caption("Extraction des features et caractéristiques du marché")
    
    st.markdown("---")
    
    # Description du processus
    with st.expander("ℹ️ Comprendre cette étape", expanded=False):
        st.markdown("""
        **Objectif** : Extraire les caractéristiques (features) des données de marché.
        
        **Features calculées** :
        - **Volatility** : Volatilité réalisée sur les 20 dernières périodes
        - **Coherence** : Cohérence du marché (0-1, 1 = très cohérent)
        - **Friction** : Friction de volatilité (0-1, 1 = très volatile)
        - **Regime** : Régime de marché (trend_up, trend_down, range)
        
        **Sortie** : Fichier `features.json` pour la simulation.
        """)
    
    # Contenu OS1
    config = {
        "domain": st.session_state["domain"],
        "seed": st.session_state["seed"],
        "tau": st.session_state["tau"],
        "run_id": st.session_state["run_id"],
        "build_hash": st.session_state["build_hash"]
    }
    
    os1_observation.render(BASE_DIR, config)
    
    # Mise à jour du status et sauvegarde si features calculées
    if st.session_state.get("features") is not None:
        st.session_state["pipeline_status"]["analysis"] = "completed"
        st.session_state["pipeline_status"]["simulation"] = "pending"
        
        # Sauvegarder dans la base de données
        save_features(st.session_state["run_id"], st.session_state["features"])
        
        st.success("✅ Analyse complétée et sauvegardée ! Vous pouvez passer à la Simulation.")
        if st.button("➡️ Passer à la Simulation", type="primary"):
            st.session_state["current_page"] = "simulation"
            st.rerun()


def page_simulation():
    """Page de simulation (OS2)."""
    from app.views import os2_simulation
    
    st.title("🎲 Simulation Monte Carlo")
    st.caption("Projection des scénarios futurs possibles")
    
    st.markdown("---")
    
    # Vérifier prérequis
    if st.session_state["pipeline_status"]["analysis"] != "completed":
        st.error("🔒 **Étape verrouillée** : Veuillez d'abord compléter l'Analyse.")
        if st.button("⬅️ Retour à l'Analyse"):
            st.session_state["current_page"] = "analyse"
            st.rerun()
        return
    
    with st.expander("ℹ️ Comprendre cette étape", expanded=False):
        st.markdown("""
        **Objectif** : Projeter les scénarios futurs via simulation Monte Carlo.
        
        **Méthode** : Bootstrap - 200 simulations sur horizon de 20 périodes.
        
        **Métriques** :
        - **μ** : Rendement moyen projeté
        - **σ** : Volatilité projetée
        - **P(ruin)** : Probabilité de ruine
        - **P(DD)** : Probabilité de drawdown > 5%
        - **CVaR_95** : Conditional Value at Risk (95%)
        
        **Verdict** : OK / UNCERTAIN / DESTRUCTIVE
        """)
    
    config = {
        "domain": st.session_state["domain"],
        "seed": st.session_state["seed"],
        "tau": st.session_state["tau"],
        "run_id": st.session_state["run_id"],
        "build_hash": st.session_state["build_hash"]
    }
    
    os2_simulation.render(BASE_DIR, config)
    
    if st.session_state.get("simulation") is not None:
        st.session_state["pipeline_status"]["simulation"] = "completed"
        st.session_state["pipeline_status"]["decision"] = "pending"
        
        # Sauvegarder dans la base de données
        save_simulation(st.session_state["run_id"], st.session_state["simulation"])
        
        st.success("✅ Simulation complétée et sauvegardée ! Vous pouvez passer à la Décision.")
        if st.button("➡️ Passer à la Décision", type="primary"):
            st.session_state["current_page"] = "decision"
            st.rerun()


def page_decision():
    """Page de décision (OS3)."""
    from app.views import os3_governance
    
    st.title("⚖️ Décision et Gouvernance")
    st.caption("Évaluation des gates et émission d'intent")
    
    st.markdown("---")
    
    # Vérifier prérequis
    if st.session_state["pipeline_status"]["simulation"] != "completed":
        st.error("🔒 **Étape verrouillée** : Veuillez d'abord compléter la Simulation.")
        if st.button("⬅️ Retour à la Simulation"):
            st.session_state["current_page"] = "simulation"
            st.rerun()
        return
    
    with st.expander("ℹ️ Comprendre cette étape", expanded=False):
        st.markdown("""
        **Objectif** : Évaluer les gates de validation et décider de l'action.
        
        **Gates** :
        - **Gate 1 (Integrity)** : Validation des champs de l'intent
        - **Gate 2 (X-108)** : Vérification du délai temporel τ
        - **Gate 3 (Risk)** : Killswitch sur risque élevé
        
        **Décision** : BLOCK > HOLD > EXECUTE (hiérarchie stricte)
        
        **Sortie** : Intent ERC-8004 (paper) si EXECUTE
        """)
    
    config = {
        "domain": st.session_state["domain"],
        "seed": st.session_state["seed"],
        "tau": st.session_state["tau"],
        "run_id": st.session_state["run_id"],
        "build_hash": st.session_state["build_hash"]
    }
    
    os3_governance.render(BASE_DIR, config)
    
    # Sauvegarder la décision et notifier si EXECUTE
    if st.session_state.get("gates_result") is not None:
        gates_result = st.session_state["gates_result"]
        
        # Sauvegarder dans la base de données
        save_decision(st.session_state["run_id"], gates_result)
        
        # Mettre à jour le status
        st.session_state["pipeline_status"]["decision"] = "completed"
        st.session_state["pipeline_status"]["report"] = "pending"
        
        # Si EXECUTE, notifier et sauvegarder l'intent
        if gates_result.get("decision") == "EXECUTE":
            user = get_current_user()
            if user and st.session_state.get("intent_emitted"):
                # Sauvegarder l'intent
                save_intent(st.session_state["run_id"], st.session_state["intent_emitted"])
                
                # Envoyer notification
                notify_execute_decision(
                    user["id"],
                    st.session_state["run_id"],
                    st.session_state["intent_emitted"],
                    st.session_state.get("features", {}),
                    gates_result
                )
                st.success("📧 Notification envoyée !")


def page_rapports():
    """Page de rapports (OS4)."""
    from app.views import os4_reports_extended
    
    st.title("📊 Rapports et Audit")
    st.caption("Consultation des artefacts et export des résultats")
    
    st.markdown("---")
    
    # Onglets pour différentes vues
    tab1, tab2, tab3 = st.tabs(["📋 Historique", "📄 Rapport Actuel", "📤 Exports"])
    
    with tab1:
        st.subheader("📋 Historique des Runs")
        
        runs_df = get_all_runs(limit=50)
        if not runs_df.empty:
            st.dataframe(runs_df, use_container_width=True, hide_index=True)
            
            # Sélection d'un run pour voir les détails
            selected_run = st.selectbox(
                "Sélectionner un run pour voir les détails",
                runs_df["run_id"].tolist(),
                format_func=lambda x: f"#{x[:8]}... ({runs_df[runs_df['run_id']==x]['final_decision'].values[0] if not runs_df[runs_df['run_id']==x].empty else 'N/A'})"
            )
            
            if selected_run:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    features = get_features(selected_run)
                    if features:
                        st.markdown("**Features**")
                        st.json(features)
                
                with col2:
                    sim = get_simulation(selected_run)
                    if sim:
                        st.markdown("**Simulation**")
                        st.json(sim)
                
                with col3:
                    decision = get_decision(selected_run)
                    if decision:
                        st.markdown("**Décision**")
                        st.json(decision)
        else:
            st.info("Aucun run enregistré.")
    
    with tab2:
        st.subheader("📄 Rapport du Run Actuel")
        
        config = {
            "domain": st.session_state["domain"],
            "seed": st.session_state["seed"],
            "tau": st.session_state["tau"],
            "run_id": st.session_state["run_id"],
            "build_hash": st.session_state["build_hash"]
        }
        
        os4_reports_extended.render(BASE_DIR, config)
        
        # Compléter le run
        if st.session_state.get("gates_result"):
            final_decision = st.session_state["gates_result"].get("decision", "UNKNOWN")
            complete_run(st.session_state["run_id"], final_decision)
            st.session_state["pipeline_status"]["report"] = "completed"
    
    with tab3:
        st.subheader("📤 Exporter les Données")
        
        # Préparer les données pour l'export
        export_data = {
            "domain": st.session_state["domain"],
            "seed": st.session_state["seed"],
            "tau": st.session_state["tau"],
            "decision": st.session_state.get("gates_result", {}).get("decision", "N/A")
        }
        
        if st.session_state.get("features"):
            export_data["features"] = st.session_state["features"]
        
        if st.session_state.get("simulation"):
            export_data["simulation"] = st.session_state["simulation"]
        
        if st.session_state.get("gates_result"):
            export_data["decision"] = st.session_state["gates_result"]
        
        if st.session_state.get("intent_emitted"):
            export_data["intent"] = st.session_state["intent_emitted"]
        
        render_export_buttons(st.session_state["run_id"], export_data)


# ============================================================
# ROUTAGE PRINCIPAL
# ============================================================

def main():
    """Point d'entrée principal."""
    
    # Vérifier l'authentification
    if not is_authenticated():
        render_login_form()
        return
    
    # Rendre la sidebar
    render_sidebar()
    
    # Router vers la page active
    current_page = st.session_state.get("current_page", "accueil")
    
    pages = {
        "accueil": page_accueil,
        "analyse": page_analyse,
        "simulation": page_simulation,
        "decision": page_decision,
        "rapports": page_rapports,
    }
    
    if current_page in pages:
        pages[current_page]()
    else:
        page_accueil()

if __name__ == "__main__":
    main()
