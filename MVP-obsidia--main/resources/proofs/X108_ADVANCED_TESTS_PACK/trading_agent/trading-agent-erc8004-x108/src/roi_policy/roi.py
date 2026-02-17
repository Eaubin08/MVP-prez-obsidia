from dataclasses import dataclass
from typing import List, Optional

@dataclass
class RoiState:
    risk_level: float
    strategy: str
    last_roi_decision_step: int
    last_strategy_change_step: int
    safe_mode: bool

def roi_init(cfg: dict) -> RoiState:
    return RoiState(
        risk_level=float(cfg["default_risk_level"]),
        strategy="base",
        last_roi_decision_step=-10**9,
        last_strategy_change_step=-10**9,
        safe_mode=False
    )

def roi_decide(
    roi: RoiState,
    step: int,
    mean_score: float,
    cfg: dict,
    gate3_reason: Optional[str] = None
):
    # Decision 3: SAFE exit if gate3 triggered often or explicit reason
    if gate3_reason in ("kill_drawdown", "kill_losses", "kill_volatility"):
        roi.safe_mode = True
        roi.last_roi_decision_step = step
        return "EXIT_MARKET_SAFE"

    if roi.safe_mode:
        # Only long-horizon re-entry allowed (outside this minimal skeleton)
        return "HOLD_SAFE"

    cooldown = int(cfg["roi_cooldown_steps"])
    if step - roi.last_roi_decision_step < cooldown:
        return "NOOP"

    # Decision 1: Change strategy if persistent positive mean_score
    persist = int(cfg["strategy_change_min_persist_steps"])
    if mean_score >= 0.0 and (step - roi.last_strategy_change_step) >= persist:
        roi.strategy = "alt" if roi.strategy == "base" else "base"
        roi.last_strategy_change_step = step
        roi.last_roi_decision_step = step
        return "CHANGE_STRATEGY"

    # Decision 2: Adjust risk level (discrete)
    levels: List[float] = [float(x) for x in cfg["risk_levels"]]
    # simple rule: if mean_score positive, step up risk; if negative, step down
    idx = min(range(len(levels)), key=lambda i: abs(levels[i] - roi.risk_level))
    if mean_score > 0.1 and idx < len(levels) - 1:
        roi.risk_level = levels[idx + 1]
        roi.last_roi_decision_step = step
        return "ADJUST_RISK_UP"
    if mean_score < -0.1 and idx > 0:
        roi.risk_level = levels[idx - 1]
        roi.last_roi_decision_step = step
        return "ADJUST_RISK_DOWN"

    return "NOOP"
