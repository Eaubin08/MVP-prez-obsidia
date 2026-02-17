
import time

def x108_gate(irrev, t0, now, tau):
    # conservative behavior under skew: negative elapsed must not allow irreversible
    elapsed = now - t0
    if irrev and elapsed < tau:
        return "HOLD"
    return "ALLOW"

def test_clock_skew_negative_elapsed_holds():
    tau = 10.0
    t0 = time.time()
    now = t0 - 5.0  # clock went backwards / skew
    assert x108_gate(True, t0, now, tau) == "HOLD"

def test_clock_skew_small_jitter_near_threshold():
    tau = 10.0
    t0 = time.time()
    # just below tau with small jitter that should still be HOLD
    now = t0 + tau - 1e-9
    assert x108_gate(True, t0, now, tau) == "HOLD"

def test_clock_skew_allows_at_or_after_threshold():
    tau = 10.0
    t0 = time.time()
    now = t0 + tau
    assert x108_gate(True, t0, now, tau) == "ALLOW"
    now2 = t0 + tau + 0.001
    assert x108_gate(True, t0, now2, tau) == "ALLOW"
