"""OS5 — Auto-Run / Demo Mode (Automated Scenario Runner)."""
import streamlit as st
import time
import pandas as pd
from pathlib import Path

from src.scenarios import load_scenarios, apply_scenario
from src.core_pipeline import run_observation, run_simulation, evaluate_gates
from src.explainer import explain_decision_flow
from src.visualization import plot_market_with_decision, plot_gates_timeline

def render(base_dir: Path, config: dict):
    """Affiche l'interface Auto-Run pour démonstrations automatisées."""
    st.subheader("OS5 — Auto-Run / Demo Mode")
    st.caption("🎬 Automated execution of all Proof scenarios for demonstration.")
    
    # Charger les scénarios
    scenarios = load_scenarios(base_dir, "trading")
    
    if not scenarios:
        st.error("❌ No scenarios found. Please check `scenarios/deterministic/trading_scenarios.json`.")
        return
    
    st.markdown(f"#### 🎯 Available Scenarios: {len(scenarios)}")
    
    # Options de mode
    mode = st.radio(
        "Select Mode",
        ["Single Scenario", "Run All Scenarios", "Comparison View"],
        horizontal=True
    )
    
    if mode == "Single Scenario":
        render_single_scenario(base_dir, config, scenarios)
    elif mode == "Run All Scenarios":
        render_run_all(base_dir, config, scenarios)
    else:
        render_comparison(base_dir, config, scenarios)

def render_single_scenario(base_dir: Path, config: dict, scenarios: list):
    """Exécute un seul scénario avec explication détaillée."""
    
    scenario_names = [f"{s['id']}: {s['name']}" for s in scenarios]
    selected = st.selectbox("Choose Scenario", scenario_names)
    
    scenario_id = selected.split(":")[0]
    scenario = next((s for s in scenarios if s["id"] == scenario_id), None)
    
    if not scenario:
        st.error("Scenario not found")
        return
    
    st.markdown(f"**Description**: {scenario['description']}")
    st.markdown(f"**Expected Decision**: `{scenario['expected_decision']}`")
    st.markdown(f"**Expected Reason**: `{scenario['expected_reason']}`")
    
    if st.button("▶️ Run Scenario", type="primary"):
        with st.spinner("Running scenario..."):
            result = execute_scenario(base_dir, config, scenario)
            
            st.success("✅ Scenario completed!")
            
            # Afficher les résultats
            display_scenario_result(result, scenario)

def render_run_all(base_dir: Path, config: dict, scenarios: list):
    """Exécute tous les scénarios en séquence."""
    
    st.markdown("#### 🚀 Run All Scenarios")
    st.info(f"This will execute all {len(scenarios)} scenarios in sequence.")
    
    if st.button("▶️ Start Auto-Run", type="primary"):
        results = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, scenario in enumerate(scenarios):
            status_text.text(f"Running {scenario['id']}...")
            
            result = execute_scenario(base_dir, config, scenario)
            results.append(result)
            
            progress_bar.progress((i + 1) / len(scenarios))
            time.sleep(0.5)  # Pause pour visualisation
        
        status_text.text("✅ All scenarios completed!")
        
        # Afficher le tableau de résultats
        st.markdown("---")
        st.markdown("#### 📊 Results Summary")
        
        df_results = pd.DataFrame([
            {
                "Scenario": r["scenario_id"],
                "Expected": r["expected_decision"],
                "Actual": r["actual_decision"],
                "Match": "✅" if r["expected_decision"] == r["actual_decision"] else "❌",
                "Reason": r["actual_reason"]
            }
            for r in results
        ])
        
        st.dataframe(df_results, use_container_width=True)
        
        # Statistiques
        matches = sum(1 for r in results if r["expected_decision"] == r["actual_decision"])
        accuracy = matches / len(results) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Scenarios", len(results))
        with col2:
            st.metric("Matches", matches)
        with col3:
            st.metric("Accuracy", f"{accuracy:.0f}%")

