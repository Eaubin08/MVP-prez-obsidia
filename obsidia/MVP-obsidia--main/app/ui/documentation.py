"""Documentation components with detailed explanations."""
import streamlit as st

def render_detail_level_selector():
    """Render detail level selector in sidebar."""
    with st.sidebar.expander("⚙️ Préférences d'affichage", expanded=False):
        detail_level = st.radio(
            "Niveau de détail",
            ["Simplifié", "Intermédiaire", "Expert"],
            index=1,
            help="Choisissez le niveau de détail des explications"
        )
        st.session_state["detail_level"] = detail_level
        
        st.caption("💡 **Simplifié** : Explications courtes et visuelles")
        st.caption("📚 **Intermédiaire** : Équilibre entre clarté et profondeur")
        st.caption("🔬 **Expert** : Détails techniques complets")
    
    return st.session_state.get("detail_level", "Intermédiaire")

def render_core_laws_detailed():
    """Render detailed core laws documentation."""
    detail_level = st.session_state.get("detail_level", "Intermédiaire")
    
    with st.expander("📚 En savoir plus sur les lois fondamentales", expanded=False):
        st.markdown("### 🔒 Core Laws (Version Détaillée)")
        
        # X-108 Temporal Lock
        st.markdown("#### 1️⃣ X-108 Temporal Lock")
        
        if detail_level == "Simplifié":
            st.info("⏱️ **Attendre τ secondes avant toute action irréversible**")
            st.caption("Empêche les décisions précipitées et permet une période de réflexion.")
        
        elif detail_level == "Intermédiaire":
            st.markdown("""
            **Principe** : Délai **obligatoire** de τ secondes avant toute action **irréversible**.
            
            **Pourquoi ?** Empêche l'anticipation et permet une période de réflexion.
            
            **Exemple concret** :
            - Intent: "Vendre 100 BTC" (irreversible=true)
            - Système: HOLD pendant τ=10s
            - Après 10s: Si pas annulé → ACT (exécution)
            """)
        
        else:  # Expert
            st.markdown("""
            **Principe** : Délai **obligatoire** de τ secondes avant toute action **irréversible**.
            
            **Pourquoi ?** Empêche l'anticipation et permet une période de réflexion.
            
            **Exemple concret** :
            - Intent: "Vendre 100 BTC" (irreversible=true)
            - Système: HOLD pendant τ=10s
            - Après 10s: Si pas annulé → ACT (exécution)
            
            **Violations détectées** :
            - **V-T1** : Tentative d'action avant τ
            - **V-T2** : Modification de t0 (horodatage)
            - **V-T3** : Clock skew (horloge désynchronisée)
            
            **Implémentation** :
            ```python
            if intent["irreversible"] and (t_now - t0) < tau:
                return {"decision": "HOLD", "reason": "x108_temporal_lock"}
            ```
            """)
        
        st.markdown("---")
        
        # Gate Priority
        st.markdown("#### 2️⃣ Gate Priority : BLOCK > HOLD > ALLOW")
        
        if detail_level == "Simplifié":
            st.info("🚦 **Priorité stricte** : BLOCK (rouge) > HOLD (orange) > ALLOW (vert)")
            st.caption("Si un gate dit BLOCK, toute la décision est BLOCK.")
        
        elif detail_level == "Intermédiaire":
            st.markdown("""
            **Principe** : Composition stricte des décisions des gates.
            
            **Ordre de priorité** :
            1. **BLOCK** : Refus absolu (risque inacceptable)
            2. **HOLD** : Attente requise (X-108 ou autre condition)
            3. **ALLOW** : Autorisation (tous les gates passent)
            
            **Exemple** :
            - Gate1: ALLOW
            - Gate2: HOLD
            - Gate3: ALLOW
            - **Décision finale** : HOLD (priorité sur ALLOW)
            """)
        
        else:  # Expert
            st.markdown("""
            **Principe** : Composition stricte des décisions des gates.
            
            **Ordre de priorité** :
            1. **BLOCK** : Refus absolu (risque inacceptable)
            2. **HOLD** : Attente requise (X-108 ou autre condition)
            3. **ALLOW** : Autorisation (tous les gates passent)
            
            **Exemple** :
            - Gate1: ALLOW
            - Gate2: HOLD
            - Gate3: ALLOW
            - **Décision finale** : HOLD (priorité sur ALLOW)
            
            **Implémentation** :
            ```python
            def compose_gates(gates):
                if any(g["decision"] == "BLOCK" for g in gates):
                    return "BLOCK"
                elif any(g["decision"] == "HOLD" for g in gates):
                    return "HOLD"
                else:
                    return "ALLOW"
            ```
            
            **Propriété mathématique** :
            - Associative : (G1 ⊕ G2) ⊕ G3 = G1 ⊕ (G2 ⊕ G3)
            - Commutative : G1 ⊕ G2 = G2 ⊕ G1
            - Idempotente : G ⊕ G = G
            """)
        
        st.markdown("---")
        
        # Irreversibility Flag
        st.markdown("#### 3️⃣ Irreversibility Flag")
        
        if detail_level == "Simplifié":
            st.info("🔴 **Si irreversible=true** → X-108 s'applique automatiquement")
        
        elif detail_level == "Intermédiaire":
            st.markdown("""
            **Principe** : Toute action marquée comme irréversible **doit** passer par X-108.
            
            **Actions irréversibles typiques** :
            - Vente d'actifs
            - Signature de contrat
            - Prescription médicale
            - Freinage d'urgence (véhicule)
            
            **Actions réversibles** :
            - Lecture de données
            - Calcul de features
            - Simulation (pas d'exécution réelle)
            """)
        
        else:  # Expert
            st.markdown("""
            **Principe** : Toute action marquée comme irréversible **doit** passer par X-108.
            
            **Actions irréversibles typiques** :
            - Vente d'actifs
            - Signature de contrat
            - Prescription médicale
            - Freinage d'urgence (véhicule)
            
            **Actions réversibles** :
            - Lecture de données
            - Calcul de features
            - Simulation (pas d'exécution réelle)
            
            **Critères d'irréversibilité** :
            1. **Modification d'état externe** (blockchain, base de données, monde physique)
            2. **Impact financier** (perte d'argent possible)
            3. **Impact humain** (santé, sécurité)
            4. **Impact juridique** (engagement contractuel)
            
            **Implémentation** :
            ```python
            if intent["irreversible"]:
                # X-108 MUST apply
                if not x108_passed(intent, tau):
                    return {"decision": "HOLD", "reason": "x108_required"}
            ```
            """)
        
        st.markdown("---")
        
        # Role Separation
        st.markdown("#### 4️⃣ Role Separation")
        
        if detail_level == "Simplifié":
            st.info("👥 **Séparation des rôles** : Explorer ≠ Executor ≠ Roi")
            st.caption("Aucun composant ne peut contourner les autres.")
        
        elif detail_level == "Intermédiaire":
            st.markdown("""
            **Principe** : Séparation stricte des responsabilités.
            
            **Rôles** :
            - **Explorer** (OS1) : Observe et calcule les features
            - **Simulator** (OS2) : Projette les scénarios futurs
            - **Gates** (OS3) : Évalue les risques et contraintes
            - **Roi** (OS3) : Décide de l'action finale
            - **Executor** (hors scope) : Exécute l'action réelle
            
            **Aucun bypass possible** : Chaque étape est obligatoire.
            """)
        
        else:  # Expert
            st.markdown("""
            **Principe** : Séparation stricte des responsabilités.
            
            **Rôles** :
            - **Explorer** (OS1) : Observe et calcule les features
            - **Simulator** (OS2) : Projette les scénarios futurs
            - **Gates** (OS3) : Évalue les risques et contraintes
            - **Roi** (OS3) : Décide de l'action finale
            - **Executor** (hors scope) : Exécute l'action réelle
            
            **Aucun bypass possible** : Chaque étape est obligatoire.
            
            **Violations détectées** :
            - **V-R1** : Executor appelle directement Explorer (bypass Gates)
            - **V-R2** : Roi modifie les features (bypass Explorer)
            - **V-R3** : Gates modifie l'intent (bypass Roi)
            
            **Implémentation** :
            - Chaque composant est un module séparé
            - Communication via artifacts JSON (read-only)
            - Aucun état partagé mutable
            - Traçabilité complète via JSONL logs
            """)
        
        st.markdown("---")
        
        # Non-Anticipation
        st.markdown("#### 5️⃣ Non-Anticipation")
        
        if detail_level == "Simplifié":
            st.info("⏳ **ACT interdit avant τ** : Pas de décision anticipée")
        
        elif detail_level == "Intermédiaire":
            st.markdown("""
            **Principe** : Aucune action ne peut être exécutée **avant** l'expiration du délai τ.
            
            **Pourquoi ?** Empêche les systèmes d'anticiper les décisions humaines.
            
            **Exemple** :
            - t0 = 10:00:00 (intent soumis)
            - τ = 10s
            - **ACT possible** : t >= 10:00:10
            - **ACT interdit** : t < 10:00:10
            """)
        
        else:  # Expert
            st.markdown("""
            **Principe** : Aucune action ne peut être exécutée **avant** l'expiration du délai τ.
            
            **Pourquoi ?** Empêche les systèmes d'anticiper les décisions humaines.
            
            **Exemple** :
            - t0 = 10:00:00 (intent soumis)
            - τ = 10s
            - **ACT possible** : t >= 10:00:10
            - **ACT interdit** : t < 10:00:10
            
            **Violations détectées** :
            - **V-NA1** : ACT avant τ (anticipation)
            - **V-NA2** : Modification de t0 pour contourner τ
            - **V-NA3** : Clock skew > tolérance
            
            **Implémentation** :
            ```python
            def check_non_anticipation(t0, t_now, tau):
                elapsed = t_now - t0
                if elapsed < tau:
                    return {"ok": False, "reason": "non_anticipation_violated"}
                return {"ok": True}
            ```
            
            **Propriété temporelle** :
            - ∀ intent irréversible, ∃ τ > 0 tel que ACT(t) ⇒ t >= t0 + τ
            """)

