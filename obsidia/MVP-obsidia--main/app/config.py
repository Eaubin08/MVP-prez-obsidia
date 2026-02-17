"""Configuration globale de l'application Obsidia Unified Interface."""
from pathlib import Path
import os

# Chemins - Compatible Streamlit Cloud et local
if os.path.exists('/mount/src'):
    # Streamlit Cloud
    BASE_DIR = Path('/mount/src/mvp-obsidia-')
else:
    # Local
    BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
TRACES_DIR = BASE_DIR / "traces"
SCENARIOS_DIR = BASE_DIR / "scenarios"
RESOURCES_DIR = BASE_DIR / "resources"

# Créer les répertoires s'ils n'existent pas
TRACES_DIR.mkdir(parents=True, exist_ok=True)
(TRACES_DIR / "last_run").mkdir(parents=True, exist_ok=True)

# Configuration par défaut
DEFAULT_DOMAIN = "Trading (ERC-8004)"
DEFAULT_MODE = "Proof (Deterministic)"
DEFAULT_SEED = 42
DEFAULT_TAU = 10.0  # X-108 temporal lock en secondes

# Domaines disponibles
DOMAINS = [
    "Trading (ERC-8004)",
    "Bank-Robo",
    "Blockchain / Intents",
    "Medical-AI (Santé)",
    "Legal-Contracts (Juridique)",
    "Auto-Drive (Véhicules)",
    "Factory-Control (Industriel)",
    "Unified"
]

# Modes disponibles
MODES = [
    "Proof (Deterministic)",
    "Free (Non-deterministic)"
]

# Niveaux OS (Pipeline)
OS_LEVELS = [
    "OS0 — Invariants (Lois)",
    "OS1 — Exploration (Découverte)",
    "OS2 — Simulation (Projection)",
    "OS3 — Gouvernance (Décision)",
    "OS4 — Rapports (Audit)",
    "OS5 — Démo Auto (Scénarios)",
    "OS6 — Tests Stress (Avancé)"
]

# Build info
BUILD_VERSION = "1.0.0"
BUILD_HASH = "obsi-unified-mvp"
