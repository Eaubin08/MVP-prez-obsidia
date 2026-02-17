"""Module de visualisation pour les données de marché et les décisions."""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

def plot_market_with_decision(df: pd.DataFrame, features: Dict[str, Any], 
                               gates_result: Optional[Dict[str, Any]] = None) -> go.Figure:
    """Crée un graphique de prix avec annotations de décision."""
    
    fig = go.Figure()
    
    # Prix
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['close'],
        mode='lines',
        name='Price',
        line=dict(color='#2E86DE', width=2)
    ))
    
    # Zone de volatilité
    if len(df) > 20:
        rolling_std = df['close'].rolling(20).std()
        upper = df['close'] + 2 * rolling_std
        lower = df['close'] - 2 * rolling_std
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=upper,
            mode='lines',
            name='Volatility Band',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=lower,
            mode='lines',
            name='Volatility Band',
            fill='tonexty',
            fillcolor='rgba(46, 134, 222, 0.1)',
            line=dict(width=0),
            showlegend=True
        ))
    
    # Annotation de décision
    if gates_result:
        decision = gates_result.get('decision', 'UNKNOWN')
        reason = gates_result.get('reason', '')
        
        # Couleur selon la décision
        colors = {
            'EXECUTE': 'green',
            'HOLD': 'orange',
            'BLOCK': 'red'
        }
        color = colors.get(decision, 'gray')
        
        # Point de décision (dernier point)
        last_price = df['close'].iloc[-1]
        last_idx = df.index[-1]
        
        fig.add_trace(go.Scatter(
            x=[last_idx],
            y=[last_price],
            mode='markers+text',
            name=f'Decision: {decision}',
            marker=dict(size=15, color=color, symbol='star'),
            text=[decision],
            textposition='top center',
            textfont=dict(size=12, color=color)
        ))
    
    # Layout
    fig.update_layout(
        title='Market Overview with Decision Point',
        xaxis_title='Time',
        yaxis_title='Price',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def plot_features_radar(features: Dict[str, Any]) -> go.Figure:
    """Crée un radar chart des features."""
    
    categories = ['Coherence', 'Stability', 'Low Friction']
    
    # Normaliser les valeurs [0, 1]
    values = [
        features.get('coherence', 0.5),
        1.0 - features.get('volatility', 0.5),  # Stabilité = inverse volatilité
        1.0 - features.get('friction', 0.5)     # Low friction
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current State',
        fillcolor='rgba(46, 134, 222, 0.3)',
        line=dict(color='#2E86DE', width=2)
    ))
    
    # Zone de sécurité (threshold)
    safe_threshold = [0.5, 0.5, 0.5]
    fig.add_trace(go.Scatterpolar(
        r=safe_threshold,
        theta=categories,
        fill='toself',
        name='Safe Threshold',
        fillcolor='rgba(46, 213, 115, 0.1)',
        line=dict(color='#2ED573', width=1, dash='dash')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        title='Market Features (Radar)',
        height=400
    )
    
    return fig

def plot_simulation_distribution(sim_result: Dict[str, Any]) -> go.Figure:
    """Crée un histogramme de la distribution de simulation."""
    
    # Simuler une distribution basée sur mu et sigma
    mu = sim_result.get('mu', 0.0)
    sigma = sim_result.get('sigma', 0.01)
    n_sims = sim_result.get('n_sims', 200)
    
    # Générer une distribution normale
    samples = np.random.normal(mu, sigma, n_sims)
    
    fig = go.Figure()
    
    # Histogramme
    fig.add_trace(go.Histogram(
        x=samples,
        nbinsx=30,
        name='Projected Returns',
        marker=dict(color='#2E86DE', opacity=0.7)
    ))
    
    # CVaR line
    cvar = sim_result.get('cvar_95', 0.0)
    fig.add_vline(
        x=cvar,
        line_dash="dash",
        line_color="red",
        annotation_text=f"CVaR 95%: {cvar:.4f}",
        annotation_position="top"
    )
    
    # Mean line
    fig.add_vline(
        x=mu,
        line_dash="dot",
        line_color="green",
        annotation_text=f"Mean: {mu:.4f}",
        annotation_position="bottom"
    )
    
    fig.update_layout(
        title='Simulation: Projected Returns Distribution',
        xaxis_title='Return',
        yaxis_title='Frequency',
        template='plotly_white',
        height=400
    )
    
    return fig

def plot_gates_timeline(gates_result: Dict[str, Any]) -> go.Figure:
    """Crée une timeline des gates."""
    
    gates = ['Gate 1\nIntegrity', 'Gate 2\nX-108', 'Gate 3\nRisk']
    statuses = [
        gates_result.get('gate1', {}).get('ok', False),
        gates_result.get('gate2', {}).get('ok', False),
        gates_result.get('gate3', {}).get('ok', False)
    ]
    
    colors = ['green' if s else 'red' for s in statuses]
    symbols = ['✅' if s else '❌' for s in statuses]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(len(gates))),
        y=[1]*len(gates),
        mode='markers+text',
        marker=dict(size=40, color=colors),
        text=symbols,
        textfont=dict(size=20),
        showlegend=False
    ))
    
    # Labels
    for i, gate in enumerate(gates):
        fig.add_annotation(
            x=i,
            y=0.8,
            text=gate,
            showarrow=False,
            font=dict(size=10)
        )
    
    # Decision finale
    decision = gates_result.get('decision', 'UNKNOWN')
    decision_color = {'EXECUTE': 'green', 'HOLD': 'orange', 'BLOCK': 'red'}.get(decision, 'gray')
    
    fig.add_trace(go.Scatter(
        x=[len(gates)],
        y=[1],
        mode='markers+text',
        marker=dict(size=50, color=decision_color, symbol='star'),
        text=[decision],
        textfont=dict(size=14, color='white'),
        name='Final Decision'
    ))
    
    fig.update_layout(
        title='Gates Evaluation Timeline',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, range=[0.5, 1.5]),
        template='plotly_white',
        height=200,
        showlegend=False
    )
    
    return fig
