
PR READY GUIDE — X-108 Temporal Safety: Strong Monotonicity + Clock Skew

1) Suggested commits (split)
- test(x108): add strong monotonicity tests (HOLD stable for all t < tau)
- test(x108): add clock-skew robustness tests (negative elapsed => HOLD)
- test(x108): add optional real-import tests for Obsidia X108Gate / trading gate2 when importable

2) CI checklist
- Python matrix: 3.10, 3.11 (and 3.12 if supported)
- Install: pip install -r requirements.txt (or minimal: pytest)
- Command: pytest -q
- Fail-fast: enabled
- Artifacts: upload pytest logs on failure

3) Acceptance criteria
- All tests pass locally and in CI
- No production code changes required
- If real-import tests skip due to layout, CI still passes (skips are acceptable)


ADD-ON (Advanced tests)
- test(x108): enforce t0 write-once via IntentMemoryGuard tests (spec-level)
- test(x108): composition monotonicity for all t < tau (multi-gate)
- test(x108): fuzz 100k cases against oracle T_tau (includes negative elapsed)

Note: t0 jitter tests are spec-level until the repo exposes an immutable intent_first_seen registry.
