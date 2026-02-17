"""OS4 — Reports / Audit / Replay."""
import streamlit as st
from pathlib import Path

from src.utils import read_artifact, zip_last_run

def render(base_dir: Path, config: dict):
    """Affiche l'interface de rapports et d'audit."""
    st.subheader("OS4 — Reports / Audit / Replay")
    st.caption("📊 Exports artifacts + basic replay from last_run folder.")
    
    # Vérifier les artifacts disponibles
    st.markdown("#### 📋 Last Run Artifacts")
    
    artifacts = {
        "features.json": read_artifact(base_dir, "features.json"),
        "simulation.json": read_artifact(base_dir, "simulation.json"),
        "gates.json": read_artifact(base_dir, "gates.json"),
        "erc8004_intent.json": read_artifact(base_dir, "erc8004_intent.json"),
        "os0_snapshot.json": read_artifact(base_dir, "os0_snapshot.json")
    }
    
    # Afficher le statut
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if artifacts["features.json"]:
            st.success("✅ Features")
        else:
            st.error("❌ Features")
    
    with col2:
        if artifacts["simulation.json"]:
            st.success("✅ Simulation")
        else:
            st.error("❌ Simulation")
    
    with col3:
        if artifacts["gates.json"]:
            st.success("✅ Gates")
        else:
            st.error("❌ Gates")
    
    with col4:
        if artifacts["erc8004_intent.json"]:
            st.success("✅ ERC-8004")
        else:
            st.error("❌ ERC-8004")
    
    with col5:
        if artifacts["os0_snapshot.json"]:
            st.success("✅ OS0")
        else:
            st.error("❌ OS0")
    
    # Export ZIP
    st.markdown("---")
    st.markdown("#### 📦 Export Artifacts")
    
    if st.button("📥 Zip last_run artifacts", type="primary"):
        zpath = zip_last_run(base_dir)
        st.success(f"✅ Created: `{zpath}`")
        
        # Bouton de téléchargement
        with open(zpath, "rb") as f:
            st.download_button(
                label="⬇️ Download artifacts.zip",
                data=f,
                file_name="artifacts.zip",
                mime="application/zip"
            )
    
    # Replay / Summary
    st.markdown("---")
    st.markdown("#### 🔄 Replay (Summary)")
    
    tabs = st.tabs(["Features", "Simulation", "Gates", "ERC-8004 Intent"])
    
    with tabs[0]:
        if artifacts["features.json"]:
            st.json(artifacts["features.json"])
        else:
            st.warning("No features artifact found.")
    
    with tabs[1]:
        if artifacts["simulation.json"]:
            st.json(artifacts["simulation.json"])
        else:
            st.warning("No simulation artifact found.")
    
    with tabs[2]:
        if artifacts["gates.json"]:
            st.json(artifacts["gates.json"])
        else:
            st.warning("No gates artifact found.")
    
    with tabs[3]:
        if artifacts["erc8004_intent.json"]:
            st.json(artifacts["erc8004_intent.json"])
            
            # Highlight ERC-8004 export location
            st.markdown("---")
            st.info("📍 **ERC-8004 Intent Export Location**: `traces/last_run/erc8004_intent.json`")
        else:
            st.warning("No ERC-8004 intent found. Go to OS3 to emit an intent.")
    
    # Naive vs Governed Comparison
    st.markdown("---")
    st.markdown("#### ⚖️ Naive vs Governed Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🚫 Naive Agent")
        st.code("""Decision: EXECUTE immediately
Reason: Signal is "good"
Laws: None
Risk: High (no gates, no X-108)
Survival: Low""", language="text")
    
    with col2:
        st.markdown("##### ✅ Governed Agent")
        if artifacts["gates.json"]:
            gates = artifacts["gates.json"].get("gates", {})
            decision = gates.get("decision", "UNKNOWN")
            reason = gates.get("reason", "")
            laws = gates.get("laws", [])
            
            st.code(f"""Decision: {decision}
Reason: {reason}
Laws: {len(laws)} activated
Risk: Controlled (gates + X-108)
Survival: High""", language="text")
        else:
            st.code("""Decision: WAIT/BLOCK
Reason: Gates not yet evaluated
Laws: X-108, BLOCK>HOLD>ALLOW
Risk: Controlled
Survival: High""", language="text")
    
    st.markdown("""
    **Key Difference**: The naive agent acts on impulse, while the governed agent enforces:
    - **Observation** → **Projection** → **Gates** → **X-108** → **Paper Intent**
    - The goal is **survival** and **traceability**, not opportunism.
    """)
    
    # Animation/Timeline (si disponible)
    st.markdown("---")
    st.markdown("#### 🎬 Timeline Animation")
    
    gif_path = base_dir / "resources" / "gifs" / "trade_blocked_timeline.gif"
    if gif_path.exists():
        st.image(str(gif_path), caption="Trade Blocked Timeline", use_container_width=True)
    else:
        st.info("Animation not available. Expected at: `resources/gifs/trade_blocked_timeline.gif`")
