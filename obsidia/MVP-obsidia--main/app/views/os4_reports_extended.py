"""OS4 — Reports / Audit / Replay (Extended with Human Algebra & Proofs)."""
import streamlit as st
from pathlib import Path

from src.utils import read_artifact, zip_last_run

def render(base_dir: Path, config: dict):
    """Affiche l'interface de rapports et d'audit étendue."""
    st.subheader("OS4 — Reports / Audit / Replay")
    st.caption("📊 Exports artifacts + Human Algebra + Proofs + Naive vs Governed.")
    
    # Tabs principaux
    tabs = st.tabs([
        "📦 Artifacts",
        "📖 Human Algebra",
        "🧪 Proofs & Tests",
        "⚖️ Naive vs Governed",
        "🎬 Timeline"
    ])
    
    # Tab 1: Artifacts
    with tabs[0]:
        render_artifacts(base_dir)
    
    # Tab 2: Human Algebra
    with tabs[1]:
        render_human_algebra(base_dir)
    
    # Tab 3: Proofs
    with tabs[2]:
        render_proofs(base_dir)
    
    # Tab 4: Naive vs Governed
    with tabs[3]:
        render_naive_vs_governed(base_dir)
    
    # Tab 5: Timeline
    with tabs[4]:
        render_timeline(base_dir)

def render_artifacts(base_dir: Path):
    """Affiche les artifacts de last_run."""
    st.markdown("#### 📋 Last Run Artifacts")
    
    artifacts = {
        "features.json": read_artifact(base_dir, "features.json"),
        "simulation.json": read_artifact(base_dir, "simulation.json"),
        "gates.json": read_artifact(base_dir, "gates.json"),
        "erc8004_intent.json": read_artifact(base_dir, "erc8004_intent.json"),
        "os0_snapshot.json": read_artifact(base_dir, "os0_snapshot.json")
    }
    
    # Statut
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.success("✅ Features") if artifacts["features.json"] else st.error("❌ Features")
    with col2:
        st.success("✅ Simulation") if artifacts["simulation.json"] else st.error("❌ Simulation")
    with col3:
        st.success("✅ Gates") if artifacts["gates.json"] else st.error("❌ Gates")
    with col4:
        st.success("✅ ERC-8004") if artifacts["erc8004_intent.json"] else st.error("❌ ERC-8004")
    with col5:
        st.success("✅ OS0") if artifacts["os0_snapshot.json"] else st.error("❌ OS0")
    
    # Export ZIP
    st.markdown("---")
    if st.button("📥 Zip last_run artifacts", type="primary"):
        zpath = zip_last_run(base_dir)
        st.success(f"✅ Created: `{zpath}`")
        
        with open(zpath, "rb") as f:
            st.download_button(
                label="⬇️ Download artifacts.zip",
                data=f,
                file_name="artifacts.zip",
                mime="application/zip"
            )
    
    # Afficher les artifacts
    st.markdown("---")
    artifact_tabs = st.tabs(["Features", "Simulation", "Gates", "ERC-8004"])
    
    with artifact_tabs[0]:
        if artifacts["features.json"]:
            st.json(artifacts["features.json"])
        else:
            st.warning("No features artifact found.")
    
    with artifact_tabs[1]:
        if artifacts["simulation.json"]:
            st.json(artifacts["simulation.json"])
        else:
            st.warning("No simulation artifact found.")
    
    with artifact_tabs[2]:
        if artifacts["gates.json"]:
            st.json(artifacts["gates.json"])
        else:
            st.warning("No gates artifact found.")
    
    with artifact_tabs[3]:
        if artifacts["erc8004_intent.json"]:
            st.json(artifacts["erc8004_intent.json"])
            st.info("📍 **ERC-8004 Intent Export Location**: `traces/last_run/erc8004_intent.json`")
        else:
            st.warning("No ERC-8004 intent found. Go to OS3 to emit an intent.")

def render_human_algebra(base_dir: Path):
    """Affiche les documents d'algèbre humaine."""
    st.markdown("#### 📖 Human Algebra Documentation")
    
    algebra_docs = [
        ("ALGEBRE_HUMAINE_TRADING_AGENT.md", "Algèbre Humaine pour Trading Agent"),
        ("TABLE_ALGEBRE_PREUVES.md", "Table d'Algèbre et Preuves"),
        ("NARRATION_TRADE_BLOQUE.md", "Narration: Trade Bloqué"),
        ("SCENARIOS_ALGEBRE.md", "Scénarios d'Algèbre")
    ]
    
    for filename, title in algebra_docs:
        path = base_dir / "resources" / "human_algebra" / filename
        if path.exists():
            with st.expander(f"📄 {title}"):
                content = path.read_text(encoding="utf-8")
                st.markdown(content)
        else:
            st.warning(f"⚠️ {filename} not found")

