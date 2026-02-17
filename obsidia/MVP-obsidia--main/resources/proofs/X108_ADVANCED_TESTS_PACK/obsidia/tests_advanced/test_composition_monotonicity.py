
import time, random

def compose(gates, ctx):
    decision = "ALLOW"
    for g in gates:
        d = g(ctx)
        if d == "BLOCK":
            return "BLOCK"
        if d == "HOLD":
            decision = "HOLD"
    return decision

def gate_x108(ctx):
    elapsed = ctx["now"] - ctx["t0"]
    if ctx["irreversible"] and elapsed < ctx["tau"]:
        return "HOLD"
    return "ALLOW"

def gate_contract(ctx):
    return "ALLOW" if ctx.get("contract_ok", True) else "BLOCK"

def gate_score(ctx):
    # irrelevant noisy gate
    return "ALLOW" if ctx.get("score", 0.0) > 0.99 else "HOLD"

def test_composition_monotone_all_t_before_tau():
    tau = 10.0
    t0 = time.time()
    gates = [gate_x108, gate_score, gate_contract]
    for _ in range(200):
        dt = random.random() * (tau - 1e-6)
        ctx = {
            "irreversible": True,
            "t0": t0,
            "now": t0 + dt,
            "tau": tau,
            "score": 1.0,
            "contract_ok": True,
        }
        assert compose(gates, ctx) != "ALLOW"
