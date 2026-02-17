
import time
import pytest

class IntentMemoryGuard:
    """Conservative guard: t0 is write-once and must not move."""
    def __init__(self):
        self._t0 = {}

    def set_first_seen(self, intent_id, t0):
        if intent_id in self._t0:
            # mutation attempt
            if abs(self._t0[intent_id] - t0) > 1e-12:
                return False
        self._t0[intent_id] = t0
        return True

def test_t0_write_once_ok():
    g = IntentMemoryGuard()
    intent_id = "abc"
    t0 = time.time()
    assert g.set_first_seen(intent_id, t0) is True
    assert g.set_first_seen(intent_id, t0) is True

def test_t0_jitter_backward_blocks():
    g = IntentMemoryGuard()
    intent_id = "abc"
    t0 = time.time()
    assert g.set_first_seen(intent_id, t0) is True
    # attacker tries to move t0 backward
    assert g.set_first_seen(intent_id, t0 - 5.0) is False

def test_t0_jitter_forward_blocks():
    g = IntentMemoryGuard()
    intent_id = "abc"
    t0 = time.time()
    assert g.set_first_seen(intent_id, t0) is True
    # attacker tries to move t0 forward (to shorten elapsed)
    assert g.set_first_seen(intent_id, t0 + 5.0) is False

# Optional: if repo exposes a real intent memory / registry, test it here.
def test_real_memory_guard_if_available():
    try:
        import obsidia_os1  # noqa: F401
    except Exception:
        pytest.skip("No real Obsidia memory module importable in this layout")
    pytest.skip("Real memory guard not wired: this is a placeholder until exposed by repo")
