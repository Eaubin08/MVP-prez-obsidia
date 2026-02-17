"""Domain Analytics Dashboard for comparing domain behaviors."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from src.domains_data import DOMAIN_CONFIGS, get_domain_config

def render():
    """Affiche le dashboard analytique des domaines."""
    
    st.markdown("## 📊 Analyse Comparative des Domaines")
    
    st.markdown("""
    Ce dashboard compare les caractéristiques et comportements des différents domaines d'application.
    Chaque domaine a des **seuils de criticité** et **délais de sécurité (τ)** adaptés à son contexte.
    """)
    
    st.markdown("---")
    
    # Préparer les données
    domains_data = []
    for domain_name, config in DOMAIN_CONFIGS.items():
        if domain_name != "Unified":
            domains_data.append({
                "Domaine": domain_name.split("(")[0].strip(),
                "Icon": config["icon"],
                "Seuil Irréversible (%)": config["irreversible_threshold"] * 100,
                "τ Recommandé (s)": config["default_tau"],
                "Tolérance Risque": config["risk_tolerance"],
                "Nb Scénarios": len(config.get("typical_scenarios", []))
            })
    
    df = pd.DataFrame(domains_data)
    
    # Métriques globales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌐 Domaines Disponibles", len(df))
    
    with col2:
        st.metric("⏱️ τ Moyen", f"{df['τ Recommandé (s)'].mean():.1f}s")
    
    with col3:
        st.metric("🔒 Seuil Moyen", f"{df['Seuil Irréversible (%)'].mean():.0f}%")
    
    with col4:
        critical_domains = len(df[df["Seuil Irréversible (%)"] >= 90])
        st.metric("⚠️ Domaines Critiques", critical_domains)
    
    st.markdown("---")
    
    # Tableau comparatif
    st.markdown("### 📋 Tableau Comparatif")
    
    # Formatter le dataframe pour l'affichage
    df_display = df.copy()
    df_display["Domaine"] = df_display["Icon"] + " " + df_display["Domaine"]
    df_display = df_display.drop("Icon", axis=1)
    
    # Colorer selon la criticité
    def color_criticality(val):
        if val >= 90:
            return 'background-color: #ffcccc'
        elif val >= 70:
            return 'background-color: #fff3cd'
        else:
            return 'background-color: #d4edda'
    
    styled_df = df_display.style.applymap(
        color_criticality,
        subset=['Seuil Irréversible (%)']
    )
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Seuil d'Irréversibilité par Domaine")
        
        fig_threshold = go.Figure(data=[
            go.Bar(
                x=df["Domaine"],
                y=df["Seuil Irréversible (%)"],
                text=df["Icon"],
                textposition='outside',
                marker=dict(
                    color=df["Seuil Irréversible (%)"],
                    colorscale='RdYlGn_r',
                    showscale=True,
                    colorbar=dict(title="Criticité (%)")
                )
            )
        ])
        
        fig_threshold.update_layout(
            xaxis_title="Domaine",
            yaxis_title="Seuil Irréversible (%)",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        
        st.plotly_chart(fig_threshold, use_container_width=True, key="domain_threshold_chart")
    
    with col2:
        st.markdown("### ⏱️ Délai de Sécurité τ par Domaine")
        
        fig_tau = go.Figure(data=[
            go.Bar(
                x=df["Domaine"],
                y=df["τ Recommandé (s)"],
                text=df["Icon"],
                textposition='outside',
                marker=dict(
                    color=df["τ Recommandé (s)"],
                    colorscale='Blues',
                    showscale=True,
                    colorbar=dict(title="τ (s)")
                )
            )
        ])
        
        fig_tau.update_layout(
            xaxis_title="Domaine",
            yaxis_title="τ Recommandé (secondes)",
            height=400
        )
        
        st.plotly_chart(fig_tau, use_container_width=True, key="domain_tau_chart")
    
    st.markdown("---")
    
    # Scatter plot: Criticité vs Délai
    st.markdown("### 🎯 Matrice Criticité vs Délai de Sécurité")
    
    fig_scatter = go.Figure(data=[
        go.Scatter(
            x=df["τ Recommandé (s)"],
            y=df["Seuil Irréversible (%)"],
            mode='markers+text',
            text=df["Icon"],
            textposition='top center',
            textfont=dict(size=20),
            marker=dict(
                size=15,
                color=df["Seuil Irréversible (%)"],
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Criticité (%)")
            ),
            hovertemplate='<b>%{text}</b><br>τ: %{x}s<br>Seuil: %{y}%<extra></extra>'
        )
    ])
    
    # Ajouter des zones
    fig_scatter.add_shape(
        type="rect",
        x0=0, x1=10, y0=0, y1=70,
        fillcolor="lightgreen", opacity=0.1,
        line=dict(width=0)
    )
    fig_scatter.add_annotation(
        x=5, y=35,
        text="Zone Faible Risque",
        showarrow=False,
        font=dict(size=10, color="green")
    )
    
    fig_scatter.add_shape(
        type="rect",
        x0=20, x1=35, y0=85, y1=100,
        fillcolor="lightcoral", opacity=0.1,
        line=dict(width=0)
    )
    fig_scatter.add_annotation(
        x=27.5, y=92.5,
        text="Zone Critique",
        showarrow=False,
        font=dict(size=10, color="red")
    )
    
    fig_scatter.update_layout(
        xaxis_title="τ Recommandé (secondes)",
        yaxis_title="Seuil Irréversible (%)",
        xaxis=dict(range=[0, 35]),
        yaxis=dict(range=[50, 105]),
        height=500
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True, key="domain_scatter_chart")
    
    st.markdown("---")
    
    # Détails par domaine
    st.markdown("### 🔍 Détails par Domaine")
    
    selected_domain = st.selectbox(
        "Sélectionnez un domaine pour voir les détails",
        options=list(DOMAIN_CONFIGS.keys())[:-1],  # Exclure Unified
        format_func=lambda x: f"{DOMAIN_CONFIGS[x]['icon']} {x}"
    )
    
    if selected_domain:
        config = get_domain_config(selected_domain)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### {config['icon']} {selected_domain}")
            st.markdown(f"**Description:** {config['description']}")
            st.markdown(f"**Tolérance au risque:** `{config['risk_tolerance']}`")
            
        with col2:
            st.metric("🔒 Seuil Irréversible", f"{config['irreversible_threshold']*100:.0f}%")
            st.metric("⏱️ τ Recommandé", f"{config['default_tau']}s")
        
        st.markdown("**Scénarios Typiques:**")
        for scenario in config.get("typical_scenarios", []):
            st.markdown(f"- {scenario}")
        
        if "critical_actions" in config:
            st.markdown("**Actions Critiques:**")
            for action in config["critical_actions"]:
                st.markdown(f"- `{action}`")
    
    st.markdown("---")
    
    # Explications
    with st.expander("💡 Comment interpréter ces données ?"):
        st.markdown("""
        ### Seuil d'Irréversibilité
        
        Le **seuil d'irréversibilité** indique à partir de quel niveau de confiance une action est considérée comme irréversible.
        
        - **< 70%** : Actions réversibles ou à faible impact
        - **70-85%** : Actions importantes nécessitant validation
        - **85-95%** : Actions critiques avec impact majeur
        - **> 95%** : Actions irréversibles avec conséquences graves
        
        ### Délai de Sécurité (τ)
        
        Le **délai de sécurité τ** (X-108 Temporal Lock) est le temps minimum obligatoire avant qu'une action irréversible puisse être exécutée.
        
        - **< 5s** : Décisions rapides (véhicules autonomes)
        - **5-15s** : Décisions standard (trading, blockchain)
        - **15-25s** : Décisions importantes (bancaire, juridique)
        - **> 25s** : Décisions critiques (médical)
        
        ### Tolérance au Risque
        
        - **very_low** : Domaines critiques (santé, juridique)
        - **low** : Domaines sensibles (bancaire, industriel)
        - **medium** : Domaines standards (trading, véhicules)
        - **high** : Domaines techniques (blockchain)
        """)
