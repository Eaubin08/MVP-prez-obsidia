"""
Module d'authentification pour Obsidia
======================================
Gestion des sessions utilisateurs et contrôle d'accès.
"""
import streamlit as st
from functools import wraps
from typing import Optional, Callable
from app.database import authenticate_user, get_user_by_id


def init_auth_session():
    """Initialise les variables de session pour l'authentification."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None


def login(username: str, password: str) -> bool:
    """Tente de connecter un utilisateur."""
    user = authenticate_user(username, password)
    
    if user:
        st.session_state["authenticated"] = True
        st.session_state["user"] = user
        return True
    return False


def logout():
    """Déconnecte l'utilisateur courant."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None


def is_authenticated() -> bool:
    """Vérifie si un utilisateur est authentifié."""
    return st.session_state.get("authenticated", False)


def get_current_user() -> Optional[dict]:
    """Récupère l'utilisateur courant."""
    return st.session_state.get("user")


def require_auth(func: Callable) -> Callable:
    """Décorateur pour protéger une fonction (nécessite authentification)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.warning("🔒 Veuillez vous connecter pour accéder à cette page.")
            render_login_form()
            return
        return func(*args, **kwargs)
    return wrapper


def require_admin(func: Callable) -> Callable:
    """Décorateur pour protéger une fonction (nécessite rôle admin)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            st.warning("🔒 Veuillez vous connecter pour accéder à cette page.")
            render_login_form()
            return
        
        user = get_current_user()
        if user.get("role") != "admin":
            st.error("🚫 Accès refusé. Cette page nécessite les privilèges administrateur.")
            return
        
        return func(*args, **kwargs)
    return wrapper


def render_login_form():
    """Affiche le formulaire de connexion."""
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <div style="font-size: 60px; margin-bottom: 20px;">🏛️</div>
        <h1 style="color: #7c9fff; margin-bottom: 10px;">OBSIDIA</h1>
        <p style="color: #888;">Plateforme de Gouvernance IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("🔐 Connexion")
            
            username = st.text_input("Nom d'utilisateur", placeholder="admin")
            password = st.text_input("Mot de passe", type="password", placeholder="admin123")
            
            submitted = st.form_submit_button("Se connecter", use_container_width=True, type="primary")
            
            if submitted:
                if login(username, password):
                    st.success("✅ Connexion réussie !")
                    st.rerun()
                else:
                    st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")
        
        st.info("💡 **Compte par défaut** : admin / admin123")


def render_user_menu():
    """Affiche le menu utilisateur dans la sidebar."""
    user = get_current_user()
    
    if user:
        st.sidebar.markdown("---")
        st.sidebar.markdown("#### 👤 Utilisateur")
        
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.markdown(f"**{user['username']}**")
            st.caption(f"Rôle: {user['role']}")
        
        with col2:
            if st.button("🚪", key="logout_btn", help="Déconnexion"):
                logout()
                st.rerun()


def render_register_form():
    """Affiche le formulaire d'inscription (admin uniquement)."""
    st.subheader("📝 Créer un nouvel utilisateur")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input("Nom d'utilisateur")
            new_email = st.text_input("Email")
        
        with col2:
            new_password = st.text_input("Mot de passe", type="password")
            confirm_password = st.text_input("Confirmer le mot de passe", type="password")
        
        role = st.selectbox("Rôle", ["user", "admin"], index=0)
        
        submitted = st.form_submit_button("Créer l'utilisateur", type="primary")
        
        if submitted:
            if not all([new_username, new_email, new_password]):
                st.error("❌ Tous les champs sont obligatoires.")
            elif new_password != confirm_password:
                st.error("❌ Les mots de passe ne correspondent pas.")
            elif len(new_password) < 6:
                st.error("❌ Le mot de passe doit contenir au moins 6 caractères.")
            else:
                from app.database import create_user
                if create_user(new_username, new_email, new_password, role):
                    st.success(f"✅ Utilisateur '{new_username}' créé avec succès !")
                else:
                    st.error("❌ Ce nom d'utilisateur ou email existe déjà.")


# Initialiser l'authentification au chargement
init_auth_session()
