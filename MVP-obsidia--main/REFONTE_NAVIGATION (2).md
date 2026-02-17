# Refonte Complète de la Navigation - Obsidia

## 🎯 Objectif

Transformer l'application d'une **démo technique** (avec OS0-OS6, modes Guidé/Expert) en une **application professionnelle** avec une navigation intuitive et une architecture claire.

---

## ❌ Problèmes de l'Ancienne Architecture

### 1. Nomenclature Technique Incompréhensible
```
OS0 — Invariants (Lois)
OS1 — Exploration (Découverte)
OS2 — Simulation (Projection)
OS3 — Gouvernance (Décision)
OS4 — Rapports (Audit)
OS5 — Démo Auto (Scénarios)
OS6 — Tests Stress (Avancé)
```
**Problème** : Un utilisateur métier ne comprend pas "OS1", "OS2"...

### 2. Double Mode Confus
- Toggle "Mode Guidé / Mode Expert" en haut de page
- Deux UX complètement différentes
- L'utilisateur ne sait pas quel mode choisir

### 3. Sidebar Surchargée
```
Navigation:
- 🏠 Dashboard
- 🔍 Analyse
- 📊 Simulation
- ⚖️ Gouvernance
- 📄 Rapports
- 🧪 Stress Tests
- 📊 Domaines

+ Configuration
+ OS Levels (7 options)
```
**Problème** : Trop d'options, certaines redondantes

### 4. Données Fictives
Le Dashboard affichait des données factices :
```python
data = {
    "Run ID": ["#20c88a56", "#1a2b3c4d", "#9f8e7d6c"],  # Faux
    "Decision": ["✅ EXECUTE", "⚠️ HOLD", "✅ EXECUTE"]   # Faux
}
```

### 5. Structure de Démo
- Pages "Stress Tests" et "Domaines" sont des fonctionnalités de démo
- Pas de workflow cohérent entre les étapes
- Navigation possible dans n'importe quel ordre

---

## ✅ Nouvelle Architecture Professionnelle

### Navigation Simplifiée (5 pages)

```
🏠 Accueil
   └── Dashboard opérationnel avec vraies données
   └── Pipeline visuel (4 étapes)
   └── Actions rapides
   └── Status système

🔍 Analyse
   └── Extraction des features (OS1)
   └── Verrouillé tant que pas d'analyse
   └── → Débloque Simulation

🎲 Simulation
   └── Monte Carlo (OS2)
   └── Verrouillé tant que pas d'analyse
   └── → Débloque Décision

⚖️ Décision
   └── Gates + Intent (OS3)
   └── Verrouillé tant que pas de simulation
   └── → Débloque Rapports

📊 Rapports
   └── Audit et export (OS4)
   └── Tous les artefacts
   └── Export ZIP
```

### Workflow Guidé Implicite

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Analyse │───→│Simulation│───→│ Décision│───→│ Rapports│
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     ↑                                        │
     └────────────────────────────────────────┘
              (Nouvelle analyse)
```

Chaque étape débloque la suivante. Pas possible de sauter des étapes.

---

## 📁 Structure des Fichiers

### Avant
```
app/
├── dashboard.py          # Toggle + double mode
├── router.py             # Routage complexe
├── ui/
│   ├── layout.py
│   ├── navigation.py     # Stepper complexe
│   ├── mode_switcher.py  # Toggle Guidé/Expert
│   └── ...
└── views/
    ├── os0_invariants.py
    ├── os1_observation.py
    ├── os2_simulation.py
    ├── os3_governance.py
    ├── os4_reports_extended.py
    ├── os5_autorun.py      # Démo
    ├── os6_exploration.py  # Démo
    ├── guided_workflow.py  # Mode guidé
    └── ... (13 fichiers)
```

### Après
```
app/
├── dashboard_new.py      # Navigation pro (5 pages)
├── config.py             # Configuration
└── views/
    ├── os1_observation.py   # Réutilisé
    ├── os2_simulation.py    # Réutilisé
    ├── os3_governance.py    # Réutilisé
    └── os4_reports_extended.py  # Réutilisé
```

**Supprimé** : 9 fichiers de démo/complexité inutile

---

## 🔧 Changements Techniques

### Session State Simplifié

#### Avant
```python
session_state = {
    "app_mode": "Guidé" or "Expert",  # Complexe
    "guided_step": 1-5,               # Mode guidé
    "current_page": "Dashboard",
    "os_level": "OS0",                # Nomenclature technique
    # ... 20+ clés
}
```

#### Après
```python
session_state = {
    "current_page": "accueil",  # Une seule navigation
    "pipeline_status": {         # Status clair
        "analysis": "pending",   # pending/completed
        "simulation": "locked",  # locked/pending/completed
        "decision": "locked",
        "report": "locked"
    },
    # ... données réelles
}
```

### Sidebar Épurée

#### Avant
```python
with st.sidebar:
    st.title("🏛️ OBSIDIA")
    page = st.radio("Navigation", [
        "🏠 Dashboard", "🔍 Analyse", "📊 Simulation",
        "⚖️ Gouvernance", "📄 Rapports", "🧪 Stress Tests",
        "📊 Domaines"
    ])
    
    with st.expander("🔬 Mode Expert (OS Levels)"):
        os_level = st.radio("OS Level", [
            "OS0 — Invariants", "OS1 — Exploration",
            "OS2 — Simulation", "OS3 — Gouvernance",
            "OS4 — Rapports", "OS5 — Démo Auto",
            "OS6 — Stress"
        ])
