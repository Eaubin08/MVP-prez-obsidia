"""OS6 — Exploration (Non-Deterministic Scenarios)."""
import streamlit as st
from pathlib import Path
import pandas as pd

from src.scenario_generator import ScenarioGenerator
from src.core_pipeline import run_observation, run_simulation, evaluate_gates
from src.visualization import plot_market_with_decision, plot_features_radar, plot_gates_timeline
from src.explainer import explain_decision_flow

def render(base_dir: Path, config: dict):
    """Affiche l'interface d'exploration non-déterministe."""
    st.subheader("OS6 — Exploration (Non-Deterministic)")
    st.caption("🎲 Generate random but realistic market scenarios for stress testing.")
    
    # Mode selection
    mode = st.radio(
        "Exploration Mode",
        ["Single Random", "Batch Generation", "Stress Test Suite"],
        horizontal=True
    )
    
    if mode == "Single Random":
        render_single_random(base_dir, config)
    elif mode == "Batch Generation":
        render_batch(base_dir, config)
    else:
        render_stress_test(base_dir, config)

def render_single_random(base_dir: Path, config: dict):
    """Génère et exécute un scénario aléatoire unique."""
    
    st.markdown("#### 🎲 Generate Random Scenario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        seed = st.number_input("Seed (for reproducibility)", min_value=0, value=None, step=1)
    
    with col2:
        regime_filter = st.selectbox(
            "Regime Filter",
            ["Any", "crash", "bear", "range", "bull", "pump"]
        )
    
    if st.button("🎲 Generate & Run", type="primary"):
        with st.spinner("Generating scenario..."):
            generator = ScenarioGenerator(seed=seed if seed else None)
            
            # Générer selon le filtre
            if regime_filter == "Any":
                scenario = generator.generate_random_scenario()
            elif regime_filter == "crash":
                scenario = generator.generate_market_crash()
            elif regime_filter == "bull":
                scenario = generator.generate_bull_market()
            elif regime_filter == "bear":
                scenario = generator.generate_bear_market()
            elif regime_filter == "pump":
                scenario = generator.generate_pump_scenario()
            else:
                scenario = generator.generate_range_market()
            
            # Exécuter le scénario
            result = execute_scenario(base_dir, config, scenario)
            
            st.success("✅ Scenario executed!")
            
            # Afficher le scénario généré
            st.markdown("---")
            st.markdown("### 📋 Generated Scenario")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Market Conditions**")
                st.json(scenario["market_conditions"])
            
            with col2:
                st.markdown("**Intent**")
                st.json(scenario["intent"])
            
            # Résultats
            display_result(result)

def render_batch(base_dir: Path, config: dict):
    """Génère et exécute un batch de scénarios."""
    
    st.markdown("#### 📦 Batch Generation")
    
    n_scenarios = st.slider("Number of scenarios", 5, 50, 10, 5)
    
    if st.button("🚀 Generate Batch", type="primary"):
        generator = ScenarioGenerator()
        scenarios = generator.generate_batch(n_scenarios)
        
        st.session_state["batch_scenarios"] = scenarios
        st.success(f"✅ Generated {len(scenarios)} scenarios!")
    
    if "batch_scenarios" in st.session_state:
        scenarios = st.session_state["batch_scenarios"]
        
        st.markdown(f"**Generated {len(scenarios)} scenarios**")
        
        if st.button("▶️ Run All Scenarios"):
            results = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, scenario in enumerate(scenarios):
                status_text.text(f"Running scenario {i+1}/{len(scenarios)}...")
                
                result = execute_scenario(base_dir, config, scenario)
                results.append(result)
                
                progress_bar.progress((i + 1) / len(scenarios))
            
            status_text.text("✅ All scenarios completed!")
            
            # Statistiques
            st.markdown("---")
            st.markdown("### 📊 Batch Results")
            
            df_results = pd.DataFrame([
                {
                    "ID": r["scenario_id"],
                    "Regime": r["market_conditions"]["regime"],
                    "Decision": r["actual_decision"],
                    "Reason": r["actual_reason"][:50] + "..." if len(r["actual_reason"]) > 50 else r["actual_reason"]
                }
                for r in results
            ])
            
            st.dataframe(df_results, use_container_width=True)
            
            # Statistiques par décision
            decision_counts = df_results["Decision"].value_counts()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("EXECUTE", decision_counts.get("EXECUTE", 0))
            with col2:
                st.metric("HOLD", decision_counts.get("HOLD", 0))
            with col3:
                st.metric("BLOCK", decision_counts.get("BLOCK", 0))
            
            # Graphique de distribution
            st.bar_chart(decision_counts)

def render_stress_test(base_dir: Path, config: dict):
    """Exécute une suite de stress tests."""
    
    st.markdown("#### 🧪 Stress Test Suite")
    st.info("This will run a comprehensive suite of extreme market scenarios.")
    
    if st.button("🔥 Run Stress Tests", type="primary"):
        generator = ScenarioGenerator()
        scenarios = generator.generate_stress_test_suite()
        
        results = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, scenario in enumerate(scenarios):
            status_text.text(f"Running {scenario['name']}...")
            
            result = execute_scenario(base_dir, config, scenario)
            results.append(result)
            
            progress_bar.progress((i + 1) / len(scenarios))
        
        status_text.text("✅ Stress tests completed!")
        
        # Afficher les résultats
        st.markdown("---")
        st.markdown("### 🔥 Stress Test Results")
        
        for idx, result in enumerate(results):
            with st.expander(f"{result['scenario_id']} - {result['actual_decision']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Market Conditions**")
                    st.json(result["market_conditions"])
                
                with col2:
                    st.markdown("**Decision**")
                    decision = result["actual_decision"]
                    color = {"EXECUTE": "🟢", "HOLD": "🟡", "BLOCK": "🔴"}.get(decision, "⚪")
                    st.markdown(f"{color} **{decision}**")
                    st.caption(result["actual_reason"])
                
                # Timeline
                if result.get("gates_result"):
                    fig = plot_gates_timeline(result["gates_result"])
                    st.plotly_chart(fig, use_container_width=True, key=f"os6_stress_{result['scenario_id']}_{idx}")

def execute_scenario(base_dir: Path, config: dict, scenario: dict) -> dict:
    """Exécute un scénario et retourne les résultats."""
    
    # Charger les données
    data_path = base_dir / "data" / "trading" / "BTC_1h.csv"
    df = pd.read_csv(data_path)
    prices = df["close"].values
    returns = pd.Series(prices).pct_change().dropna().values
    
    # OS1: Observation
    features = run_observation(returns, base_dir)
    
    # Override avec market_conditions
    if "market_conditions" in scenario:
        features.update(scenario["market_conditions"])
    
    # OS2: Simulation
    sim_result = run_simulation(returns, base_dir, n_sims=100, horizon=10)
    
    # OS3: Gates
    intent = scenario.get("intent", {})
    intent["timestamp"] = 0.0
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
        hold_started_ts=0.0,
        tau_seconds=config.get("tau", 10.0),
        state=state,
        returns=returns,
        base_dir=base_dir
    )
    
    return {
        "scenario_id": scenario["id"],
        "market_conditions": scenario.get("market_conditions", {}),
        "actual_decision": gates_result.get("decision"),
        "actual_reason": gates_result.get("reason"),
        "features": features,
        "sim_result": sim_result,
        "gates_result": gates_result
    }

def display_result(result: dict):
    """Affiche les résultats d'un scénario."""
    
    st.markdown("---")
    st.markdown("### 🎯 Decision Result")
    
    decision = result["actual_decision"]
    color_emoji = {"EXECUTE": "🟢", "HOLD": "🟡", "BLOCK": "🔴"}.get(decision, "⚪")
    
    st.markdown(f"## {color_emoji} {decision}")
    st.caption(result["actual_reason"])
    
    # Timeline
    if result.get("gates_result"):
        fig = plot_gates_timeline(result["gates_result"])
        st.plotly_chart(fig, use_container_width=True, key="os6_result_timeline")
    
    # Radar chart
    col1, col2 = st.columns(2)
    
    with col1:
        from src.visualization import plot_features_radar
        fig_radar = plot_features_radar(result["features"])
        st.plotly_chart(fig_radar, use_container_width=True, key="os6_result_radar")
    
    with col2:
        # Explication
        st.markdown("**📖 Explanation**")
        explanation = explain_decision_flow(
            result["features"],
            result["sim_result"],
            result["gates_result"]
        )
        with st.expander("View Full Explanation"):
            st.markdown(explanation)
