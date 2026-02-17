"""
Module de notifications pour Obsidia
====================================
Envoi d'emails et notifications lors des décisions EXECUTE.
"""
import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any, Optional
from app.database import create_notification, get_user_by_id


# Configuration SMTP (à configurer selon votre serveur)
SMTP_CONFIG = {
    "enabled": False,  # Mettre à True pour activer les emails
    "host": "smtp.gmail.com",
    "port": 587,
    "username": "",
    "password": "",
    "from_email": "notifications@obsidia.local",
    "from_name": "Obsidia Notifications"
}


def configure_smtp(host: str, port: int, username: str, password: str, from_email: str):
    """Configure les paramètres SMTP."""
    SMTP_CONFIG["enabled"] = True
    SMTP_CONFIG["host"] = host
    SMTP_CONFIG["port"] = port
    SMTP_CONFIG["username"] = username
    SMTP_CONFIG["password"] = password
    SMTP_CONFIG["from_email"] = from_email


def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Envoie un email."""
    if not SMTP_CONFIG["enabled"]:
        st.warning("📧 Les notifications email sont désactivées.")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
        msg['To'] = to_email
        
        # Version HTML
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connexion et envoi
        with smtplib.SMTP(SMTP_CONFIG["host"], SMTP_CONFIG["port"]) as server:
            server.starttls()
            server.login(SMTP_CONFIG["username"], SMTP_CONFIG["password"])
            server.send_message(msg)
        
        return True
    except Exception as e:
        st.error(f"❌ Erreur d'envoi d'email: {str(e)}")
        return False


def generate_execute_email_template(run_id: str, intent: Dict[str, Any], 
                                    features: Dict[str, Any], 
                                    decision: Dict[str, Any]) -> str:
    """Génère le template HTML pour l'email EXECUTE."""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #4CAF50, #45a049); color: white; 
                      padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .section {{ margin-bottom: 20px; padding: 15px; background: white; 
                       border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            .success-badge {{ background: #4CAF50; color: white; padding: 8px 16px; 
                            border-radius: 20px; display: inline-block; font-weight: bold; }}
            .metric {{ display: inline-block; margin: 5px 10px; padding: 8px 12px; 
                     background: #e3f2fd; border-radius: 4px; }}
            .footer {{ text-align: center; padding: 20px; color: #888; font-size: 12px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #f5f5f5; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏛️ OBSIDIA</h1>
                <p>Notification de Décision - Intent Approuvé</p>
            </div>
            
            <div class="content">
                <div style="text-align: center; margin-bottom: 20px;">
                    <span class="success-badge">✅ EXECUTE - Intent Approuvé</span>
                </div>
                
                <div class="section">
                    <h3>📋 Détails de l'Intent</h3>
                    <table>
                        <tr><th>Run ID</th><td>#{run_id[:8]}</td></tr>
                        <tr><th>Asset</th><td>{intent.get('asset', 'N/A')}</td></tr>
                        <tr><th>Side</th><td>{intent.get('side', 'N/A')}</td></tr>
                        <tr><th>Amount</th><td>{intent.get('amount', 'N/A')}</td></tr>
                        <tr><th>Irreversible</th><td>{'Oui' if intent.get('irreversible') else 'Non'}</td></tr>
                        <tr><th>Timestamp</th><td>{datetime.fromtimestamp(intent.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
                    </table>
                </div>
                
                <div class="section">
                    <h3>📊 Features du Marché</h3>
                    <div>
                        <span class="metric">Volatility: {features.get('volatility', 'N/A'):.4f}</span>
                        <span class="metric">Coherence: {features.get('coherence', 'N/A'):.4f}</span>
                        <span class="metric">Friction: {features.get('friction', 'N/A'):.4f}</span>
                        <span class="metric">Regime: {features.get('regime', 'N/A')}</span>
                    </div>
                </div>
                
                <div class="section">
                    <h3>🚦 Évaluation des Gates</h3>
                    <table>
                        <tr>
                            <th>Gate</th>
                            <th>Status</th>
                            <th>Raison</th>
                        </tr>
                        <tr>
                            <td>Gate 1 - Integrity</td>
                            <td>{'✅ PASS' if decision.get('gate1', {}).get('ok') else '❌ FAIL'}</td>
                            <td>{decision.get('gate1', {}).get('reason', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Gate 2 - X-108</td>
                            <td>{'✅ PASS' if decision.get('gate2', {}).get('ok') else '⏳ HOLD'}</td>
                            <td>{decision.get('gate2', {}).get('reason', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Gate 3 - Risk</td>
                            <td>{'✅ PASS' if decision.get('gate3', {}).get('ok') else '❌ FAIL'}</td>
                            <td>{decision.get('gate3', {}).get('reason', 'N/A')}</td>
                        </tr>
                    </table>
                </div>
                
                <div class="section">
                    <h3>📝 Décision Finale</h3>
                    <p><strong>Décision:</strong> {decision.get('decision', 'N/A')}</p>
                    <p><strong>Raison:</strong> {decision.get('reason', 'N/A')}</p>
                </div>
            </div>
            
            <div class="footer">
                <p>Cet email a été généré automatiquement par Obsidia</p>
                <p>© 2026 Obsidia - Gouvernance Transparente IA</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html


def notify_execute_decision(user_id: int, run_id: str, intent: Dict[str, Any],
                            features: Dict[str, Any], decision: Dict[str, Any]) -> bool:
    """Notifie l'utilisateur d'une décision EXECUTE."""
    
    # Créer notification dans la base de données
    message = f"Intent {intent.get('side')} {intent.get('asset')} approuvé - Run #{run_id[:8]}"
    create_notification(user_id, run_id, "execute", message)
    
    # Envoyer email si configuré
    if SMTP_CONFIG["enabled"]:
        user = get_user_by_id(user_id)
        if user and user.get("email"):
            subject = f"[Obsidia] Intent Approuvé - {intent.get('side')} {intent.get('asset')}"
            html_content = generate_execute_email_template(run_id, intent, features, decision)
            return send_email(user["email"], subject, html_content)
    
    return True


def render_notification_bell(user_id: int):
    """Affiche l'icône de notification avec le nombre de non-lues."""
    from app.database import get_unread_count
    
    unread = get_unread_count(user_id)
    
    if unread > 0:
        st.markdown(f"""
        <div style="
            position: relative;
            display: inline-block;
        ">
            <span style="font-size: 20px;">🔔</span>
            <span style="
                position: absolute;
                top: -5px;
                right: -5px;
                background: #f44336;
                color: white;
                border-radius: 50%;
                padding: 2px 6px;
                font-size: 10px;
                font-weight: bold;
            ">{unread}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<span style='font-size: 20px;'>🔔</span>", unsafe_allow_html=True)


def render_notifications_panel(user_id: int):
    """Affiche le panneau des notifications."""
    from app.database import get_notifications, mark_notification_read
    
    st.subheader("📬 Notifications")
    
    notifications = get_notifications(user_id)
    
    if not notifications:
        st.info("Aucune notification.")
        return
    
    for notif in notifications:
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])
            
            with col1:
                icon = "✅" if notif["type"] == "execute" else "📧"
                bg_color = "#e8f5e9" if notif["is_read"] else "#fff3e0"
                
                st.markdown(f"""
                <div style="
                    background: {bg_color};
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 5px;
                ">
                    <strong>{icon} {notif['type'].upper()}</strong><br>
                    <small>{notif['message']}</small><br>
                    <small style="color: #888;">{notif['sent_at']}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if not notif["is_read"]:
                    if st.button("✓ Lu", key=f"mark_read_{notif['id']}"):
                        mark_notification_read(notif["id"])
                        st.rerun()
            
            with col3:
                if st.button("🗑️", key=f"delete_notif_{notif['id']}"):
                    # TODO: Implémenter la suppression
                    pass


def render_smtp_config():
    """Affiche le formulaire de configuration SMTP."""
    st.subheader("⚙️ Configuration SMTP")
    
    with st.form("smtp_config"):
        col1, col2 = st.columns(2)
        
        with col1:
            host = st.text_input("Serveur SMTP", value=SMTP_CONFIG["host"])
            port = st.number_input("Port", value=SMTP_CONFIG["port"], min_value=1, max_value=65535)
            username = st.text_input("Nom d'utilisateur")
        
        with col2:
            password = st.text_input("Mot de passe", type="password")
            from_email = st.text_input("Email expéditeur", value=SMTP_CONFIG["from_email"])
        
        submitted = st.form_submit_button("Sauvegarder", type="primary")
        
        if submitted:
            configure_smtp(host, port, username, password, from_email)
            st.success("✅ Configuration SMTP sauvegardée !")
    
    # Test d'envoi
    st.markdown("---")
    st.subheader("🧪 Test d'envoi")
    
    test_email = st.text_input("Email de test")
    if st.button("Envoyer un email de test"):
        if test_email:
            subject = "[Obsidia] Test de notification"
            html = "<h1>Test réussi !</h1><p>Votre configuration SMTP fonctionne correctement.</p>"
            if send_email(test_email, subject, html):
                st.success("✅ Email de test envoyé !")
        else:
            st.error("❌ Veuillez entrer un email de test.")
