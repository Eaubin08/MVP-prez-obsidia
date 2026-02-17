import pytest
from helpers.discovery import discover

def test_TNI06_missing_trace_blocks_or_marks_systemic():
    tgt = discover()
    if not tgt.audit_api:
        pytest.skip("Audit API not exposed (trace / replay)")
    pytest.skip("Audit trace negative test requires explicit audit API contract (to be wired).")
