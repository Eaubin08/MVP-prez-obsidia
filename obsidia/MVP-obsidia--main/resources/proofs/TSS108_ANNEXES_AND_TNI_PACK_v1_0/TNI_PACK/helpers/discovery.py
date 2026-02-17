from __future__ import annotations
import importlib
from dataclasses import dataclass
from typing import Any, Optional, Callable, Tuple

@dataclass
class Targets:
    obsidia_x108: Any | None = None
    trading_gate2: Callable[..., Tuple[bool, str]] | None = None
    intent_registry: Any | None = None
    policy_api: Any | None = None
    audit_api: Any | None = None

def _try_import(path: str):
    try:
        return importlib.import_module(path)
    except Exception:
        return None

def discover() -> Targets:
    t = Targets()
    # Obsidia canonical path
    m = _try_import("obsidia_os1.x108")
    if m and hasattr(m, "X108Gate"):
        t.obsidia_x108 = m.X108Gate
    # Trading canonical path
    m2 = _try_import("src.gates.gate2_x108_temporal")
    if m2 and hasattr(m2, "gate2_x108_temporal"):
        t.trading_gate2 = m2.gate2_x108_temporal
    # Optional intent registry API
    for cand in ["obsidia_os0.intent_registry", "intent_registry", "obsidia.intent_registry"]:
        mr = _try_import(cand)
        if mr and hasattr(mr, "set_first_seen") and hasattr(mr, "get_first_seen"):
            t.intent_registry = mr
            break
    # Optional policy API
    for cand in ["policy", "obsidia_policy", "obsidia_os2.policy"]:
        mp = _try_import(cand)
        if mp:
            t.policy_api = mp
            break
    # Optional audit API
    for cand in ["obsidia_os3.audit", "audit", "obsidia_audit"]:
        ma = _try_import(cand)
        if ma:
            t.audit_api = ma
            break
    return t
