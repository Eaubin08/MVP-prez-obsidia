"""Générateur de scénarios non-déterministes pour exploration."""
import numpy as np
from typing import Dict, Any, List

class ScenarioGenerator:
    """Génère des scénarios de marché aléatoires mais réalistes."""
    
    REGIMES = ["crash", "bear", "range", "bull", "pump"]
    ASSETS = ["BTC", "ETH", "SOL", "MATIC"]
    SIDES = ["BUY", "SELL"]
    
    def __init__(self, seed: int = None):
        """Initialise le générateur avec une seed optionnelle."""
        self.rng = np.random.RandomState(seed)
    
    def generate_market_crash(self) -> Dict[str, Any]:
        """Génère un scénario de crash de marché."""
        return {
            "id": f"crash_{self.rng.randint(1000, 9999)}",
            "name": "Market Crash",
            "description": "Extreme volatility with rapid price decline",
            "market_conditions": {
                "volatility": self.rng.uniform(0.45, 0.70),
                "coherence": self.rng.uniform(0.10, 0.30),
                "friction": self.rng.uniform(0.50, 0.80),
                "regime": "crash"
            },
            "intent": {
                "asset": self.rng.choice(self.ASSETS),
                "side": "SELL",
                "amount": self.rng.uniform(500, 5000),
                "irreversible": True
            },
            "expected_decision": "BLOCK",
            "expected_reason": "High volatility + Low coherence"
        }
    
    def generate_bull_market(self) -> Dict[str, Any]:
        """Génère un scénario de marché haussier."""
        return {
            "id": f"bull_{self.rng.randint(1000, 9999)}",
            "name": "Bull Market",
            "description": "Strong uptrend with high confidence",
            "market_conditions": {
                "volatility": self.rng.uniform(0.05, 0.15),
                "coherence": self.rng.uniform(0.70, 0.90),
                "friction": self.rng.uniform(0.05, 0.15),
                "regime": "bull"
            },
            "intent": {
                "asset": self.rng.choice(self.ASSETS),
                "side": "BUY",
                "amount": self.rng.uniform(100, 1000),
                "irreversible": True
            },
            "expected_decision": "EXECUTE",
            "expected_reason": "Favorable conditions"
        }
    
    def generate_range_market(self) -> Dict[str, Any]:
        """Génère un scénario de marché latéral."""
        return {
            "id": f"range_{self.rng.randint(1000, 9999)}",
            "name": "Range-Bound Market",
            "description": "Sideways movement with mixed signals",
            "market_conditions": {
                "volatility": self.rng.uniform(0.20, 0.35),
                "coherence": self.rng.uniform(0.35, 0.55),
                "friction": self.rng.uniform(0.25, 0.40),
                "regime": "range"
            },
            "intent": {
                "asset": self.rng.choice(self.ASSETS),
                "side": self.rng.choice(self.SIDES),
                "amount": self.rng.uniform(200, 800),
                "irreversible": True
            },
            "expected_decision": "HOLD",
            "expected_reason": "Uncertain conditions, X-108 required"
        }
    
    def generate_pump_scenario(self) -> Dict[str, Any]:
        """Génère un scénario de pump (montée rapide)."""
        return {
            "id": f"pump_{self.rng.randint(1000, 9999)}",
            "name": "Pump (Rapid Rise)",
            "description": "Sudden price surge with high volatility",
            "market_conditions": {
                "volatility": self.rng.uniform(0.40, 0.60),
                "coherence": self.rng.uniform(0.20, 0.40),
                "friction": self.rng.uniform(0.30, 0.50),
                "regime": "pump"
            },
            "intent": {
                "asset": self.rng.choice(self.ASSETS),
                "side": "BUY",
                "amount": self.rng.uniform(1000, 3000),
                "irreversible": True
            },
            "expected_decision": "BLOCK",
            "expected_reason": "High volatility despite upward movement"
        }
    
    def generate_bear_market(self) -> Dict[str, Any]:
        """Génère un scénario de marché baissier."""
        return {
            "id": f"bear_{self.rng.randint(1000, 9999)}",
            "name": "Bear Market",
            "description": "Sustained downtrend with moderate volatility",
            "market_conditions": {
                "volatility": self.rng.uniform(0.25, 0.40),
                "coherence": self.rng.uniform(0.50, 0.70),
                "friction": self.rng.uniform(0.20, 0.35),
                "regime": "bear"
            },
            "intent": {
                "asset": self.rng.choice(self.ASSETS),
                "side": "SELL",
                "amount": self.rng.uniform(300, 1500),
                "irreversible": True
            },
            "expected_decision": "HOLD",
            "expected_reason": "Bearish trend, X-108 recommended"
        }
    
    def generate_random_scenario(self) -> Dict[str, Any]:
        """Génère un scénario aléatoire."""
        generators = [
            self.generate_market_crash,
            self.generate_bull_market,
            self.generate_range_market,
            self.generate_pump_scenario,
            self.generate_bear_market
        ]
        
        generator = self.rng.choice(generators)
        return generator()
    
    def generate_batch(self, n: int = 10) -> List[Dict[str, Any]]:
        """Génère un batch de n scénarios aléatoires."""
        return [self.generate_random_scenario() for _ in range(n)]
    
    def generate_stress_test_suite(self) -> List[Dict[str, Any]]:
        """Génère une suite complète de stress tests."""
        return [
            self.generate_market_crash(),
            self.generate_market_crash(),
            self.generate_pump_scenario(),
            self.generate_pump_scenario(),
            self.generate_bull_market(),
            self.generate_bear_market(),
            self.generate_range_market(),
            self.generate_range_market(),
        ]
