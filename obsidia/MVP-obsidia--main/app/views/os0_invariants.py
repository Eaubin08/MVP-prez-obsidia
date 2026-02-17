"""OS0 — Invariants (lecture seule)."""
import streamlit as st
from pathlib import Path
import json

def render(base_dir: Path):
    """Affiche les invariants système."""
    st.subheader("OS0 — Invariants (Read-Only)")
    
    st.markdown("#### 🔒 Core Laws")
    st.markdown("""
    - **X-108 Temporal Lock**: τ-second delay for irreversible intents (non-anticipation, clock-skew HOLD)
    - **Gate Priority**: **BLOCK > HOLD > ALLOW** (strict composition)
    - **Irreversibility Flag**: If `irreversible=true` ⇒ X-108 applies
    - **Role Separation**: Explorer ≠ Executor ≠ Roi (no bypass)
    - **Non-Anticipation**: ACT MUST NOT occur before τ seconds elapsed
    """)
    
    st.markdown("#### 📋 Contracts & Types")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.code("""Intent {
  domain: string
  action: BUY | SELL | HOLD
  amount: float
  asset: string
  timestamp: float
  irreversible: bool
  metadata: dict
}""", language="text")
    
    with col2:
        st.code("""Decision {
  EXECUTE | WAIT | BLOCK | EXIT
  reason: string
  laws: list[string]
}""", language="text")
    
    st.markdown("#### 📦 Build Info")
    from app.config import BUILD_VERSION, BUILD_HASH
    st.info(f"Version: `{BUILD_VERSION}` • Build Hash: `{BUILD_HASH}`")
    
    st.markdown("---")
    
    if st.button("📥 Export OS0 Snapshot (JSON)"):
        snap = {
            "laws": [
                "X-108 Temporal Lock",
                "BLOCK > HOLD > ALLOW",
                "Role separation",
                "Non-anticipation"
            ],
            "schemas": {
                "intent": ["domain", "action", "amount", "asset", "timestamp", "irreversible", "metadata"],
                "decision": ["EXECUTE", "WAIT", "BLOCK", "EXIT"]
            },
            "version": BUILD_VERSION,
            "build_hash": BUILD_HASH
        }
        
        out = base_dir / "traces" / "last_run" / "os0_snapshot.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(snap, indent=2), encoding="utf-8")
        
        st.success(f"✅ Saved: `{out}`")
        st.json(snap)
