"""Landing page with mode selection."""
import streamlit as st
from pathlib import Path

def render():
    """Affiche la landing page avec choix du mode."""
    
    # CSS personnalisé
    st.markdown("""
    <style>
    .landing-hero {
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 40px;
    }
    .landing-title {
        font-size: 48px;
        font-weight: bold;
        color: white;
        margin-bottom: 10px;
    }
    .landing-subtitle {
        font-size: 20px;
        color: rgba(255,255,255,0.9);
        margin-bottom: 0;
    }
    .mode-card {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        height: 100%;
        border: 2px solid transparent;
    }
    .mode-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    .mode-icon {
        font-size: 64px;
        margin-bottom: 20px;
    }
    .mode-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #333;
    }
    .mode-description {
        font-size: 16px;
        color: #666;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .mode-features {
        text-align: left;
        margin: 20px 0;
    }
    .mode-features li {
        margin: 8px 0;
        color: #555;
    }
    .quick-info {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="landing-hero">
        <h1 class="landing-title">🏛️ OBSIDIA</h1>
        <p class="landing-subtitle">Gouvernance Transparente pour IA Autonome</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick info (condensée)
    st.markdown("""
    <div class="quick-info">
        <strong>🎯 En bref :</strong> Obsidia garantit que chaque décision d'IA est <strong>traçable</strong>, 
        <strong>sécurisée</strong> (délai X-108) et <strong>auditable</strong> (exports JSON).
    </div>
    """, unsafe_allow_html=True)
    
    # CTA prominents
    st.markdown("## 🚀 Choisissez votre parcours")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">🎓</div>
            <div class="mode-title">Mode Guidé</div>
            <div class="mode-description">
                Workflow <strong>pas-à-pas</strong> avec explications détaillées.
                Parfait pour découvrir le système.
            </div>
            <div class="mode-features">
                <strong>✨ Inclut :</strong>
                <ul>
                    <li>✅ 5 étapes guidées</li>
                    <li>✅ Validation automatique</li>
                    <li>✅ Scénarios prédéfinis</li>
                    <li>✅ Assistance contextuelle</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Démarrer en Mode Guidé", type="primary", use_container_width=True, key="btn_guided"):
            st.session_state["app_mode"] = "guided"
            st.session_state["guided_step"] = 1
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">⚡</div>
            <div class="mode-title">Mode Expert</div>
            <div class="mode-description">
                Accès <strong>complet</strong> à toutes les fonctionnalités 
                sans guidage ni restrictions.
            </div>
            <div class="mode-features">
                <strong>✨ Inclut :</strong>
                <ul>
                    <li>✅ Accès direct OS0-OS6</li>
                    <li>✅ Configuration avancée</li>
                    <li>✅ Stress testing</li>
                    <li>✅ Exports complets</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ Démarrer en Mode Expert", use_container_width=True, key="btn_expert"):
            st.session_state["app_mode"] = "expert"
            st.rerun()
    
    st.markdown("---")
    
    # Section informative (condensée et collapsée par défaut)
    with st.expander("📚 En savoir plus sur Obsidia", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 Objectifs
            - **Transparence** : Décisions expliquées
            - **Sécurité** : Verrous temporels (X-108)
            - **Auditabilité** : Exports JSON/JSONL
            - **Reproductibilité** : Seed + Run ID
            
            ### 🔒 Lois Fondamentales
            1. **BLOCK > HOLD > ALLOW** (priorité stricte)
            2. **X-108 Temporal Lock** (délai τ obligatoire)
            3. **Exploration ≠ Action** (séparation des rôles)
            4. **Non-Anticipation** (pas d'action avant τ)
            """)
        
        with col2:
            st.markdown("""
            ### 🏗️ Architecture (6 niveaux)
            - **OS0** : Lois fondamentales
            - **OS1** : Exploration données
            - **OS2** : Simulation Monte Carlo
            - **OS3** : Gouvernance (gates + ROI)
            - **OS4** : Rapports et exports
            - **OS5** : Démo automatisée
            - **OS6** : Tests de stress
            
            ### 🌍 Domaines Supportés
            Trading, Santé, Juridique, Véhicules, Industrie, etc.
            """)
    
    with st.expander("🎓 Mode Guidé vs ⚡ Mode Expert", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎓 Mode Guidé
            
            **Pour qui ?**
            - Nouveaux utilisateurs
            - Démonstrations
            - Formation
            
            **Fonctionnement :**
            - Workflow linéaire (5 étapes)
            - Validation automatique
            - Explications détaillées
            - Console verrouillée progressivement
            """)
        
        with col2:
            st.markdown("""
            ### ⚡ Mode Expert
            
            **Pour qui ?**
            - Utilisateurs expérimentés
            - Développeurs
            - Auditeurs
            
            **Fonctionnement :**
            - Navigation libre OS0-OS6
            - Configuration avancée
            - Stress testing
            - Aucune restriction
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 14px;">
        <p>🏛️ <strong>Obsidia Unified Interface</strong> | Build: obsi-unified-mvp | Version: 1.0.0</p>
        <p>📖 <a href="#" style="color: #667eea;">Documentation</a> | 
           💬 <a href="#" style="color: #667eea;">Support</a> | 
           🔗 <a href="https://github.com/Eaubin08/MVP-obsidia-" style="color: #667eea;">GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)