def render_proofs(base_dir: Path):
    """Affiche les preuves et tests."""
    st.markdown("#### 🧪 Proofs & Institutional Tests")
    
    proof_sections = st.tabs([
        "Annexes Constitutionnelles",
        "TNI Pack",
        "X-108 Advanced Tests"
    ])
    
    with proof_sections[0]:
        annexes_path = base_dir / "resources" / "proofs" / "TSS108_ANNEXES_AND_TNI_PACK_v1_0" / "ANNEXES_CONSTITUTIONNELLES_v1.0.md"
        if annexes_path.exists():
            content = annexes_path.read_text(encoding="utf-8")
            st.markdown(content)
        else:
            st.warning("Annexes not found")
    
    with proof_sections[1]:
        tni_readme = base_dir / "resources" / "proofs" / "TSS108_ANNEXES_AND_TNI_PACK_v1_0" / "TNI_PACK" / "README.md"
        if tni_readme.exists():
            content = tni_readme.read_text(encoding="utf-8")
            st.markdown(content)
        else:
            st.warning("TNI Pack not found")
    
    with proof_sections[2]:
        x108_guide = base_dir / "resources" / "proofs" / "X108_ADVANCED_TESTS_PACK" / "PR_READY_GUIDE.md"
        if x108_guide.exists():
            content = x108_guide.read_text(encoding="utf-8")
            st.markdown(content)
        else:
            st.warning("X-108 tests not found")

def render_naive_vs_governed(base_dir: Path):
    """Affiche la comparaison Naive vs Governed."""
    st.markdown("#### ⚖️ Naive vs Governed Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🚫 Naive Agent")
        st.code("""Decision: EXECUTE immediately
Reason: Signal is "good"
Laws: None
Risk: High (no gates, no X-108)
Survival: Low

Timeline:
T0: Market signal detected
T1: EXECUTE (no delay)
T2: Loss realized
T3: Cascade failure""", language="text")
        
        st.error("❌ **Failure Mode**: Acts on impulse, no safety checks")
    
    with col2:
        st.markdown("##### ✅ Governed Agent")
        
        artifacts = read_artifact(base_dir, "gates.json")
        if artifacts:
            gates = artifacts.get("gates", {})
            decision = gates.get("decision", "UNKNOWN")
            reason = gates.get("reason", "")
            laws = gates.get("laws", [])
            
            st.code(f"""Decision: {decision}
Reason: {reason}
Laws: {len(laws)} activated
Risk: Controlled (gates + X-108)
Survival: High

Timeline:
T0: Market signal detected
T1: OS1 → Features computed
T2: OS2 → Simulation run
T3: OS3 → Gates evaluated
T4: {decision} (after τ seconds)""", language="text")
            
            if decision == "EXECUTE":
                st.success("✅ **Success Mode**: Validated through governance")
            else:
                st.warning(f"⚠️ **Protected Mode**: {decision} prevents loss")
        else:
            st.code("""Decision: WAIT/BLOCK
Reason: Gates not yet evaluated
Laws: X-108, BLOCK>HOLD>ALLOW
Risk: Controlled
Survival: High

Timeline:
T0: Market signal detected
T1-T4: Governance pipeline
T5: Decision after validation""", language="text")
            
            st.info("ℹ️ Run OS1→OS2→OS3 to see governed decision")
    
    st.markdown("---")
    st.markdown("""
    **Key Difference**: The naive agent acts on impulse, while the governed agent enforces:
    - **Observation** → **Projection** → **Gates** → **X-108** → **Paper Intent**
    - The goal is **survival** and **traceability**, not opportunism.
    """)

def render_timeline(base_dir: Path):
    """Affiche la timeline animée."""
    st.markdown("#### 🎬 Timeline Animation")
    
    gif_path = base_dir / "resources" / "gifs" / "trade_blocked_timeline.gif"
    if gif_path.exists():
        st.image(str(gif_path), caption="Trade Blocked Timeline", use_container_width=True)
    else:
        st.info("Animation not available. Expected at: `resources/gifs/trade_blocked_timeline.gif`")