def render_feature_explanation(feature_name: str, value: float):
    """Render detailed explanation for a specific feature."""
    detail_level = st.session_state.get("detail_level", "Intermédiaire")
    
    explanations = {
        "volatility": {
            "Simplifié": f"📊 Volatilité = {value:.3f} → {'Élevée' if value > 0.3 else 'Faible'}",
            "Intermédiaire": f"📊 **Volatilité** : {value:.3f}\n\nMesure l'instabilité du marché. > 0.3 = risque élevé.",
            "Expert": f"📊 **Volatilité** : {value:.3f}\n\nÉcart-type des returns sur fenêtre glissante. Formule : σ = sqrt(E[(r - μ)²])\n\n> 0.3 = régime volatile → BLOCK recommandé"
        },
        "coherence": {
            "Simplifié": f"🔗 Cohérence = {value:.3f} → {'Bonne' if value > 0.5 else 'Faible'}",
            "Intermédiaire": f"🔗 **Cohérence** : {value:.3f}\n\nMesure la prévisibilité. > 0.5 = marché cohérent.",
            "Expert": f"🔗 **Cohérence** : {value:.3f}\n\nAutocorrélation des returns. Formule : ρ(k) = Cov(r_t, r_{t-k}) / Var(r)\n\n< 0.3 = marché chaotique → BLOCK"
        },
        "friction": {
            "Simplifié": f"⚡ Friction = {value:.3f} → {'Élevée' if value > 0.5 else 'Faible'}",
            "Intermédiaire": f"⚡ **Friction** : {value:.3f}\n\nRésistance au changement. > 0.5 = marché lent.",
            "Expert": f"⚡ **Friction** : {value:.3f}\n\nInertie du marché. Formule : f = 1 - |Δr| / σ\n\n> 0.7 = marché figé → Risque de gap"
        }
    }
    
    return explanations.get(feature_name, {}).get(detail_level, f"{feature_name} = {value}")
