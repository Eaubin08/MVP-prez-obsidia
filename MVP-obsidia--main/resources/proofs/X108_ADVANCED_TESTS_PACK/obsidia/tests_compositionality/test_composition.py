
import time

def compose_gates(gates, ctx):
    # BLOCK > HOLD > ALLOW
    decision = "ALLOW"
    for g in gates:
        d = g(ctx)
        if d == "BLOCK":
            return "BLOCK"
        if d == "HOLD":
            decision = "HOLD"
    return decision

def gate_x108(ctx):
    if ctx["irreversible"] and ctx["now"] - ctx["t0"] < ctx["tau"]:
        return "HOLD"
    return "ALLOW"

def gate_score(ctx):
    return "ALLOW" if ctx.get("score", 0) > 0.99 else "HOLD"

def gate_contract(ctx):
    return "ALLOW" if ctx.get("contract_ok", True) else "BLOCK"

def test_composition_preserves_non_anticipation():
    ctx = {
        "irreversible": True,
        "t0": time.time(),
        "now": time.time(),
        "tau": 10,
        "score": 1.0,
        "contract_ok": True,
    }
    gates = [gate_x108, gate_score, gate_contract]
    assert compose_gates(gates, ctx) != "ALLOW"

def test_block_dominates():
    ctx = {
        "irreversible": False,
        "t0": time.time()-100,
        "now": time.time(),
        "tau": 10,
        "score": 1.0,
        "contract_ok": False,
    }
    gates = [gate_x108, gate_score, gate_contract]
    assert compose_gates(gates, ctx) == "BLOCK"

def test_allow_only_if_all_allow():
    ctx = {
        "irreversible": False,
        "t0": time.time()-100,
        "now": time.time(),
        "tau": 10,
        "score": 1.0,
        "contract_ok": True,
    }
    gates = [gate_x108, gate_score, gate_contract]
    assert compose_gates(gates, ctx) == "ALLOW"
