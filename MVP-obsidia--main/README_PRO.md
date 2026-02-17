# Obsidia Pro - Gouvernance Transparente IA

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red)

Application professionnelle de gouvernance et d'audit pour agents autonomes de trading.

---

## 🚀 Nouveautés de la Version Pro

### ✅ Base de Données SQLite
- **Historique complet** des runs avec traçabilité
- **Stockage persistant** des features, simulations, décisions et intents
- **Statistiques globales** et métriques d'utilisation

### 🔐 Authentification Utilisateurs
- **Système de login** avec hashage des mots de passe
- **Rôles** : utilisateur et administrateur
- **Sessions** sécurisées avec gestion des déconnexions

### 📧 Notifications Email
- **Alertes automatiques** lors d'une décision EXECUTE
- **Templates HTML** professionnels
- **Configuration SMTP** personnalisable

### 📤 Exports Multi-Formats
- **Excel (.xlsx)** : Rapports détaillés avec feuilles multiples
- **PDF (.pdf)** : Rapports formatés pour impression
- **JSON (.json)** : Export des données brutes

---

## 📁 Structure du Projet

```
MVP-obsidia-
├── app/
│   ├── dashboard.py          # Point d'entrée principal
│   ├── config.py             # Configuration globale
│   ├── database.py           # Module base de données SQLite
│   ├── auth.py               # Module d'authentification
│   ├── notifications.py      # Module notifications email
│   ├── exporters.py          # Module exports PDF/Excel/JSON
│   ├── ui/                   # Composants UI
│   │   ├── layout.py
│   │   ├── navigation.py
│   │   ├── header.py
│   │   └── styles.py
│   └── views/                # Vues des pages
│       ├── os1_observation.py
│       ├── os2_simulation.py
│       ├── os3_governance.py
│       └── os4_reports_extended.py
├── data/
│   ├── trading/
│   │   └── BTC_1h.csv
│   └── obsidia.db            # Base de données SQLite
├── scenarios/
│   └── deterministic/
│       └── trading_scenarios.json
├── requirements.txt
├── migrate_to_pro.py         # Script de migration
└── README_PRO.md
```

---

## 🛠️ Installation

### 1. Cloner le Repository

```bash
git clone https://github.com/Eaubin08/MVP-obsidia-.git
cd MVP-obsidia-
```

### 2. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer l'Application

```bash
streamlit run app/dashboard.py
```

L'application sera accessible sur `http://localhost:8501`

---

## 🔐 Authentification

### Compte par Défaut

| Champ | Valeur |
|-------|--------|
| Nom d'utilisateur | `admin` |
| Mot de passe | `admin123` |
| Rôle | `admin` |

### Créer un Nouvel Utilisateur (Admin)

1. Connectez-vous avec le compte admin
2. Allez dans **Paramètres > Utilisateurs**
3. Remplissez le formulaire d'inscription

---

## 📊 Pipeline de Gouvernance

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Analyse │───→│Simulation│───→│ Décision│───→│ Rapports│
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     ↑                                        │
     └────────────────────────────────────────┘
              (Nouvelle analyse)