```

#### Après
```python
with st.sidebar:
    # Logo
    st.markdown("🏛️ OBSIDIA")
    
    # Navigation simple (5 boutons)
    for page_id, icon, label in pages:
        st.button(f"{icon} {label}", key=f"nav_{page_id}")
    
    # Config essentielle uniquement
    st.selectbox("Domaine", ["Trading", "Medical-AI", ...])
    st.number_input("Seed", ...)
    st.slider("τ (s)", ...)
    
    # Status visuel
    st.markdown("#### 📈 Pipeline")
    st.markdown("✅ Analyse")
    st.markdown("⏳ Simulation")
    st.markdown("🔒 Décision")
```

---

## 📊 Comparaison Visuelle

### Ancien Dashboard (Démo)
```
┌─────────────────────────────────────────────────────────┐
│ [Toggle: Mode Guidé ● Mode Expert]                      │
├─────────────────────────────────────────────────────────┤
│ Dashboard Obsidia                                       │
│                                                         │
│ Run ID  Seed  Délai τ                                   │
│ #20c88a  42   10.0s    ← FAUSSES DONNÉES               │
│                                                         │
│ 📊 Dernières Simulations (FAUSSES)                      │
│ ┌──────────┬──────────┬────────┬──────────┐            │
│ │ #20c88a56│ 2026-... │ 0.5706 │ ✅ EXEC  │            │
│ │ #1a2b3c4d│ 2026-... │ 0.4821 │ ⚠️ HOLD  │            │
│ └──────────┴──────────┴────────┴──────────┘            │
│                                                         │
│ ⚡ Actions Rapides                                      │
│ [Nouvelle Analyse] [Lancer Simu] [Voir Rapports]...    │
└─────────────────────────────────────────────────────────┘
```

### Nouveau Dashboard (Pro)
```
┌─────────────────────────────────────────────────────────┐
│ 🏛️ Obsidia                                    #a3f7b2d  │
│ Plateforme de gouvernance et d'audit                    │
├─────────────────────────────────────────────────────────┤
│ 📊 Pipeline de Gouvernance                              │
│ ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│ │🔍 Analyse│→│🎲 Simu  │→│⚖️ Décis.│→│📊 Rapport│     │
│ │  ⏳     │  │  🔒     │  │  🔒     │  │  🔒     │     │
│ └─────────┘  └─────────┘  └─────────┘  └─────────┘     │
├─────────────────────────────────────────────────────────┤
│ ⚡ Actions Rapides                                      │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│ │🔍 Nouvelle  │ │📊 Voir      │ │⚙️ Configurer│        │
│ │  Analyse    │ │  Rapports   │ │             │        │
│ └─────────────┘ └─────────────┘ └─────────────┘        │
├─────────────────────────────────────────────────────────┤
│ ⚖️ Status Système                                       │
│ Invariants    │ Gates           │ Configuration         │
│ ✅ BLOCK>...  │ ✅ Gate 1       │ 🎯 Trading            │
│ ✅ X-108      │ ✅ Gate 2       │ 🎲 Seed: 42           │
│ ✅ Séparation │ ✅ Gate 3       │ 🔒 τ: 10.0s           │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Comment Migrer

### 1. Tester la Nouvelle Version
```bash
cd MVP-obsidia-
streamlit run app/dashboard_new.py
```

### 2. Remplacer l'Ancien Dashboard
```bash
mv app/dashboard.py app/dashboard_old.py
mv app/dashboard_new.py app/dashboard.py
```

### 3. Nettoyer les Fichiers Inutiles
```bash
# Supprimer les vues de démo
rm app/views/os0_invariants.py
rm app/views/os5_autorun.py
rm app/views/os6_exploration.py
rm app/views/guided_workflow.py
rm app/views/landing_page.py
rm app/views/domain_analytics.py

# Supprimer les UI complexes
rm app/ui/mode_switcher.py
rm app/ui/expert_navigation.py
rm app/ui/console_x108.py
```

---

## ✅ Checklist de Validation

- [ ] Navigation claire (5 pages max)
- [ ] Pas de données fictives
- [ ] Workflow guidé implicite
- [ ] Noms user-friendly (pas OS0, OS1...)
- [ ] Sidebar épurée
- [ ] Un seul mode (pas Guidé/Expert)
- [ ] Status du pipeline visible
- [ ] Étapes verrouillées/débloquées

---

## 🎓 Leçons Apprises

1. **Nommer pour les utilisateurs, pas pour les développeurs**
   - ❌ "OS1 — Exploration (Découverte)"
   - ✅ "Analyse"

2. **Un seul mode de navigation**
   - ❌ Toggle Guidé/Expert
   - ✅ Workflow guidé implicite avec verrous

3. **Montrer le vrai status**
   - ❌ Données fictives
   - ✅ Pipeline status (pending/completed/locked)

4. **Limiter les options**
   - ❌ 7+ options dans la sidebar
   - ✅ 5 pages essentielles
