"""Domain-specific data and scenarios for different application areas."""
import numpy as np
import pandas as pd
from typing import Dict, List

DOMAIN_CONFIGS = {
    "Trading (ERC-8004)": {
        "description": "Trading de cryptomonnaies avec standard ERC-8004",
        "irreversible_threshold": 0.7,
        "default_tau": 10.0,
        "risk_tolerance": "medium",
        "icon": "💰",
        "typical_scenarios": [
            "Achat/Vente de BTC",
            "Arbitrage cross-exchange",
            "Position leverage"
        ]
    },
    "Bank-Robo": {
        "description": "Conseiller bancaire robotisé pour gestion de patrimoine",
        "irreversible_threshold": 0.9,
        "default_tau": 15.0,
        "risk_tolerance": "low",
        "icon": "🏦",
        "typical_scenarios": [
            "Virement important",
            "Ouverture de crédit",
            "Placement long terme"
        ]
    },
    "Blockchain / Intents": {
        "description": "Exécution d'intents blockchain (smart contracts)",
        "irreversible_threshold": 1.0,
        "default_tau": 5.0,
        "risk_tolerance": "high",
        "icon": "⛓️",
        "typical_scenarios": [
            "Déploiement de contrat",
            "Transaction on-chain",
            "Stake/Unstake"
        ]
    },
    "Medical-AI (Santé)": {
        "description": "Aide à la décision médicale (diagnostic, prescription)",
        "irreversible_threshold": 0.95,
        "default_tau": 30.0,
        "risk_tolerance": "very_low",
        "icon": "🏥",
        "typical_scenarios": [
            "Prescription chirurgie",
            "Dosage médicament critique",
            "Arrêt traitement vital"
        ],
        "critical_actions": [
            "PRESCRIBE_SURGERY",
            "MODIFY_CRITICAL_DOSE",
            "STOP_LIFE_SUPPORT"
        ]
    },
    "Legal-Contracts (Juridique)": {
        "description": "Signature et validation de contrats légaux",
        "irreversible_threshold": 0.98,
        "default_tau": 25.0,
        "risk_tolerance": "very_low",
        "icon": "⚖️",
        "typical_scenarios": [
            "Signature contrat immobilier",
            "Accord commercial majeur",
            "Testament"
        ],
        "critical_actions": [
            "SIGN_CONTRACT",
            "VALIDATE_AGREEMENT",
            "EXECUTE_WILL"
        ]
    },
    "Auto-Drive (Véhicules)": {
        "description": "Véhicules autonomes - décisions de conduite",
        "irreversible_threshold": 0.6,
        "default_tau": 2.0,
        "risk_tolerance": "medium",
        "icon": "🚗",
        "typical_scenarios": [
            "Changement de voie d'urgence",
            "Freinage automatique",
            "Dépassement"
        ],
        "critical_actions": [
            "EMERGENCY_BRAKE",
            "LANE_CHANGE_URGENT",
            "OVERTAKE"
        ]
    },
    "Factory-Control (Industriel)": {
        "description": "Contrôle de lignes de production industrielles",
        "irreversible_threshold": 0.85,
        "default_tau": 20.0,
        "risk_tolerance": "low",
        "icon": "🏭",
        "typical_scenarios": [
            "Arrêt d'urgence ligne",
            "Changement de recette",
            "Maintenance préventive"
        ],
        "critical_actions": [
            "EMERGENCY_SHUTDOWN",
            "CHANGE_RECIPE",
            "START_MAINTENANCE"
        ]
    },
    "Unified": {
        "description": "Mode unifié multi-domaines",
        "irreversible_threshold": 0.8,
        "default_tau": 10.0,
        "risk_tolerance": "medium",
        "icon": "🌐",
        "typical_scenarios": [
            "Scénario générique"
        ]
    }
}

def get_domain_config(domain: str) -> Dict:
    """Retourne la configuration d'un domaine."""
    return DOMAIN_CONFIGS.get(domain, DOMAIN_CONFIGS["Unified"])

def generate_domain_specific_data(domain: str, seed: int = 42) -> pd.DataFrame:
    """Génère des données synthétiques adaptées au domaine."""
    np.random.seed(seed)
    
    config = get_domain_config(domain)
    
    # Paramètres selon le domaine
    if "Medical" in domain:
        # Données médicales: stabilité élevée, peu de volatilité
        n_points = 100
        base = 98.0  # Température corporelle baseline
        volatility = 0.5
        trend = 0.01
    elif "Legal" in domain:
        # Données juridiques: très stable, presque constant
        n_points = 50
        base = 100.0
        volatility = 0.1
        trend = 0.0
    elif "Auto-Drive" in domain:
        # Données véhicules: haute fréquence, réactivité
        n_points = 200
        base = 50.0  # Vitesse baseline
        volatility = 5.0
        trend = 0.05
    elif "Factory" in domain:
        # Données industrielles: cycles réguliers
        n_points = 150
        base = 1000.0  # Production baseline
        volatility = 20.0
        trend = 0.02
    else:
        # Trading / Blockchain / Bank: volatilité moyenne
        n_points = 100
        base = 50000.0
        volatility = 1000.0
        trend = 0.03
    
    # Générer les données
    timestamps = pd.date_range(start='2024-01-01', periods=n_points, freq='1H')
    
    # Prix avec tendance et bruit
    prices = []
    price = base
    for i in range(n_points):
        price += np.random.normal(trend * price, volatility)
        prices.append(max(price, 0.01))  # Éviter les valeurs négatives
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'close': prices
    })
    
    return df

def get_domain_critical_threshold(domain: str) -> float:
    """Retourne le seuil de criticité pour un domaine."""
    config = get_domain_config(domain)
    return config.get("irreversible_threshold", 0.8)

def get_domain_recommended_tau(domain: str) -> float:
    """Retourne le τ recommandé pour un domaine."""
    config = get_domain_config(domain)
    return config.get("default_tau", 10.0)

def get_domain_scenarios(domain: str) -> List[str]:
    """Retourne les scénarios typiques d'un domaine."""
    config = get_domain_config(domain)
    return config.get("typical_scenarios", [])

def get_domain_description(domain: str) -> str:
    """Retourne la description d'un domaine."""
    config = get_domain_config(domain)
    icon = config.get("icon", "🌐")
    desc = config.get("description", "")
    return f"{icon} {desc}"

def is_action_critical(domain: str, action: str) -> bool:
    """Vérifie si une action est critique dans un domaine."""
    config = get_domain_config(domain)
    critical_actions = config.get("critical_actions", [])
    return action.upper() in critical_actions
