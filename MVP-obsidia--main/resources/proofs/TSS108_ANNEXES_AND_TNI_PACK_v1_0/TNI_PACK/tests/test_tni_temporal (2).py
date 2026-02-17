import random
import pytest
from helpers.discovery import discover

def test_TNI01_non_anticipation_hold_before_tau():
    tgt = discover()
    if not tgt.obsidia_x108:
        pytest.skip("X108Gate not detected (obsidia_os1.x108.X108Gate)")
    Gate = tgt.obsidia_x108
    g = Gate(min_wait_s=108.0)
    random.seed(1337)
    for _ in range(500):
        e = random.uniform(-10.0, 107.999999)
        out = g.check(elapsed_s=e, irreversible=True)
        assert out.decision == "HOLD"

def test_TNI03_clock_skew_negative_elapsed_hold():
    tgt = discover()
    if tgt.obsidia_x108:
        g = tgt.obsidia_x108(min_wait_s=108.0)
        out = g.check(elapsed_s=-1.0, irreversible=True)
        assert out.decision == "HOLD"
    elif tgt.trading_gate2:
        state = {"last_invest_ts": 1000.0}
        ok, reason = tgt.trading_gate2(state, now_ts=999.0, hold_seconds=10.0, coherence=1.0, coherence_threshold=0.6)
        assert ok is False and reason == "x108_hold"
    else:
        pytest.skip("No temporal gate detected")
