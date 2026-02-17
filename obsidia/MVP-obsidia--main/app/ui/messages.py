"""Professional messaging system for Obsidia interface."""
import streamlit as st

# Professional messages (not tutorial-style)
MESSAGES = {
    "os1_intro": {
        "simplifié": "Analysez les données de marché et calculez les caractéristiques nécessaires pour la simulation.",
        "intermédiaire": "Cette étape extrait les features (volatilité, cohérence, friction) à partir des données de marché. Ces métriques alimenteront la simulation Monte Carlo (OS2).",
        "expert": "**Rôle** : Explorer (séparation des rôles). **Objectif** : Feature extraction pour projection stochastique. **Sortie** : features.json avec volatility, coherence, friction, regime."
    },
    "os2_intro": {
        "simplifié": "Projetez les scénarios futurs possibles via simulation Monte Carlo.",
        "intermédiaire": "La simulation Monte Carlo génère N scénarios stochastiques sur un horizon H. Les métriques clés (μ, CVaR, P(Ruin)) permettent d'évaluer le risque.",
        "expert": "**Méthode** : Monte Carlo avec N scénarios, horizon H steps. **Métriques** : μ (expected return), σ (volatility), CVaR 95%, P(DD > threshold), P(Ruin). **Sortie** : simulation.json."
    },
    "os3_intro": {
        "simplifié": "Évaluez les gates de validation et appliquez la politique ROI.",
        "intermédiaire": "Les 3 gates (Integrity, X-108, Risk) valident la décision. La priorité BLOCK > HOLD > ALLOW s'applique. Le délai τ (X-108) est obligatoire pour actions irréversibles.",
        "expert": "**Gates** : G1 (Integrity), G2 (X-108 Temporal Lock), G3 (Risk Killswitch). **Composition** : max(BLOCK, HOLD, ALLOW). **ROI** : Return on Intent policy. **Sortie** : gates.json + erc8004_intent.json."
    },
    "os4_intro": {
        "simplifié": "Consultez les artefacts générés et exportez les résultats.",
        "intermédiaire": "Tous les artefacts (features, simulation, gates, intent) sont disponibles au format JSON/JSONL. L'export ZIP permet l'audit complet.",
        "expert": "**Artifacts** : features.json, simulation.json, gates.json, erc8004_intent.json, os0_snapshot.json. **Formats** : JSON (structured), JSONL (streaming), ZIP (archive). **Traçabilité** : Run ID + Seed + Build Hash."
    },
    "no_features": {
        "action": "Calculez les features",
        "reason": "Les features sont nécessaires pour la simulation Monte Carlo",
        "link": "OS1 — Exploration"
    },
    "no_simulation": {
        "action": "Exécutez la simulation",
        "reason": "La simulation est nécessaire pour évaluer les gates",
        "link": "OS2 — Simulation"
    },
    "no_gates": {
        "action": "Évaluez les gates",
        "reason": "Les gates sont nécessaires pour émettre un intent",
        "link": "OS3 — Gouvernance"
    }
}

def get_intro_message(os_level: str, detail_level: str = "intermédiaire") -> str:
    """
    Get professional introduction message for an OS level.
    
    Args:
        os_level: OS level (os1, os2, os3, os4)
        detail_level: Level of detail (simplifié, intermédiaire, expert)
    
    Returns:
        Introduction message
    """
    key = f"{os_level}_intro"
    messages = MESSAGES.get(key, {})
    return messages.get(detail_level.lower(), messages.get("intermédiaire", ""))

def render_prerequisite_message(missing: str):
    """
    Render a professional prerequisite message.
    
    Args:
        missing: Missing prerequisite (features, simulation, gates)
    """
    key = f"no_{missing}"
    msg = MESSAGES.get(key, {})
    
    if msg:
        st.error(f"🔒 **Prérequis manquant** : {msg['action']}")
        st.info(f"**Raison** : {msg['reason']}")
        st.markdown(f"👉 Accédez à **{msg['link']}** pour compléter cette étape.")
    else:
        st.warning(f"⚠️ Prérequis manquant : {missing}")

def render_step_objective(step: int, title: str, objective: str):
    """
    Render a professional step objective (not tutorial-style).
    
    Args:
        step: Step number
        title: Step title
        objective: Step objective
    """
    st.markdown(f"## {step}. {title}")
    st.markdown(f"**Objectif** : {objective}")
    st.markdown("---")

def render_success_message(action: str, details: str = ""):
    """
    Render a professional success message.
    
    Args:
        action: Action completed
        details: Optional details
    """
    st.success(f"✅ **{action}** complété avec succès")
    if details:
        st.caption(details)

def render_warning_message(title: str, reason: str, action: str = ""):
    """
    Render a professional warning message.
    
    Args:
        title: Warning title
        reason: Reason for warning
        action: Optional action to take
    """
    st.warning(f"⚠️ **{title}**")
    st.markdown(f"**Raison** : {reason}")
    if action:
        st.markdown(f"**Action recommandée** : {action}")
