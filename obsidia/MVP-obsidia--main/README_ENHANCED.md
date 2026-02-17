# Obsidia Unified Interface - Enhanced Demo

This project is a fully functional Streamlit application demonstrating a robust governance and decision-making pipeline for autonomous agents, now enhanced with **interactive visualizations**, **real-time explanations**, **auto-run demos**, and **non-deterministic exploration**.

## 🚀 What's New in This Version

### 📊 Interactive Market Visualizations
- **Price charts** with decision annotations
- **Radar charts** showing market features (Coherence, Stability, Friction)
- **Distribution plots** for Monte Carlo simulations
- **Gates timeline** visualization showing the decision pipeline

### 💬 Real-Time Human Algebra Explanations
- **Live narrative** translating technical metrics into plain language
- **Step-by-step reasoning** from observation → simulation → gates → decision
- **Color-coded warnings** and recommendations
- **Complete decision flow** explanation in OS4

### 🎬 OS5 — Auto-Run / Demo Mode
- **Single Scenario**: Run predefined scenarios with detailed explanations
- **Run All Scenarios**: Execute all 5 proof scenarios in sequence
- **Comparison View**: Side-by-side visualization of all scenarios
- **Accuracy metrics**: Track expected vs actual decisions

### 🎲 OS6 — Exploration (Non-Deterministic)
- **Random Scenario Generator**: Create realistic market scenarios on-the-fly
- **Batch Generation**: Generate and test 5-50 scenarios at once
- **Stress Test Suite**: Extreme scenarios (crash, pump, bear, bull, range)
- **Regime Filters**: Focus on specific market conditions

## 🎯 Complete Feature List

### Core Governance Pipeline (OS0-OS4)

- **OS0 - Invariants**: Non-negotiable system laws
- **OS1 - Observation**: Feature extraction with **interactive charts** and **real-time explanations**
- **OS2 - Simulation**: Monte Carlo projection with **distribution visualization**
- **OS3 - Governance**: Multi-gate system with **timeline visualization**
- **OS4 - Reports**: Audit trail, Human Algebra docs, Proofs, Naive vs Governed comparison

### New Modes (OS5-OS6)

- **OS5 - Auto-Run**: Automated execution of proof scenarios for demos
- **OS6 - Exploration**: Non-deterministic scenario generation and stress testing

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

## 📚 User Guide

### For Demonstrations (Recommended Path)

1. **Start with OS5 - Auto-Run**:
   - Select "Run All Scenarios" to see the complete governance pipeline in action
   - Watch as the system processes 5 different market scenarios
   - See accuracy metrics and decision distribution

2. **Explore OS6 - Exploration**:
   - Generate random scenarios to stress-test the system
   - Try the "Stress Test Suite" for extreme conditions
   - Observe how the system handles crashes, pumps, and volatile markets

3. **Review OS4 - Reports**:
   - Check the "Naive vs Governed" comparison
   - Read the Human Algebra documentation
   - Download artifacts for external audit

### For Manual Testing

1. **OS1 - Observation**:
   - Load market data and compute features
   - See the **price chart** with volatility bands
   - Read the **real-time explanation** of market conditions
   - View the **radar chart** showing Coherence, Stability, and Friction

2. **OS2 - Simulation**:
   - Run Monte Carlo simulation
   - See the **distribution plot** with CVaR and mean lines
   - Understand risk projection in plain language

3. **OS3 - Governance**:
   - Create a paper intent (BUY/SELL)
   - Evaluate gates and see the **timeline visualization**
   - Understand why the decision was BLOCK/HOLD/EXECUTE

4. **OS4 - Reports**:
   - Download artifacts as ZIP
   - Review complete decision flow
   - Access institutional proofs and tests

## 🎨 Visualization Features

### Market Overview (OS1)
- **Price Chart**: Shows historical prices with volatility bands
- **Decision Points**: Annotated markers showing where decisions were made
- **Radar Chart**: 3-axis visualization of Coherence, Stability, and Low Friction

### Simulation (OS2)
- **Distribution Histogram**: Shows projected returns from Monte Carlo
- **CVaR Line**: Marks the 95% Conditional Value at Risk
- **Mean Line**: Shows expected return

### Gates (OS3)
- **Timeline**: Visual representation of Gate 1 → Gate 2 → Gate 3 → Decision
- **Status Indicators**: ✅ PASS or ❌ FAIL for each gate
- **Final Decision Star**: Color-coded (🟢 EXECUTE, 🟡 HOLD, 🔴 BLOCK)

