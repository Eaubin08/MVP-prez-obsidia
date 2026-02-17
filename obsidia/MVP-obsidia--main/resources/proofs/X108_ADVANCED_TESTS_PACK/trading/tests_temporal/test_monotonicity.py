
import time

def x108_gate(irrev, t0, now, tau):
    if irrev and now - t0 < tau:
        return "HOLD"
    return "ALLOW"

def test_monotonicity_before_tau():
    tau = 10
    t0 = time.time()
    irrev = True
    # simulate time progression strictly before tau
    decisions = []
    for dt in [0, 1, 2, 5, 9]:
        decisions.append(x108_gate(irrev, t0, t0 + dt, tau))
    # HOLD must never regress to ALLOW before tau
    assert all(d == "HOLD" for d in decisions)

def test_transition_at_tau():
    tau = 10
    t0 = time.time()
    irrev = True
    assert x108_gate(irrev, t0, t0 + tau - 0.001, tau) == "HOLD"
    assert x108_gate(irrev, t0, t0 + tau, tau) == "ALLOW"
