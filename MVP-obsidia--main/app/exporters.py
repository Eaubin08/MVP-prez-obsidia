"""
Module d'export pour Obsidia
============================
Export des rapports en PDF et Excel.
"""
import io
import json
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd
import streamlit as st


def export_to_excel(run_id: str, data: Dict[str, Any]) -> bytes:
    """Exporte les données d'un run au format Excel."""
    
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Feuille 1: Informations générales
        info_data = {
            'Propriété': ['Run ID', 'Date', 'Domaine', 'Seed', 'Tau (s)', 'Décision Finale'],
            'Valeur': [
                run_id,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                data.get('domain', 'N/A'),
                data.get('seed', 'N/A'),
                data.get('tau', 'N/A'),
                data.get('decision', 'N/A')
            ]
        }
        pd.DataFrame(info_data).to_excel(writer, sheet_name='Informations', index=False)
        
        # Feuille 2: Features
        if 'features' in data:
            features_df = pd.DataFrame([data['features']])
            features_df.to_excel(writer, sheet_name='Features', index=False)
        
        # Feuille 3: Simulation
        if 'simulation' in data:
            sim = data['simulation']
            sim_data = {
                'Métrique': ['Mu', 'Sigma', 'P(Ruin)', 'P(DD)', 'CVaR 95%', 'Verdict', 'N Sims', 'Horizon'],
                'Valeur': [
                    sim.get('mu', 'N/A'),
                    sim.get('sigma', 'N/A'),
                    sim.get('p_ruin', 'N/A'),
                    sim.get('p_dd', 'N/A'),
                    sim.get('cvar_95', 'N/A'),
                    sim.get('verdict', 'N/A'),
                    sim.get('n_sims', 'N/A'),
                    sim.get('horizon', 'N/A')
                ]
            }
            pd.DataFrame(sim_data).to_excel(writer, sheet_name='Simulation', index=False)
        
        # Feuille 4: Décision (Gates)
        if 'decision' in data:
            decision = data['decision']
            gates_data = {
                'Gate': ['Gate 1 - Integrity', 'Gate 2 - X-108', 'Gate 3 - Risk', 'Décision Finale'],
                'Status': [
                    'PASS' if decision.get('gate1', {}).get('ok') else 'FAIL',
                    'PASS' if decision.get('gate2', {}).get('ok') else 'HOLD',
                    'PASS' if decision.get('gate3', {}).get('ok') else 'FAIL',
                    decision.get('decision', 'N/A')
                ],
                'Raison': [
                    decision.get('gate1', {}).get('reason', 'N/A'),
                    decision.get('gate2', {}).get('reason', 'N/A'),
                    decision.get('gate3', {}).get('reason', 'N/A'),
                    decision.get('reason', 'N/A')
                ]
            }
            pd.DataFrame(gates_data).to_excel(writer, sheet_name='Décision', index=False)
        
        # Feuille 5: Intent
        if 'intent' in data:
            intent = data['intent']
            intent_data = {
                'Propriété': ['Asset', 'Side', 'Amount', 'Irreversible', 'Timestamp'],
                'Valeur': [
                    intent.get('asset', 'N/A'),
                    intent.get('side', 'N/A'),
                    intent.get('amount', 'N/A'),
                    'Oui' if intent.get('irreversible') else 'Non',
                    datetime.fromtimestamp(intent.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S') if intent.get('timestamp') else 'N/A'
                ]
            }
            pd.DataFrame(intent_data).to_excel(writer, sheet_name='Intent', index=False)
    
    output.seek(0)
    return output.getvalue()


def export_to_pdf(run_id: str, data: Dict[str, Any]) -> bytes:
    """Exporte les données d'un run au format PDF."""
    
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
    except ImportError:
        st.error("❌ ReportLab n'est pas installé. Installez-le avec: pip install reportlab")
        return b""
    
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#7c9fff'),
        spaceAfter=12
    )
    
    elements = []
    
    # Titre
    elements.append(Paragraph("🏛️ OBSIDIA - Rapport de Gouvernance", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Informations générales
    elements.append(Paragraph("📋 Informations Générales", subtitle_style))
    
    info_data = [
        ['Propriété', 'Valeur'],
        ['Run ID', run_id],
        ['Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Domaine', str(data.get('domain', 'N/A'))],
        ['Seed', str(data.get('seed', 'N/A'))],
        ['Tau (s)', str(data.get('tau', 'N/A'))],
        ['Décision Finale', str(data.get('decision', 'N/A'))]
    ]
    
    info_table = Table(info_data, colWidths=[2.5*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c9fff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Features
    if 'features' in data:
        elements.append(Paragraph("📊 Features du Marché", subtitle_style))
        features = data['features']
        features_data = [
            ['Métrique', 'Valeur'],
            ['Volatility', f"{features.get('volatility', 0):.6f}"],
            ['Coherence', f"{features.get('coherence', 0):.6f}"],
            ['Friction', f"{features.get('friction', 0):.6f}"],
            ['Regime', str(features.get('regime', 'N/A'))]
        ]
        
        features_table = Table(features_data, colWidths=[2.5*inch, 4*inch])
        features_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(features_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Simulation
    if 'simulation' in data:
        elements.append(Paragraph("🎲 Résultats de Simulation", subtitle_style))
        sim = data['simulation']
        sim_data = [
            ['Métrique', 'Valeur'],
            ['Mu (Expected Return)', f"{sim.get('mu', 0):.6f}"],
            ['Sigma (Volatility)', f"{sim.get('sigma', 0):.6f}"],
            ['P(Ruin)', f"{sim.get('p_ruin', 0):.4f}"],
            ['P(DD > 5%)', f"{sim.get('p_dd', 0):.4f}"],
            ['CVaR 95%', f"{sim.get('cvar_95', 0):.6f}"],
            ['Verdict', str(sim.get('verdict', 'N/A'))]
        ]
        
        sim_table = Table(sim_data, colWidths=[2.5*inch, 4*inch])
        sim_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9800')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(sim_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Décision (Gates)
    if 'decision' in data:
        elements.append(Paragraph("⚖️ Évaluation des Gates", subtitle_style))
        decision = data['decision']
        
        # Couleur selon la décision
        decision_color = colors.HexColor('#4CAF50') if decision.get('decision') == 'EXECUTE' else colors.HexColor('#F44336')
        
        gates_data = [
            ['Gate', 'Status', 'Raison'],
            ['Gate 1 - Integrity', 'PASS' if decision.get('gate1', {}).get('ok') else 'FAIL', 
             str(decision.get('gate1', {}).get('reason', 'N/A'))],
            ['Gate 2 - X-108', 'PASS' if decision.get('gate2', {}).get('ok') else 'HOLD',
             str(decision.get('gate2', {}).get('reason', 'N/A'))],
            ['Gate 3 - Risk', 'PASS' if decision.get('gate3', {}).get('ok') else 'FAIL',
             str(decision.get('gate3', {}).get('reason', 'N/A'))],
            ['Décision Finale', str(decision.get('decision', 'N/A')),
             str(decision.get('reason', 'N/A'))]
        ]
        
        gates_table = Table(gates_data, colWidths=[2*inch, 1.5*inch, 3*inch])
        gates_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c9fff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, -1), (-1, -1), decision_color),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        elements.append(gates_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Intent
    if 'intent' in data:
        elements.append(Paragraph("📝 Intent ERC-8004", subtitle_style))
        intent = data['intent']
        intent_data = [
            ['Propriété', 'Valeur'],
            ['Asset', str(intent.get('asset', 'N/A'))],
            ['Side', str(intent.get('side', 'N/A'))],
            ['Amount', str(intent.get('amount', 'N/A'))],
            ['Irreversible', 'Oui' if intent.get('irreversible') else 'Non'],
            ['Timestamp', datetime.fromtimestamp(intent.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S') if intent.get('timestamp') else 'N/A']
        ]
        
        intent_table = Table(intent_data, colWidths=[2.5*inch, 4*inch])
        intent_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9C27B0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(intent_table)
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(
        f"<para alignment='center' fontSize='8' textColor='#888888'>"
        f"Généré par Obsidia le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"© 2026 Obsidia - Gouvernance Transparente IA</para>",
        styles['Normal']
    ))
    
    doc.build(elements)
    output.seek(0)
    return output.getvalue()


def export_to_json(run_id: str, data: Dict[str, Any]) -> str:
    """Exporte les données d'un run au format JSON."""
    export_data = {
        "run_id": run_id,
        "export_date": datetime.now().isoformat(),
        "data": data
    }
    return json.dumps(export_data, indent=2, default=str)


def render_export_buttons(run_id: str, data: Dict[str, Any]):
    """Affiche les boutons d'export."""
    st.subheader("📤 Exporter le Rapport")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export Excel
        excel_data = export_to_excel(run_id, data)
        st.download_button(
            label="📊 Excel (.xlsx)",
            data=excel_data,
            file_name=f"obsidia_report_{run_id[:8]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        # Export PDF
        pdf_data = export_to_pdf(run_id, data)
        if pdf_data:
            st.download_button(
                label="📄 PDF (.pdf)",
                data=pdf_data,
                file_name=f"obsidia_report_{run_id[:8]}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col3:
        # Export JSON
        json_data = export_to_json(run_id, data)
        st.download_button(
            label="🗂️ JSON (.json)",
            data=json_data,
            file_name=f"obsidia_report_{run_id[:8]}.json",
            mime="application/json",
            use_container_width=True
        )
