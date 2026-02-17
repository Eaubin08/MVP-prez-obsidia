# Obsidia Unified Interface - Hackathon Demo

This project is a fully functional Streamlit application built by merging four distinct archives, demonstrating a robust governance and decision-making pipeline for autonomous agents.

## 🚀 What is Demonstrated

This application showcases a unified interface for governing an autonomous trading agent, following a strict, auditable pipeline from observation to action. The core principles are **safety, traceability, and robustness** over performance.

- **OS0 - Invariants**: The non-negotiable laws of the system (e.g., `BLOCK > HOLD > ALLOW`).
- **OS1 - Observation**: Feature extraction from market data (Volatility, Coherence, etc.).
- **OS2 - Simulation**: Monte Carlo projection (SIM-LITE) to forecast potential risks (Drawdown, Ruin).
- **OS3 - Governance**: A multi-stage gate system (Integrity, X-108 Temporal Lock, Risk) that filters and validates user intents.
- **OS4 - Reports**: A comprehensive audit trail with downloadable artifacts and decision timelines.

## 🛠️ How to Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Streamlit App**:
    ```bash
    streamlit run app/dashboard.py
    ```

## 📦 What Artifacts are Produced

On every run, the application generates a complete, auditable trail of the decision-making process in the `traces/` directory.

- **Logs (JSONL)**:
  - `traces/decision_log.jsonl`: Log of all feature computation events.
  - `traces/simulation_log.jsonl`: Log of all simulation runs and their verdicts.
  - `traces/roi_log.jsonl`: Log of all gate evaluations.
  - `traces/intents_log.jsonl`: Log of all emitted ERC-8004 intents.

- **Artifacts (JSON)**:
  - `traces/last_run/os0_snapshot.json`: A snapshot of the system's core invariants.
  - `traces/last_run/features.json`: The raw features computed in OS1.
  - `traces/last_run/simulation.json`: The full results from the SIM-LITE projection in OS2.
  - `traces/last_run/gates.json`: The detailed output of the gate evaluation in OS3.
  - `traces/last_run/erc8004_intent.json`: The final "paper" trade intent, ready for submission.

- **Downloadable ZIP**:
  - From the **OS4 - Reports** page, you can download `artifacts.zip`, a package containing all the JSON artifacts from the latest run for external auditing.

## 🎯 ERC-8004 Intent Export

The primary output of a successful governance cycle is the **ERC-8004 Trade Intent**.

- **Location**: You can find the generated paper intent in the `traces/last_run/` directory, named `erc8004_intent.json`.
- **Verification**: The content of this file is also displayed in the **OS4 - Reports** tab for easy verification within-app verification.
