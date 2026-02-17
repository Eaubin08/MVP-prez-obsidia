import numpy as np

def realized_vol(returns: np.ndarray, window: int = 20) -> float:
    if len(returns) == 0:
        return 0.0
    if len(returns) < window:
        return float(np.std(returns))
    return float(np.std(returns[-window:]))

def coherence_from_vol(vol: float) -> float:
    # deterministic, bounded [0,1]
    return float(max(0.0, min(1.0, 1.0 - 10.0 * vol)))

def friction_from_vol(vol: float) -> float:
    return float(max(0.0, min(1.0, 10.0 * vol)))

def regime_from_returns(returns: np.ndarray, window: int = 50) -> str:
    if len(returns) < 2:
        return "unknown"
    w = returns[-window:] if len(returns) >= window else returns
    mu = float(np.mean(w))
    vol = float(np.std(w) + 1e-12)
    z = mu / vol
    if z > 0.2:
        return "trend_up"
    if z < -0.2:
        return "trend_down"
    return "range"

def extract_features(returns: np.ndarray) -> dict:
    vol = realized_vol(returns, 20)
    return {
        "volatility": vol,
        "coherence": coherence_from_vol(vol),
        "friction": friction_from_vol(vol),
        "regime": regime_from_returns(returns, 50),
    }
