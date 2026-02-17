from __future__ import annotations

import math
import pytest

# Target: forge_os01_x108_v1/src/obsidia_os1/x108.py
from obsidia_os1.x108 import X108Gate


def test_reversible_bypass_act():
    gate = X108Gate(min_wait_s=108.0)
    res = gate.check(elapsed_s=0.0, irreversible=False)
    assert res.decision == "ACT"
    assert res.wait_s == 0.0


@pytest.mark.parametrize(
    "elapsed,min_wait,expected_decision,expected_wait",
    [
        (0.0, 108.0, "HOLD", 108.0),
        (10.0, 108.0, "HOLD", 98.0),
        (107.999, 108.0, "HOLD", pytest.approx(0.001, abs=1e-3)),
        (108.0, 108.0, "ACT", 0.0),
        (109.0, 108.0, "ACT", 0.0),
    ],
)
def test_irreversible_time_gate(elapsed, min_wait, expected_decision, expected_wait):
    gate = X108Gate(min_wait_s=min_wait)
    res = gate.check(elapsed_s=elapsed, irreversible=True)
    assert res.decision == expected_decision
    if expected_decision == "HOLD":
        assert res.wait_s == expected_wait
        assert "HOLD" in res.reason
    else:
        assert res.wait_s == expected_wait
        assert "satisfied" in res.reason.lower() or "bypass" in res.reason.lower()


def test_monotonicity_irreversible():
    gate = X108Gate(min_wait_s=108.0)
    # For irreversible actions, once ACT is reachable at time t, it must remain reachable for t' >= t.
    times = [0.0, 50.0, 107.0, 108.0, 200.0]
    decisions = [gate.check(t, True).decision for t in times]
    # Find first ACT, then all subsequent must be ACT
    if "ACT" in decisions:
        first_act = decisions.index("ACT")
        assert all(d == "ACT" for d in decisions[first_act:])
