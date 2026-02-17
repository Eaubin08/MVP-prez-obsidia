
from obsidia_os2.metrics import compute_metrics_core_fixed, decision_act_hold

def test_end_to_end_simple():
    W = [
        [0,1,0,0],
        [1,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
    ]
    core = [0,1]
    m = compute_metrics_core_fixed(W, core)
    decision = decision_act_hold(m, theta_S=0.0)
    assert decision in ["ACT","HOLD"]
