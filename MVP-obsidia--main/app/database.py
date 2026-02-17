"""
Module de base de données pour Obsidia
======================================
Gestion de l'historique des runs, utilisateurs et artefacts.
"""
import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import pandas as pd

DB_PATH = Path(__file__).parent.parent / "data" / "obsidia.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_database():
    """Initialise la base de données avec les tables nécessaires."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table des utilisateurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    """)
    
    # Table des runs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            domain TEXT NOT NULL,
            seed INTEGER,
            tau REAL,
            status TEXT DEFAULT 'running',
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            final_decision TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Table des features
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            volatility REAL,
            coherence REAL,
            friction REAL,
            regime TEXT,
            computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        )
    """)
    
    # Table des simulations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            mu REAL,
            sigma REAL,
            p_ruin REAL,
            p_dd REAL,
            cvar_95 REAL,
            verdict TEXT,
            n_sims INTEGER,
            horizon INTEGER,
            computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        )
    """)
    
    # Table des décisions (gates)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            gate1_ok BOOLEAN,
            gate1_reason TEXT,
            gate2_ok BOOLEAN,
            gate2_reason TEXT,
            gate3_ok BOOLEAN,
            gate3_reason TEXT,
            final_decision TEXT,
            decision_reason TEXT,
            decided_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        )
    """)
    
    # Table des intents
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            asset TEXT,
            side TEXT,
            amount REAL,
            irreversible BOOLEAN,
            timestamp REAL,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        )
    """)
    
    # Table des notifications
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            run_id TEXT NOT NULL,
            type TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT 0,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        )
    """)
    
    # Créer l'utilisateur admin par défaut (password: admin123)
    admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    """, ("admin", "admin@obsidia.local", admin_hash, "admin"))
    
    conn.commit()
    conn.close()


# ============================================================
# FONCTIONS UTILISATEURS
# ============================================================

def create_user(username: str, email: str, password: str, role: str = "user") -> bool:
    """Crée un nouvel utilisateur."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, (username, email, password_hash, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authentifie un utilisateur et retourne ses infos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute("""
        SELECT id, username, email, role, created_at
        FROM users
        WHERE username = ? AND password_hash = ? AND is_active = 1
    """, (username, password_hash))
    
    result = cursor.fetchone()
    
    if result:
        # Mettre à jour last_login
        cursor.execute("""
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
        """, (result[0],))
        conn.commit()
        
        conn.close()
        return {
            "id": result[0],
            "username": result[1],
            "email": result[2],
            "role": result[3],
            "created_at": result[4]
        }
    
    conn.close()
    return None


def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Récupère un utilisateur par son ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, username, email, role, created_at, last_login
        FROM users WHERE id = ?
    """, (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "id": result[0],
            "username": result[1],
            "email": result[2],
            "role": result[3],
            "created_at": result[4],
            "last_login": result[5]
        }
    return None


def get_all_users() -> List[Dict]:
    """Récupère tous les utilisateurs."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, username, email, role, created_at, last_login, is_active
        FROM users ORDER BY created_at DESC
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": r[0],
            "username": r[1],
            "email": r[2],
            "role": r[3],
            "created_at": r[4],
            "last_login": r[5],
            "is_active": r[6]
        }
        for r in results
    ]


# ============================================================
# FONCTIONS RUNS
# ============================================================

def create_run(run_id: str, user_id: Optional[int], domain: str, seed: int, tau: float) -> bool:
    """Crée un nouveau run."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO runs (run_id, user_id, domain, seed, tau)
            VALUES (?, ?, ?, ?, ?)
        """, (run_id, user_id, domain, seed, tau))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def complete_run(run_id: str, final_decision: str) -> bool:
    """Marque un run comme complété."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE runs 
        SET status = 'completed', completed_at = CURRENT_TIMESTAMP, final_decision = ?
        WHERE run_id = ?
    """, (final_decision, run_id))
    
    conn.commit()
    conn.close()
    return True


def get_run(run_id: str) -> Optional[Dict]:
    """Récupère un run par son ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.*, u.username
        FROM runs r
        LEFT JOIN users u ON r.user_id = u.id
        WHERE r.run_id = ?
    """, (run_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "id": result[0],
            "run_id": result[1],
            "user_id": result[2],
            "domain": result[3],
            "seed": result[4],
            "tau": result[5],
            "status": result[6],
            "started_at": result[7],
            "completed_at": result[8],
            "final_decision": result[9],
            "username": result[10]
        }
    return None


def get_user_runs(user_id: int, limit: int = 50) -> List[Dict]:
    """Récupère les runs d'un utilisateur."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT run_id, domain, seed, tau, status, started_at, completed_at, final_decision
        FROM runs
        WHERE user_id = ?
        ORDER BY started_at DESC
        LIMIT ?
    """, (user_id, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "run_id": r[0],
            "domain": r[1],
            "seed": r[2],
            "tau": r[3],
            "status": r[4],
            "started_at": r[5],
            "completed_at": r[6],
            "final_decision": r[7]
        }
        for r in results
    ]


def get_all_runs(limit: int = 100) -> pd.DataFrame:
    """Récupère tous les runs sous forme de DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    
    query = """
        SELECT 
            r.run_id,
            u.username,
            r.domain,
            r.seed,
            r.tau,
            r.status,
            r.started_at,
            r.completed_at,
            r.final_decision
        FROM runs r
        LEFT JOIN users u ON r.user_id = u.id
        ORDER BY r.started_at DESC
        LIMIT ?
    """
    
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    
    return df


