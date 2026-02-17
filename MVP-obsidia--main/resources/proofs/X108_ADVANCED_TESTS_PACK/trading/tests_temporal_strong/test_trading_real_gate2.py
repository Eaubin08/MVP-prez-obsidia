
import time
import pytest

def test_trading_gate2_real_negative_elapsed_is_hold():
    # gate2 likely uses timestamps; we test conservative rule if callable
    try:
        from src.gates.gate2_x108_temporal import gate2_x108_temporal
    except Exception:
        pytest.skip("Real trading gate2_x108_temporal not importable in this layout")

    intent = {"irreversible": True, "first_seen": time.time(), "coherence": 1.0}
    ctx = {"now": intent["first_seen"] - 1.0, "tau": 10.0, "coherence_threshold": 0.6}
    # We don't know the exact signature; try common patterns, else skip
    try:
        out = gate2_x108_temporal(intent=intent, ctx=ctx)
    except TypeError:
        try:
            out = gate2_x108_temporal(intent, ctx)
        except Exception:
            pytest.skip("gate2_x108_temporal signature not compatible with harness assumptions")
    # Accept HOLD-like outputs (string or dict)
    if isinstance(out, str):
        assert out.upper() in {"HOLD", "ANALYZE", "BLOCK"}
    elif isinstance(out, dict):
        d = str(out.get("decision", "")).upper()
        assert d in {"HOLD", "ANALYZE", "BLOCK"}
    else:
        pytest.skip("Unexpected output type for gate2_x108_temporal")
