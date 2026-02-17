
import subprocess, sys

tests = [
    "test_time_is_law.py",
    "test_structure_without_intelligence.py",
    "test_meta_coherence_simulation.py",
    "test_absolute_hold_gate.py",
    "test_non_invertible_order.py",
]

for t in tests:
    print("\n=== RUNNING", t, "===")
    subprocess.run([sys.executable, t], check=False)
