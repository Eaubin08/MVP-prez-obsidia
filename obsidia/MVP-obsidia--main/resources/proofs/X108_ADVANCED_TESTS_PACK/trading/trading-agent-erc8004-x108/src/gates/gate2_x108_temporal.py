def gate2_x108_temporal(state: dict, now_ts: float, hold_seconds: float, coherence: float, coherence_threshold: float):
    last = float(state.get("last_invest_ts", 0.0))
    dt = now_ts - last
    if dt < hold_seconds:
        return False, "x108_hold"
    if coherence < coherence_threshold:
        return False, "x108_low_coherence"
    return True, "pass"
