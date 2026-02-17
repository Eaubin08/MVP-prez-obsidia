"""Layout components for the Obsidia Unified Interface."""
import streamlit as st
from datetime import datetime

def header(run_id: str, domain: str, mode: str, build_hash: str):
    """Affiche le header principal avec les informations de contexte."""
    st.markdown("### Obsidia Unified Interface")
    st.caption(
        f"Run: `{run_id}` • Domain: `{domain}` • Mode: `{mode}` • Build: `{build_hash}` • "
        f"Time: {datetime.now().strftime('%H:%M:%S')}"
    )

def invariant_panel():
    """Affiche le panneau des invariants dans la sidebar."""
    from app.ui.documentation import render_detail_level_selector
    
    # Sélecteur de niveau de détail
    detail_level = render_detail_level_selector()
    
    with st.sidebar.expander("⚖️ Lois Fondamentales (Invariants)", expanded=False):
        if detail_level == "Simplifié":
            st.markdown("**🔒 Lois du Système:**")
            st.markdown("- Priorité: **BLOCK > HOLD > ALLOW**")
            st.markdown("- X-108: **HOLD→ACT** pour intents irréversibles")
            st.markdown("- Séparation: **Exploration ≠ Action**")
            st.markdown("- Non-anticipation: **ACT INTERDIT avant τ**")
        elif detail_level == "Intermédiaire":
            st.markdown("**🔒 Lois du Système:**")
            st.markdown("- **Priorité**: BLOCK > HOLD > ALLOW (composition stricte)")
            st.markdown("- **X-108**: Délai τ obligatoire pour actions irréversibles")
            st.markdown("- **Séparation**: Explorer ≠ Executor ≠ Roi (aucun bypass)")
            st.markdown("- **Non-anticipation**: ACT INTERDIT avant τ secondes")
            st.markdown("- **Irréversibilité**: Si irreversible=true ⇒ X-108 s'applique")
        else:  # Expert
            st.markdown("**🔒 Core Laws (Version Expert):**")
            st.markdown("""
            1. **X-108 Temporal Lock**: ∀ intent irréversible, ∃ τ > 0 tel que ACT(t) ⇒ t ≥ t0 + τ
            2. **Gate Priority**: compose(gates) = max(BLOCK, HOLD, ALLOW) avec BLOCK > HOLD > ALLOW
            3. **Irreversibility Flag**: irreversible=true ⇒ X-108 MUST apply
            4. **Role Separation**: Explorer ≠ Executor ≠ Roi (no bypass, full traceability)
            5. **Non-Anticipation**: ACT MUST NOT occur before τ seconds elapsed
            """)
        
        st.markdown("---")
        st.markdown("**💡 Rappel:**")
        st.caption("Ces lois sont **non-négociables** et s'appliquent à tous les niveaux OS.")
        
        if detail_level != "Simplifié":
            st.caption("📚 Pour plus de détails, consultez la documentation complète dans OS0 ou OS4.")

def sidebar_controls():
    """Affiche les contrôles globaux dans la sidebar."""
    st.sidebar.title("🏛️ Console de Contrôle")
    
    from app.config import MODES, DOMAINS, DEFAULT_SEED, DEFAULT_TAU, BASE_DIR
    from src.scenarios import load_scenarios
    from src.console_lock import is_console_locked, render_lock_message, render_change_warning
    
    # Vérifier si en mode guidé
    is_guided = st.session_state.get("app_mode") == "guided"
    
    # Warning si config changée
    if is_guided:
        render_change_warning()
    
    # Section Configuration
    config_locked = is_console_locked("config")
    with st.sidebar.expander("⚙️ Configuration Générale", expanded=not config_locked):
        if config_locked:
            render_lock_message("config")
            # Afficher config actuelle en lecture seule
            st.caption(f"🎭 Mode: {st.session_state.get('mode', 'Free')}")
            st.caption(f"🎯 Domaine: {st.session_state.get('domain', 'Trading')}")
        else:
            mode = st.selectbox("🎭 Mode d'exécution", MODES, index=0, 
                               help="Proof: Scénarios déterministes pour validation | Free: Exploration libre")
            domain = st.selectbox("🎯 Domaine d'application", DOMAINS, index=0,
                                 help="Sélectionnez le domaine métier à analyser")
    
    # Scenario picker (Proof Mode only)
    selected_scenario = None
    scenarios_locked = is_console_locked("scenarios")
    
    if not config_locked:  # Si config pas locked, on peut avoir le mode
        mode_val = mode
    else:
        mode_val = st.session_state.get("mode", "Free")
    
    if mode_val.startswith("Proof"):
        with st.sidebar.expander("🎯 Scénarios de Test", expanded=False):
            if scenarios_locked:
                render_lock_message("scenarios")
                if "selected_scenario" in st.session_state:
                    st.caption(f"✅ Scénario: {st.session_state['selected_scenario'].get('name', 'Aucun')}")
            else:
                scenarios = load_scenarios(BASE_DIR, "trading")
                if scenarios:
                    scenario_names = ["(Aucun)"] + [f"{s['id']}: {s['name']}" for s in scenarios]
                    scenario_choice = st.selectbox("Choisir un scénario", scenario_names, index=0,
                                                  help="Scénarios prédéfinis pour tests de validation")
                    
                    if scenario_choice != "(Aucun)":
                        scenario_id = scenario_choice.split(":")[0]
                        selected_scenario = next((s for s in scenarios if s["id"] == scenario_id), None)
                        
                        if selected_scenario:
                            st.info(f"✅ {selected_scenario['description']}")
    
    # Section Paramètres
    temporal_locked = is_console_locked("temporal")
    with st.sidebar.expander("⏱️ Paramètres Temporels & Aléatoires", expanded=not temporal_locked):
        if temporal_locked:
            render_lock_message("temporal")
            st.caption(f"🎲 Seed: {st.session_state.get('seed', DEFAULT_SEED)}")
            st.caption(f"🔒 τ: {st.session_state.get('tau', DEFAULT_TAU)}s")
            seed = st.session_state.get("seed", DEFAULT_SEED)
            tau = st.session_state.get("tau", DEFAULT_TAU)
        else:
            seed = st.number_input("🎲 Graine aléatoire", min_value=0, value=DEFAULT_SEED, step=1,
                                  help="Pour reproduire exactement les mêmes résultats")
            tau = st.slider("🔒 Délai de sécurité τ (secondes)", 1.0, 30.0, DEFAULT_TAU, 1.0,
                           help="Temps d'attente obligatoire avant action irréversible (X-108)")
    
    # Retourner config (locked ou non)
    if config_locked:
        mode = st.session_state.get("mode", "Free")
        domain = st.session_state.get("domain", "Trading")
    
    return {
        "mode": mode,
        "domain": domain,
        "seed": int(seed),
        "tau": float(tau),
        "nondeterministic": mode.startswith("Free"),
        "selected_scenario": selected_scenario
    }
