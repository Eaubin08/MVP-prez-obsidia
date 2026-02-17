
import time

def decide(irrev, t0, now, tau):
    if irrev and now - t0 < tau:
        return "HOLD"
    return "ALLOW"

def test_idempotence_same_inputs():
    tau = 10
    t0 = time.time()
    irrev = True
    now = t0 + 3
    d1 = decide(irrev, t0, now, tau)
    d2 = decide(irrev, t0, now, tau)
    d3 = decide(irrev, t0, now, tau)
    assert d1 == d2 == d3

def test_idempotence_after_tau():
    tau = 10
    t0 = time.time()
    irrev = True
    now = t0 + tau + 1
    assert decide(irrev, t0, now, tau) == decide(irrev, t0, now, tau)
