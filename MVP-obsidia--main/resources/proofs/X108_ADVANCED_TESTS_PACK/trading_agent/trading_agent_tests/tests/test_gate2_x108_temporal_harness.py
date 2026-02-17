from __future__ import annotations

import pytest

# Target: src/gates/gate2_x108_temporal.py
from src.gates.gate2_x108_temporal import gate2_x108_temporal


def test_hold_by_time():
    state = {"last_invest_ts": 100.0}
    ok, reason = gate2_x108_temporal(
        state=state, now_ts=105.0, hold_seconds=10.0, coherence=1.0, coherence_threshold=0.6
    )
    assert ok is False
    assert reason == "x108_hold"


def test_hold_by_low_coherence():
    state = {"last_invest_ts": 100.0}
    ok, reason = gate2_x108_temporal(
        state=state, now_ts=120.0, hold_seconds=10.0, coherence=0.59, coherence_threshold=0.6
    )
    assert ok is False
    assert reason == "x108_low_coherence"


def test_pass_when_time_and_coherence_ok():
    state = {"last_invest_ts": 100.0}
    ok, reason = gate2_x108_temporal(
        state=state, now_ts=120.0, hold_seconds=10.0, coherence=0.9, coherence_threshold=0.6
    )
    assert ok is True
    assert reason == "pass"


@pytest.mark.parametrize("dt", [0.0, 1.0, 9.999])
def test_time_boundary_hold(dt):
    state = {"last_invest_ts": 100.0}
    ok, reason = gate2_x108_temporal(
        state=state, now_ts=100.0 + dt, hold_seconds=10.0, coherence=1.0, coherence_threshold=0.6
    )
    assert ok is False
    assert reason == "x108_hold"


@pytest.mark.parametrize("coh", [0.0, 0.1, 0.59])
def test_coherence_boundary_hold(coh):
    state = {"last_invest_ts": 100.0}
    ok, reason = gate2_x108_temporal(
        state=state, now_ts=200.0, hold_seconds=10.0, coherence=coh, coherence_threshold=0.6
    )
    assert ok is False
    assert reason == "x108_low_coherence"