```

### 1. Analyse (OS1)
- Extraction des features du marché
- Calcul de Volatility, Coherence, Friction, Regime
- Sauvegarde automatique dans la base de données

### 2. Simulation (OS2)
- Projection Monte Carlo (200 simulations)
- Calcul de μ, σ, P(ruin), P(DD), CVaR_95
- Verdict : OK / UNCERTAIN / DESTRUCTIVE

### 3. Décision (OS3)
- Évaluation des 3 gates : Integrity, X-108, Risk
- Décision : BLOCK / HOLD / EXECUTE
- Émission d'intent ERC-8004 si EXECUTE

### 4. Rapports (OS4)
- Consultation de l'historique
- Export PDF/Excel/JSON
- Audit complet avec traçabilité

---

## 📧 Configuration des Notifications Email

### 1. Configurer SMTP

Allez dans **Paramètres > Notifications** et renseignez :

```
Serveur SMTP: smtp.gmail.com
Port: 587
Nom d'utilisateur: votre-email@gmail.com
Mot de passe: votre-mot-de-passe-app
Email expéditeur: notifications@obsidia.local
```

### 2. Test d'Envoi

Utilisez le bouton "Envoyer un email de test" pour vérifier la configuration.

### 3. Notifications Automatiques

Les notifications sont envoyées automatiquement lors d'une décision **EXECUTE**.

---

## 📤 Formats d'Export

### Excel (.xlsx)
- Feuille "Informations" : Métadonnées du run
- Feuille "Features" : Caractéristiques du marché
- Feuille "Simulation" : Résultats Monte Carlo
- Feuille "Décision" : Évaluation des gates
- Feuille "Intent" : Détails de l'intent ERC-8004

### PDF (.pdf)
- Rapport formaté avec en-tête et pied de page
- Tableaux colorés par section
- Décision mise en évidence

### JSON (.json)
- Export brut des données
- Format machine-readable
- Idéal pour l'intégration API

---

## 🗄️ Schéma de la Base de Données

### Tables Principales

```sql
-- Utilisateurs
users (id, username, email, password_hash, role, created_at, last_login, is_active)

-- Runs
runs (id, run_id, user_id, domain, seed, tau, status, started_at, completed_at, final_decision)

-- Features
features (id, run_id, volatility, coherence, friction, regime, computed_at)

-- Simulations
simulations (id, run_id, mu, sigma, p_ruin, p_dd, cvar_95, verdict, n_sims, horizon, computed_at)

-- Décisions
decisions (id, run_id, gate1_ok, gate1_reason, gate2_ok, gate2_reason, 
           gate3_ok, gate3_reason, final_decision, decision_reason, decided_at)

-- Intents
intents (id, run_id, asset, side, amount, irreversible, timestamp, metadata, created_at)

-- Notifications
notifications (id, user_id, run_id, type, message, is_read, sent_at)
```

---

## 🔧 Migration depuis l'Ancienne Version

Si vous avez une ancienne version de l'application :

```bash
python migrate_to_pro.py
```

Ce script va :
1. Sauvegarder vos fichiers existants
2. Installer le nouveau dashboard Pro
3. Supprimer les fichiers inutiles
4. Initialiser la base de données

---

## 📊 Statistiques et Métriques

L'application collecte automatiquement :

- **Nombre total de runs**
- **Nombre d'utilisateurs**
- **Runs par jour**
- **Répartition des décisions** (EXECUTE / HOLD / BLOCK)
- **Dernier run** et sa décision

---

## 🛡️ Sécurité

- **Hashage SHA-256** des mots de passe
- **Sessions** avec validation côté serveur
- **Contrôle d'accès** par rôles (user/admin)
- **Séparation des données** par utilisateur

---

## 📝 Changelog

### v2.0.0 - Obsidia Pro
- ✅ Base de données SQLite avec historique complet
- ✅ Système d'authentification utilisateurs
- ✅ Notifications email configurables
- ✅ Exports PDF, Excel et JSON
- ✅ Interface professionnelle avec workflow guidé
- ✅ Statistiques globales et métriques

### v1.0.0 - Version Initiale
- Pipeline OS0-OS4
- Visualisations Plotly
- Human Algebra
- Scénarios déterministes

---

## 🤝 Contribution

Ce projet est développé dans le cadre d'un hackathon. Pour toute question ou suggestion :

1. Ouvrez une issue sur GitHub
2. Décrivez le problème ou la fonctionnalité souhaitée
3. Soumettez une pull request si vous avez une solution

---

## 📄 Licence

Ce projet est fourni tel quel à des fins de démonstration.

---

## 👤 Auteur

**Eaubin08**

- GitHub: [@Eaubin08](https://github.com/Eaubin08)

---

<p align="center">
  <strong>🏛️ Obsidia - Gouvernance Transparente IA</strong><br>
  <em>Sécurité, Traçabilité, Robustesse</em>
</p>
