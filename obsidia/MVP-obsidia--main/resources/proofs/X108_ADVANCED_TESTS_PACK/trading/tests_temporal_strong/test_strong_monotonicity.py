
import time, random

def x108_gate(irrev, t0, now, tau):
    # conservative: if clock skew yields negative elapsed, hold for irreversible
    elapsed = now - t0
    if irrev and elapsed < tau:
        return "HOLD"
    return "ALLOW"

def test_strong_monotonicity_dense_grid_before_tau():
    tau = 10.0
    t0 = time.time()
    irrev = True
    # Dense grid strictly before tau
    for dt in [i * 0.1 for i in range(0, int((tau - 0.1)/0.1) + 1)]:
        assert x108_gate(irrev, t0, t0 + dt, tau) == "HOLD"

def test_strong_monotonicity_random_before_tau():
    tau = 10.0
    t0 = time.time()
    irrev = True
    for _ in range(200):
        dt = random.random() * (tau - 1e-6)  # strictly before
        assert x108_gate(irrev, t0, t0 + dt, tau) == "HOLD"