## 📖 Human Algebra Explanations

Every level now includes **real-time narrative explanations**:

- **OS1**: "The market is unstable (V↑↑), coherence is low (C↓↓) → BLOCK recommended"
- **OS2**: "Simulation shows 15% chance of ruin → DESTRUCTIVE scenario → BLOCK"
- **OS3**: "Gate 2 failed: X-108 timer not elapsed → HOLD required"

These explanations translate technical metrics into **plain language** for non-technical stakeholders.

## 🧪 Scenario Types

### Deterministic (Proof Mode)
1. **BLOCK: Low Coherence** - High volatility blocks the intent
2. **HOLD: X-108 Timer** - Temporal lock activates
3. **EXECUTE: All Gates Pass** - Successful execution
4. **BLOCK: Destructive Simulation** - High risk projection
5. **EXECUTE: Reversible Intent** - No X-108 required

### Non-Deterministic (Exploration Mode)
- **Market Crash**: Extreme volatility, rapid decline
- **Bull Market**: Strong uptrend, high confidence
- **Bear Market**: Sustained downtrend
- **Range-Bound**: Sideways movement, mixed signals
- **Pump**: Sudden surge with high volatility

## 📦 Artifacts Produced

- `traces/decision_log.jsonl`: Feature computation log
- `traces/simulation_log.jsonl`: Simulation runs log
- `traces/roi_log.jsonl`: Gate evaluations log
- `traces/intents_log.jsonl`: ERC-8004 intents log
- `traces/last_run/*.json`: Latest run artifacts
- `artifacts.zip`: Downloadable package (from OS4)

## 🎯 ERC-8004 Intent Export

**Location**: `traces/last_run/erc8004_intent.json`

**Verification**: Displayed in OS4 - Reports tab

## 📁 Enhanced Project Structure

```
MVP-obsidia-/
├── app/
│   ├── dashboard.py          # Main entry point
│   ├── config.py              # Configuration (now with OS5, OS6)
│   ├── router.py              # Navigation
│   ├── ui/layout.py           # UI components
│   └── views/
│       ├── os0_invariants.py
│       ├── os1_observation.py  # ✨ Enhanced with visualizations
│       ├── os2_simulation.py   # ✨ Enhanced with distribution plots
│       ├── os3_governance.py   # ✨ Enhanced with timeline
│       ├── os4_reports_extended.py
│       ├── os5_autorun.py      # 🆕 Auto-Run / Demo Mode
│       └── os6_exploration.py  # 🆕 Non-Deterministic Exploration
├── src/
│   ├── core_pipeline.py
│   ├── scenarios.py
│   ├── scenario_generator.py  # 🆕 Random scenario generator
│   ├── visualization.py       # 🆕 Plotly visualizations
│   ├── explainer.py           # 🆕 Real-time explanations
│   ├── features/
│   ├── simulation/
│   ├── gates/
│   ├── roi_policy/
│   ├── execution/
│   ├── score/
│   └── utils.py
├── scenarios/
│   └── deterministic/
│       └── trading_scenarios.json
├── resources/
│   ├── human_algebra/
│   ├── proofs/
│   └── gifs/
├── data/
│   └── trading/BTC_1h.csv
├── traces/                    # Generated artifacts
├── requirements.txt
└── README.md
```

## ✨ Key Improvements

1. **Visual Understanding**: Charts and graphs make market conditions immediately clear
2. **Plain Language**: Human Algebra explanations remove technical barriers
3. **Demo-Ready**: OS5 Auto-Run perfect for presentations and demos
4. **Stress Testing**: OS6 Exploration enables comprehensive testing
5. **Transparency**: Every decision is explained step-by-step

## 🧪 Acceptance Tests

All original criteria ✅ PLUS:

6. ✅ Interactive visualizations in OS1, OS2, OS3
7. ✅ Real-time Human Algebra explanations
8. ✅ OS5 Auto-Run mode with scenario comparison
9. ✅ OS6 Exploration mode with random scenario generation
10. ✅ Stress test suite for extreme market conditions

## 🤝 Contributing

This is a hackathon demonstration project. For questions or collaboration, please open an issue on GitHub.

## 📄 License

This project is provided as-is for demonstration purposes.
