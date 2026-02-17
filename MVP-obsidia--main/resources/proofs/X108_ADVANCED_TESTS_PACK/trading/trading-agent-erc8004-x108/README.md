# trading-agent-erc8004-x108

Hackathon-ready skeleton implementing the **validated** pipeline:

Market Data → Features (coherence/friction/regime) → Simulation (SIM-LITE) → Projected metrics (μ, σ, P(DD), P(ruin), CVaR) → Score → Gates (1→2→3) → Roi (X-108 long horizon) → TradeIntent (ERC-8004) → Execution + logs

This repo is intentionally minimal and deterministic. It does **not** ship external market feeds; it can run on a CSV OHLCV.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# generate a sample market CSV
python scripts/make_sample_csv.py --out data/sample_prices.csv

# run a backtest-like dry run (no broker)
python scripts/run_backtest.py --csv data/sample_prices.csv
```

Outputs are written to `logs/`:
- decision_log.jsonl
- simulation_log.jsonl
- roi_log.jsonl
- orders_log.jsonl

## Folder layout

- `src/features/` feature extraction (coherence/friction/regime)
- `src/simulation/` SIM-LITE bootstrap projection
- `src/score/` score function + defaults
- `src/gates/` Gate1/2/3 (integrity, X-108 temporal, risk/kill)
- `src/roi_policy/` Roi sovereign decisions (change strategy / adjust risk / exit market)
- `src/execution/` ERC-8004 TradeIntent builder + dry executor
- `app/dashboard.py` optional Streamlit dashboard (reads logs)

## Notes

- Gate2 implements X-108 **for investment decisions** (not micro-ticks): HOLD window + stability check.
- Roi decisions are rare and logged; trader executes only when Roi allows.

