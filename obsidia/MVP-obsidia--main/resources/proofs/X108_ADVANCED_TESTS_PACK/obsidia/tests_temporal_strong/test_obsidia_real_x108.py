
import time
import pytest

def test_obsidia_x108_real_negative_elapsed_is_hold():
    # Try importing real X108Gate; skip if not present
    try:
        from obsidia_os1.x108 import X108Gate, HOLD, ACT
    except Exception:
        pytest.skip("Real Obsidia X108Gate not importable in this layout")
    g = X108Gate(min_wait=10)
    # elapsed negative should behave as before-tau
    assert g.check(elapsed_s=-1.0, irreversible=True) == HOLD
    assert g.check(elapsed_s=0.0, irreversible=True) == HOLD
    assert g.check(elapsed_s=9.999, irreversible=True) == HOLD
    assert g.check(elapsed_s=10.0, irreversible=True) == ACT

def test_obsidia_x108_real_monotonicity_strong():
    try:
        from obsidia_os1.x108 import X108Gate, HOLD, ACT
    except Exception:
        pytest.skip("Real Obsidia X108Gate not importable in this layout")
    g = X108Gate(min_wait=10)
    # Strong monotonicity: any elapsed < min_wait is HOLD for irreversible
    for e in [i * 0.1 for i in range(0, 100)]:  # 0..9.9
        assert g.check(elapsed_s=e, irreversible=True) == HOLD
    assert g.check(elapsed_s=10.0, irreversible=True) == ACT
