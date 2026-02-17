# Obsidia Unified Interface - Complete Hackathon Demo

This project is a fully functional Streamlit application built by merging four distinct archives, demonstrating a robust governance and decision-making pipeline for autonomous agents.

## 🚀 What is Demonstrated

This application showcases a unified interface for governing an autonomous trading agent, following a strict, auditable pipeline from observation to action. The core principles are **safety, traceability, and robustness** over performance.

The system implements a complete governance stack with five operational levels:

- **OS0 - Invariants**: The non-negotiable laws of the system (e.g., `BLOCK > HOLD > ALLOW`, X-108 temporal lock).
- **OS1 - Observation**: Feature extraction from market data (Volatility, Coherence, Friction, Regime).
- **OS2 - Simulation**: Monte Carlo projection (SIM-LITE) to forecast potential risks (Drawdown, Ruin probability).
- **OS3 - Governance**: A multi-stage gate system (Integrity, X-108 Temporal Lock, Risk Killswitch) that filters and validates user intents.
- **OS4 - Reports**: A comprehensive audit trail with downloadable artifacts, Human Algebra documentation, institutional proofs, and Naive vs Governed comparison.

## 🛠️ How to Run

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Eaubin08/MVP-obsidia-.git
   cd MVP-obsidia-
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run app/dashboard.py
   ```

The application will open automatically in your browser at `http://localhost:8501`.

## 🎯 Key Features

### Two Modes of Operation

1. **Proof Mode (Deterministic)**: 
   - Predefined scenarios with fixed seeds
   - Demonstrates specific governance outcomes (BLOCK, HOLD, EXECUTE)
   - Reproducible results for auditing

2. **Free Mode (Non-deterministic)**:
   - Live exploration with real market data
   - User-defined intents and parameters
   - Dynamic risk assessment

### Proof Scenarios

The application includes 5 predefined scenarios demonstrating different governance outcomes:

1. **BLOCK: Low Coherence** - Intent blocked due to high market volatility
2. **HOLD: X-108 Timer Active** - Intent held due to temporal lock
3. **EXECUTE: All Gates Pass** - Successful execution after validation
4. **BLOCK: Destructive Simulation** - Intent blocked due to high risk projection
5. **EXECUTE: Reversible Intent** - Immediate execution for non-irreversible actions

### Human Algebra & Institutional Proofs

The OS4 Reports section includes:

- **Human Algebra Documentation**: Qualitative representation of system states for non-technical stakeholders
- **Annexes Constitutionnelles**: Constitutional framework defining system laws and constraints
- **TNI Pack (Tests Négatifs Institutionnels)**: Institutional negative tests proving failure modes
- **X-108 Advanced Tests**: Comprehensive test suite for temporal lock validation
- **Naive vs Governed Comparison**: Side-by-side comparison showing the value of governance

## 📦 What Artifacts are Produced

On every run, the application generates a complete, auditable trail of the decision-making process in the `traces/` directory.

### Logs (JSONL)

- `traces/decision_log.jsonl`: Log of all feature computation events
- `traces/simulation_log.jsonl`: Log of all simulation runs and their verdicts
- `traces/roi_log.jsonl`: Log of all gate evaluations
- `traces/intents_log.jsonl`: Log of all emitted ERC-8004 intents

### Artifacts (JSON)

- `traces/last_run/os0_snapshot.json`: A snapshot of the system's core invariants
- `traces/last_run/features.json`: The raw features computed in OS1
- `traces/last_run/simulation.json`: The full results from the SIM-LITE projection in OS2
- `traces/last_run/gates.json`: The detailed output of the gate evaluation in OS3
- `traces/last_run/erc8004_intent.json`: The final "paper" trade intent, ready for submission

### Downloadable ZIP

From the **OS4 - Reports** page, you can download `artifacts.zip`, a package containing all the JSON artifacts from the latest run for external auditing.

## 🎯 ERC-8004 Intent Export

The primary output of a successful governance cycle is the **ERC-8004 Trade Intent**.

**Location**: You can find the generated paper intent in the `traces/last_run/` directory, named `erc8004_intent.json`.

**Verification**: The content of this file is also displayed in the **OS4 - Reports** tab for easy within-app verification.

## 📁 Project Structure

```
MVP-obsidia-/
├── app/
│   ├── dashboard.py          # Main Streamlit entry point
│   ├── config.py              # Global configuration
│   ├── router.py              # OS level navigation
│   ├── ui/
│   │   └── layout.py          # UI components (header, sidebar, invariant panel)
│   └── views/
│       ├── os0_invariants.py  # OS0 view
│       ├── os1_observation.py # OS1 view
│       ├── os2_simulation.py  # OS2 view
│       ├── os3_governance.py  # OS3 view
│       └── os4_reports_extended.py # OS4 view (with tabs)
├── src/
│   ├── core_pipeline.py       # Orchestration pipeline
│   ├── scenarios.py           # Scenario management
│   ├── features/              # Feature extraction
│   ├── simulation/            # Monte Carlo simulation
│   ├── gates/                 # Gate evaluation (1, 2, 3)
│   ├── roi_policy/            # ROI decision logic
│   ├── execution/             # ERC-8004 intent builder
│   ├── score/                 # Human algebra
│   └── utils.py               # Utilities (artifacts, logs)
├── data/
│   └── trading/
│       └── BTC_1h.csv         # Market data
├── scenarios/
│   └── deterministic/
│       └── trading_scenarios.json # Proof scenarios
├── resources/
│   ├── human_algebra/         # Human Algebra documentation
│   ├── proofs/                # Institutional proofs and tests
│   └── gifs/                  # Timeline animations
├── traces/                    # Generated artifacts and logs
├── requirements.txt
└── README.md
```

## 🧪 Acceptance Tests

The project meets all acceptance criteria:

1. ✅ `streamlit run app/dashboard.py` runs with no errors
2. ✅ Proof Mode has predefined scenarios resulting in BLOCK/HOLD/EXECUTE with clear reasons
3. ✅ Generates artifacts:
   - `traces/decision_log.jsonl`
   - `traces/last_run/features.json`
   - `traces/last_run/simulation.json`
   - `traces/last_run/gates.json`
   - `traces/last_run/erc8004_intent.json`
   - `artifacts.zip` downloadable from OS4
4. ✅ "Naive vs Governed" comparison page exists and is accessible in OS4
5. ✅ README.md explains what is demonstrated, how to run, what artifacts are produced, and where to find the ERC-8004 intent export

## 📚 Additional Resources

- **Human Algebra**: Qualitative symbolic representation for non-technical communication
- **Annexes Constitutionnelles**: Legal-like framework defining system constraints
- **TNI Pack**: Institutional negative tests proving safe failure modes
- **X-108 Advanced Tests**: Comprehensive temporal lock validation suite

## 🤝 Contributing

This is a hackathon demonstration project. For questions or collaboration, please open an issue on GitHub.

## 📄 License

This project is provided as-is for demonstration purposes.
