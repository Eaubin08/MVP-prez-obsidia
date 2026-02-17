import pytest
from helpers.discovery import discover

def test_TNI04_policy_hot_reload_enters_safe_hold():
    tgt = discover()
    if not tgt.policy_api:
        pytest.skip("Policy API not exposed (hot-reload safe-mode)")
    pytest.skip("Policy hot-reload test requires explicit API contract (to be wired).")

def test_TNI05_unattested_tool_is_blocked():
    tgt = discover()
    if not tgt.policy_api:
        pytest.skip("Policy API not exposed (tool attestation / allowlist)")
    pytest.skip("Tool attestation test requires explicit API contract (to be wired).")
