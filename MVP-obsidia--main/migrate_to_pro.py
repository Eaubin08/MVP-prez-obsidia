#!/usr/bin/env python3
"""
Script de migration vers Obsidia Pro
====================================
Ce script effectue la migration de l'ancienne version démo vers la version Pro.

Actions effectuées:
1. Sauvegarde de l'ancien dashboard
2. Installation du nouveau dashboard Pro
3. Suppression des fichiers inutiles
4. Initialisation de la base de données
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

def print_header(text):
    """Affiche un header formaté."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    """Affiche un message de succès."""
    print(f"✅ {text}")

def print_warning(text):
    """Affiche un avertissement."""
    print(f"⚠️  {text}")

def print_error(text):
    """Affiche une erreur."""
    print(f"❌ {text}")

def backup_file(filepath):
    """Crée une sauvegarde d'un fichier."""
    if os.path.exists(filepath):
        backup_path = f"{filepath}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(filepath, backup_path)
        print_success(f"Sauvegarde créée: {backup_path}")
        return backup_path
    return None

def main():
    """Fonction principale de migration."""
    
    base_dir = Path(__file__).parent
    app_dir = base_dir / "app"
    views_dir = app_dir / "views"
    ui_dir = app_dir / "ui"
    
    print_header("MIGRATION VERS OBSIDIA PRO")
    print("\nCe script va migrer votre application vers la version Pro.")
    print("Actions: Sauvegarde → Installation → Nettoyage")
    
    input("\nAppuyez sur Entrée pour continuer...")
    
    # ============================================================
    # ÉTAPE 1: Sauvegarde
    # ============================================================
    print_header("ÉTAPE 1: Sauvegarde des fichiers existants")
    
    files_to_backup = [
        app_dir / "dashboard.py",
    ]
    
    for filepath in files_to_backup:
        backup_file(str(filepath))
    
    print_success("Sauvegardes créées avec succès!")
    
    # ============================================================
    # ÉTAPE 2: Installation du nouveau dashboard
    # ============================================================
    print_header("ÉTAPE 2: Installation du nouveau dashboard Pro")
    
    # Vérifier que dashboard_pro.py existe
    pro_dashboard = app_dir / "dashboard_pro.py"
    if not pro_dashboard.exists():
        print_error("dashboard_pro.py n'existe pas!")
        print("Assurez-vous d'avoir copié tous les fichiers du nouveau projet.")
        return
    
    # Remplacer l'ancien dashboard
    old_dashboard = app_dir / "dashboard.py"
    if old_dashboard.exists():
        os.remove(old_dashboard)
    
    # Copier le nouveau dashboard
    shutil.copy2(pro_dashboard, old_dashboard)
    print_success("Nouveau dashboard installé!")
    
    # ============================================================
    # ÉTAPE 3: Installation des modules
    # ============================================================
    print_header("ÉTAPE 3: Vérification des modules")
    
    required_modules = [
        app_dir / "database.py",
        app_dir / "auth.py",
        app_dir / "notifications.py",
        app_dir / "exporters.py",
    ]
    
    for module in required_modules:
        if module.exists():
            print_success(f"Module trouvé: {module.name}")
        else:
            print_error(f"Module manquant: {module.name}")
    
    # ============================================================
    # ÉTAPE 4: Nettoyage des fichiers inutiles
    # ============================================================
    print_header("ÉTAPE 4: Nettoyage des fichiers inutiles")
    
    files_to_remove = [
        # Vues de démo
        views_dir / "os0_invariants.py",
        views_dir / "os5_autorun.py",
        views_dir / "os6_exploration.py",
        views_dir / "guided_workflow.py",
        views_dir / "landing_page.py",
        views_dir / "domain_analytics.py",
        views_dir / "os4_reports.py",  # Remplacé par extended
        
        # UI complexes
        ui_dir / "mode_switcher.py",
        ui_dir / "expert_navigation.py",
        ui_dir / "console_x108.py",
        ui_dir / "actionable_messages.py",
        ui_dir / "messages.py",
        ui_dir / "enhanced.py",
        ui_dir / "documentation.py",
        
        # Anciens dashboards
        app_dir / "dashboard_new.py",
        app_dir / "router.py",
    ]
    
    removed_count = 0
    for filepath in files_to_remove:
        if filepath.exists():
            try:
                os.remove(filepath)
                print_success(f"Supprimé: {filepath.name}")
                removed_count += 1
            except Exception as e:
                print_error(f"Erreur lors de la suppression de {filepath.name}: {e}")
        else:
            print_warning(f"Déjà supprimé: {filepath.name}")
    
    print_success(f"{removed_count} fichiers supprimés!")
    
    # ============================================================
    # ÉTAPE 5: Initialisation de la base de données
    # ============================================================
    print_header("ÉTAPE 5: Initialisation de la base de données")
    
    try:
        from app.database import init_database
        init_database()
        print_success("Base de données initialisée!")
    except Exception as e:
        print_error(f"Erreur lors de l'initialisation de la base de données: {e}")
    
    # ============================================================
    # ÉTAPE 6: Vérification finale
    # ============================================================
    print_header("ÉTAPE 6: Vérification finale")
    
    checks = [
        (app_dir / "dashboard.py", "Dashboard principal"),
        (app_dir / "database.py", "Module base de données"),
        (app_dir / "auth.py", "Module authentification"),
        (app_dir / "notifications.py", "Module notifications"),
        (app_dir / "exporters.py", "Module exports"),
    ]
    
    all_ok = True
    for filepath, description in checks:
        if filepath.exists():
            print_success(f"✓ {description}")
        else:
            print_error(f"✗ {description} manquant!")
            all_ok = False
    
    # ============================================================
    # RÉSUMÉ
    # ============================================================
    print_header("MIGRATION TERMINÉE")
    
    if all_ok:
        print_success("Tous les fichiers sont en place!")
        print("\n📋 Prochaines étapes:")
        print("   1. Installez les nouvelles dépendances:")
        print("      pip install -r requirements.txt")
        print("\n   2. Lancez l'application:")
        print("      streamlit run app/dashboard.py")
        print("\n   3. Connectez-vous avec:")
        print("      Nom d'utilisateur: admin")
        print("      Mot de passe: admin123")
        print("\n   4. Configurez les notifications SMTP (optionnel)")
        print("      dans la page Paramètres > Notifications")
    else:
        print_error("Certains fichiers sont manquants!")
        print("Veuillez vérifier l'installation.")

if __name__ == "__main__":
    main()
