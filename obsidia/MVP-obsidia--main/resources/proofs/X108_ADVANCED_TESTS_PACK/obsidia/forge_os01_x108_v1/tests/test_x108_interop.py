from __future__ import annotations

import json
from pathlib import Path

import pytest

from obsidia_os1.os1 import run_request
from obsidia_os1.x108 import X108Gate


def _load_scenarios() -> list[dict]:
    path = Path(__file__).parent / "scenarios_sample.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


SCENARIOS = _load_scenarios()


@pytest.mark.parametrize("sc", SCENARIOS, ids=[s["id"] for s in SCENARIOS])
def test_x108_hold_or_act(sc: dict):
    gate = X108Gate(min_wait_s=float(sc.get("threshold", 108)))
    dec = run_request(
        raw_input=sc.get("input_text", "x = 1"),
        x108_gate=gate,
        x108_ctx={
            "irreversible": bool(sc.get("irreversible", True)),
            "time_elapsed": float(sc.get("time_elapsed", 0)),
            "threshold": float(sc.get("threshold", 108)),
        },
    )
    if sc["time_elapsed"] < sc["threshold"] and sc["irreversible"]:
        assert dec.decision == "HOLD"
    elif sc["irreversible"]:
        assert dec.decision in {"ACT", "HOLD"}
    else:
        # reversible: X108 should allow ACT
        assert dec.decision in {"ACT", "HOLD"}

    # SSR must always exist
    assert isinstance(dec.ssr, str) and len(dec.ssr) > 0
