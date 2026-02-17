"""Console X-108 - Timeline et validation pour Mode Guidé."""
import streamlit as st
from src.state_manager import get_data_flags

def render_console_x108():
    """Affiche la console X-108 avec timeline et statut de validation."""
    
    with st.expander("📊 Console X-108 - Timeline", expanded=False):
        st.markdown("""
        **X-108** : Protocole de délai de sécurité obligatoire avant toute action irréversible.
        
        La timeline ci-dessous montre la progression à travers les niveaux OS :
        """)
        
        flags = get_data_flags()
        
        # Timeline visuelle
        timeline_items = [
            ("OS0", "Invariants", True, "✅"),  # Toujours validé
            ("OS1", "Exploration", flags.get("features_computed", False), "🔍"),
            ("OS2", "Simulation", flags.get("simulation_done", False), "🎲"),
            ("OS3", "Gouvernance", flags.get("governance_tested", False), "⚖️"),
            ("OS4", "Rapport", False, "📊")  # Validé quand on arrive à OS4
        ]
        
        st.markdown("### 📍 Progression Pipeline")
        
        for os_level, label, completed, icon in timeline_items:
            if completed:
                st.markdown(f"✅ **{os_level} - {label}** {icon} : Complété")
            else:
                st.markdown(f"⏳ **{os_level} - {label}** {icon} : En attente")
        
        st.markdown("---")
        
        # Statut de validation
        st.markdown("### ✓ Statut de Validation")
        
        if flags.get("features_computed"):
            st.success("✅ Features calculées")
        else:
            st.warning("⏳ Features non calculées")
        
        if flags.get("simulation_done"):
            st.success("✅ Simulation exécutée")
        else:
            st.warning("⏳ Simulation non exécutée")
        
        if flags.get("governance_tested"):
            st.success("✅ Gouvernance testée")
        else:
            st.warning("⏳ Gouvernance non testée")
        
        st.markdown("---")
        st.caption("💡 La console X-108 garantit que chaque étape est validée avant de passer à la suivante.")
