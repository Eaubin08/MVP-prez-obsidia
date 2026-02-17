import time
import pytest
from helpers.discovery import discover

def test_TNI02_t0_mutation_blocks():
    tgt = discover()
    if not tgt.intent_registry:
        pytest.skip("Intent registry write-once API not exposed (set_first_seen/get_first_seen)")
    r = tgt.intent_registry
    intent_id = "intent-t0-mutation"
    t0 = time.time()
    assert r.set_first_seen(intent_id, t0) in (True, None)
    # mutation attempt MUST fail
    assert r.set_first_seen(intent_id, t0 - 1.0) is False