# ============================================================
# FONCTIONS FEATURES
# ============================================================

def save_features(run_id: str, features: Dict[str, Any]) -> bool:
    """Sauvegarde les features d'un run."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO features (run_id, volatility, coherence, friction, regime)
        VALUES (?, ?, ?, ?, ?)
    """, (
        run_id,
        features.get("volatility"),
        features.get("coherence"),
        features.get("friction"),
        features.get("regime")
    ))
    
    conn.commit()
    conn.close()
    return True


def get_features(run_id: str) -> Optional[Dict]:
    """Récupère les features d'un run."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT volatility, coherence, friction, regime, computed_at
        FROM features WHERE run_id = ?
    """, (run_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "volatility": result[0],
            "coherence": result[1],
            "friction": result[2],
            "regime": result[3],
            "computed_at": result[4]
        }
    return None


# ============================================================
# FONCTIONS SIMULATIONS
# ============================================================

def save_simulation(run_id: str, sim_result: Dict[str, Any]) -> bool:
    """Sauvegarde les résultats de simulation."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO simulations 
        (run_id, mu, sigma, p_ruin, p_dd, cvar_95, verdict, n_sims, horizon)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run_id,
        sim_result.get("mu"),
        sim_result.get("sigma"),
        sim_result.get("p_ruin"),
        sim_result.get("p_dd"),
        sim_result.get("cvar_95"),
        sim_result.get("verdict"),
        sim_result.get("n_sims"),
        sim_result.get("horizon")
    ))
    
    conn.commit()
    conn.close()
    return True


def get_simulation(run_id: str) -> Optional[Dict]:
    """Récupère les résultats de simulation d'un run."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT mu, sigma, p_ruin, p_dd, cvar_95, verdict, n_sims, horizon, computed_at
        FROM simulations WHERE run_id = ?
    """, (run_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "mu": result[0],
            "sigma": result[1],
            "p_ruin": result[2],
            "p_dd": result[3],
            "cvar_95": result[4],
            "verdict": result[5],
            "n_sims": result[6],
            "horizon": result[7],
            "computed_at": result[8]
        }
    return None


# ============================================================
# FONCTIONS DÉCISIONS
# ============================================================

def save_decision(run_id: str, gates_result: Dict[str, Any]) -> bool:
    """Sauvegarde la décision des gates."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    gate1 = gates_result.get("gate1", {})
    gate2 = gates_result.get("gate2", {})
    gate3 = gates_result.get("gate3", {})
    
    cursor.execute("""
        INSERT INTO decisions 
        (run_id, gate1_ok, gate1_reason, gate2_ok, gate2_reason, 
         gate3_ok, gate3_reason, final_decision, decision_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run_id,
        gate1.get("ok"),
        gate1.get("reason"),
        gate2.get("ok"),
        gate2.get("reason"),
        gate3.get("ok"),
        gate3.get("reason"),
        gates_result.get("decision"),
        gates_result.get("reason")
    ))
    
    conn.commit()
    conn.close()
    return True


def get_decision(run_id: str) -> Optional[Dict]:
    """Récupère la décision d'un run."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT gate1_ok, gate1_reason, gate2_ok, gate2_reason,
               gate3_ok, gate3_reason, final_decision, decision_reason, decided_at
        FROM decisions WHERE run_id = ?
    """, (run_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "gate1": {"ok": result[0], "reason": result[1]},
            "gate2": {"ok": result[2], "reason": result[3]},
            "gate3": {"ok": result[4], "reason": result[5]},
            "decision": result[6],
            "reason": result[7],
            "decided_at": result[8]
        }
    return None


# ============================================================
# FONCTIONS INTENTS
# ============================================================

def save_intent(run_id: str, intent: Dict[str, Any]) -> bool:
    """Sauvegarde un intent ERC-8004."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO intents (run_id, asset, side, amount, irreversible, timestamp, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        run_id,
        intent.get("asset"),
        intent.get("side"),
        intent.get("amount"),
        intent.get("irreversible"),
        intent.get("timestamp"),
        json.dumps(intent.get("metadata", {}))
    ))
    
    conn.commit()
    conn.close()
    return True


