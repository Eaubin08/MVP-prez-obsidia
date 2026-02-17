"""Module de gestion des scénarios déterministes (Proof Mode)."""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

def load_scenarios(base_dir: Path, domain: str = "trading") -> List[Dict[str, Any]]:
    """Charge les scénarios déterministes pour un domaine donné."""
    scenarios_file = base_dir / "scenarios" / "deterministic" / f"{domain}_scenarios.json"
    
    if not scenarios_file.exists():
        return []
    
    with open(scenarios_file, "r", encoding="utf-8") as f:
        return json.load(f)

def get_scenario_by_id(scenarios: List[Dict[str, Any]], scenario_id: str) -> Optional[Dict[str, Any]]:
    """Récupère un scénario par son ID."""
    for s in scenarios:
        if s.get("id") == scenario_id:
            return s
    return None

def apply_scenario(scenario: Dict[str, Any]) -> Dict[str, Any]:
    """Applique un scénario et retourne les paramètres configurés."""
    return {
        "seed": scenario.get("seed", 42),
        "intent": scenario.get("intent", {}),
        "market_conditions": scenario.get("market_conditions", {}),
        "time_elapsed": scenario.get("time_elapsed", 0.0),
        "tau": scenario.get("tau", 10.0),
        "simulation_override": scenario.get("simulation_override"),
        "expected_decision": scenario.get("expected_decision"),
        "expected_reason": scenario.get("expected_reason")
    }
