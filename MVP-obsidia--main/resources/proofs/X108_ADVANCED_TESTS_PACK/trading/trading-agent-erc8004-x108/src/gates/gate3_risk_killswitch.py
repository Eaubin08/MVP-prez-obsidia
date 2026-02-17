import numpy as np

def compute_drawdown(equity_curve):
    peak = equity_curve[0] if len(equity_curve) else 1.0
    max_dd = 0.0
    for v in equity_curve:
        peak = max(peak, v)
        dd = 1.0 - v / peak
        max_dd = max(max_dd, float(dd))
    return float(max_dd)

def gate3_risk_kill(state: dict, returns: np.ndarray, cfg: dict):
    # drawdown/vol/consecutive loss based kill
    equity = state.get("equity_curve", [1.0])
    dd = compute_drawdown(equity)
    vol = float(np.std(returns[-50:])) if len(returns) else 0.0
    consec_losses = int(state.get("consecutive_losses", 0))
    cooldown = int(state.get("cooldown_remaining", 0))

    if cooldown > 0:
        return False, "cooldown"

    if dd >= float(cfg["max_drawdown"]):
        state["cooldown_remaining"] = int(cfg["cooldown_steps"])
        return False, "kill_drawdown"
    if vol >= float(cfg["max_volatility"]):
        state["cooldown_remaining"] = int(cfg["cooldown_steps"])
        return False, "kill_volatility"
    if consec_losses >= int(cfg["max_consecutive_losses"]):
        state["cooldown_remaining"] = int(cfg["cooldown_steps"])
        return False, "kill_losses"
    return True, "pass"