def render_comparison(base_dir: Path, config: dict, scenarios: list):
    """Affiche une comparaison côte à côte de tous les scénarios."""
    
    st.markdown("#### ⚖️ Scenarios Comparison")
    
    if st.button("🔄 Load All Scenarios", type="primary"):
        with st.spinner("Loading all scenarios..."):
            results = []
            
            for scenario in scenarios:
                result = execute_scenario(base_dir, config, scenario)
                results.append(result)
            
            st.session_state["comparison_results"] = results
            st.success("✅ All scenarios loaded!")
    
    if "comparison_results" in st.session_state:
        results = st.session_state["comparison_results"]
        
        # Afficher en grille
        cols = st.columns(2)
        
        for i, result in enumerate(results):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"##### {result['scenario_id']}")
                    
                    decision = result["actual_decision"]
                    color = {"EXECUTE": "🟢", "HOLD": "🟡", "BLOCK": "🔴"}.get(decision, "⚪")
                    
                    st.markdown(f"{color} **{decision}**")
                    st.caption(result["actual_reason"])
                    
                    # Timeline
                    if result.get("gates_result"):
                        fig = plot_gates_timeline(result["gates_result"])
                        st.plotly_chart(fig, use_container_width=True, key=f"os5_timeline_{result['scenario_id']}")

def execute_scenario(base_dir: Path, config: dict, scenario: dict) -> dict:
    """Exécute un scénario complet et retourne les résultats."""
    
    # Appliquer le scénario
    params = apply_scenario(scenario)
    
    # Charger les données
    data_path = base_dir / "data" / "trading" / "BTC_1h.csv"
    df = pd.read_csv(data_path)
    prices = df["close"].values
    returns = pd.Series(prices).pct_change().dropna().values
    
    # OS1: Observation
    features = run_observation(returns, base_dir)
    
    # Override avec market_conditions du scénario si présent
    if "market_conditions" in params:
        features.update(params["market_conditions"])
    
    # OS2: Simulation
    sim_result = run_simulation(returns, base_dir, n_sims=100, horizon=10)
    
    # Override simulation si présent
    if params.get("simulation_override"):
        sim_result.update(params["simulation_override"])
    
    # OS3: Gates
    intent = params.get("intent", {})
    intent["timestamp"] = time.time()
    intent["coherence"] = features.get("coherence", 0.5)
    
    state = {
        "last_invest_ts": 0.0,
        "equity_curve": [1.0],
        "consecutive_losses": 0,
        "cooldown_remaining": 0
    }
    
    gates_result = evaluate_gates(
        intent=intent,
        features=features,
        sim_result=sim_result,
        hold_started_ts=params.get("time_elapsed", 0.0),
        tau_seconds=params.get("tau", 10.0),
        state=state,
        returns=returns,
        base_dir=base_dir
    )
    
    return {
        "scenario_id": scenario["id"],
        "expected_decision": params.get("expected_decision"),
        "expected_reason": params.get("expected_reason"),
        "actual_decision": gates_result.get("decision"),
        "actual_reason": gates_result.get("reason"),
        "features": features,
        "sim_result": sim_result,
        "gates_result": gates_result
    }

def display_scenario_result(result: dict, scenario: dict):
    """Affiche les résultats détaillés d'un scénario."""
    
    st.markdown("---")
    st.markdown("### 📊 Scenario Results")
    
    # Comparaison Expected vs Actual
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Expected")
        st.code(f"""Decision: {result['expected_decision']}
Reason: {result['expected_reason']}""", language="text")
    
    with col2:
        st.markdown("#### Actual")
        decision = result['actual_decision']
        color = {"EXECUTE": "green", "HOLD": "orange", "BLOCK": "red"}.get(decision, "gray")
        
        if result['expected_decision'] == decision:
            st.success(f"✅ Match! Decision: {decision}")
        else:
            st.error(f"❌ Mismatch! Expected {result['expected_decision']}, got {decision}")
        
        st.code(f"""Decision: {decision}
Reason: {result['actual_reason']}""", language="text")
    
    # Explication complète
    st.markdown("---")
    st.markdown("### 📖 Complete Explanation")
    
    explanation = explain_decision_flow(
        result["features"],
        result["sim_result"],
        result["gates_result"]
    )
    
    st.markdown(explanation)
