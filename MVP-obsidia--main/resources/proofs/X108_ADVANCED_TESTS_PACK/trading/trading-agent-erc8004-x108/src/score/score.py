def compute_score(projected: dict, features: dict, x_bonus: float, weights: dict, dd_threshold: float) -> float:
    # projected: mu, sigma, p_dd, p_ruin, cvar_95
    E = projected.get("mu", 0.0)
    sigma = projected.get("sigma", 0.0)
    p_dd = projected.get("p_dd", 0.0)
    p_ruin = projected.get("p_ruin", 0.0)

    # T and V are proxies from features:
    # T ~ coherence, V ~ (1 - friction)
    T = float(features.get("coherence", 0.0))
    V = float(1.0 - float(features.get("friction", 0.0)))

    w_E = float(weights.get("w_E", 1.0))
    w_sigma = float(weights.get("w_sigma", 1.0))
    w_DD = float(weights.get("w_DD", 1.0))
    w_ruin = float(weights.get("w_ruin", 1.0))
    w_T = float(weights.get("w_T", 0.25))
    w_V = float(weights.get("w_V", 0.25))
    w_X = float(weights.get("w_X", 0.5))

    # Score as validated structure
    S = (w_E * E
         - w_sigma * sigma
         - w_DD * p_dd
         - w_ruin * p_ruin
         + w_T * T
         + w_V * V
         + w_X * x_bonus)
    return float(S)
