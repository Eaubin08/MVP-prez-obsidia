
import random, time

def oracle_T_tau(irrev, elapsed, tau):
    if irrev and elapsed < tau:
        return "HOLD"
    return "ALLOW"

def gate_x108(irrev, elapsed, tau):
    # model: same as oracle
    if irrev and elapsed < tau:
        return "HOLD"
    return "ALLOW"

def test_fuzz_oracle_100k():
    random.seed(1337)
    tau = 10.0
    for _ in range(100_000):
        irrev = random.choice([True, False])
        # elapsed range includes negative, before, at, after
        elapsed = random.uniform(-5.0, 25.0)
        assert gate_x108(irrev, elapsed, tau) == oracle_T_tau(irrev, elapsed, tau)
