
from obsidia_os2.metrics import compute_metrics_core_fixed

def test_core_world_invariance():
    # Simple 4-node example (2 core, 2 world)
    W = [
        [0,1,0,0],
        [1,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
    ]
    core = [0,1]

    m1 = compute_metrics_core_fixed(W, core)

    # Modify world-only edges
    W[2][3] = W[3][2] = 0.9

    m2 = compute_metrics_core_fixed(W, core)

    assert m1.S == m2.S