def get_intent(run_id: str) -> Optional[Dict]:
    """Récupère l'intent d'un run."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT asset, side, amount, irreversible, timestamp, metadata, created_at
        FROM intents WHERE run_id = ?
    """, (run_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "asset": result[0],
            "side": result[1],
            "amount": result[2],
            "irreversible": result[3],
            "timestamp": result[4],
            "metadata": json.loads(result[5]) if result[5] else {},
            "created_at": result[6]
        }
    return None


# ============================================================
# FONCTIONS NOTIFICATIONS
# ============================================================

def create_notification(user_id: int, run_id: str, notif_type: str, message: str) -> bool:
    """Crée une notification pour un utilisateur."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO notifications (user_id, run_id, type, message)
        VALUES (?, ?, ?, ?)
    """, (user_id, run_id, notif_type, message))
    
    conn.commit()
    conn.close()
    return True


def get_notifications(user_id: int, unread_only: bool = False) -> List[Dict]:
    """Récupère les notifications d'un utilisateur."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """
        SELECT n.id, n.run_id, n.type, n.message, n.is_read, n.sent_at, r.final_decision
        FROM notifications n
        LEFT JOIN runs r ON n.run_id = r.run_id
        WHERE n.user_id = ?
    """
    
    if unread_only:
        query += " AND n.is_read = 0"
    
    query += " ORDER BY n.sent_at DESC"
    
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": r[0],
            "run_id": r[1],
            "type": r[2],
            "message": r[3],
            "is_read": r[4],
            "sent_at": r[5],
            "final_decision": r[6]
        }
        for r in results
    ]


def mark_notification_read(notification_id: int) -> bool:
    """Marque une notification comme lue."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE notifications SET is_read = 1 WHERE id = ?
    """, (notification_id,))
    
    conn.commit()
    conn.close()
    return True


def get_unread_count(user_id: int) -> int:
    """Compte les notifications non lues."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0
    """, (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else 0


# ============================================================
# STATISTIQUES
# ============================================================

def get_statistics() -> Dict[str, Any]:
    """Récupère les statistiques globales."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    stats = {}
    
    # Nombre total de runs
    cursor.execute("SELECT COUNT(*) FROM runs")
    stats["total_runs"] = cursor.fetchone()[0]
    
    # Nombre d'utilisateurs
    cursor.execute("SELECT COUNT(*) FROM users")
    stats["total_users"] = cursor.fetchone()[0]
    
    # Répartition des décisions
    cursor.execute("""
        SELECT final_decision, COUNT(*) 
        FROM runs 
        WHERE final_decision IS NOT NULL
        GROUP BY final_decision
    """)
    stats["decisions"] = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Runs aujourd'hui
    cursor.execute("""
        SELECT COUNT(*) FROM runs 
        WHERE date(started_at) = date('now')
    """)
    stats["runs_today"] = cursor.fetchone()[0]
    
    # Dernier run
    cursor.execute("""
        SELECT run_id, started_at, final_decision 
        FROM runs 
        ORDER BY started_at DESC 
        LIMIT 1
    """)
    result = cursor.fetchone()
    stats["last_run"] = {
        "run_id": result[0],
        "started_at": result[1],
        "final_decision": result[2]
    } if result else None
    
    conn.close()
    return stats


# Initialiser la base de données au chargement
init_database()
