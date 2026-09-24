"""
db.py — SQLite schema + seeding for BHUMI-INSIGHT.
Same responsibility as in the original bhoominiti-ai repo: create the
database on first run and seed demo accounts + land data.
"""

import sqlite3
import os
import pandas as pd
import hashlib
import binascii

DB_PATH = os.path.join(os.path.dirname(__file__), "bhoominiti.db")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str, salt: bytes = None) -> str:
    """PBKDF2-HMAC-SHA256 password hashing (same approach as original repo)."""
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return binascii.hexlify(salt).decode() + "$" + binascii.hexlify(dk).decode()


def verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, hash_hex = stored.split("$")
        salt = binascii.unhexlify(salt_hex)
        expected = binascii.unhexlify(hash_hex)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
        return dk == expected
    except Exception:
        return False


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS land_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT NOT NULL,
            region TEXT,
            latitude REAL,
            longitude REAL,
            agricultural_pct REAL,
            forest_pct REAL,
            urban_pct REAL,
            wasteland_pct REAL,
            water_pct REAL,
            risk_score REAL,
            land_disputes INTEGER,
            total_parcels INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS policy_simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            state TEXT,
            irrigation_weight REAL,
            forest_weight REAL,
            urbanization_weight REAL,
            dispute_resolution_weight REAL,
            resulting_score REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    # Seed demo users if empty
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        demo_users = [
            ("Dr. R. Sharma", "researcher@bhumi.in", "demo123", "Researcher"),
            ("A. Verma", "policymaker@bhumi.in", "demo123", "Policymaker"),
            ("S. Nair", "admin@bhumi.in", "demo123", "Administrator"),
        ]
        for name, email, pw, role in demo_users:
            cur.execute(
                "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                (name, email, hash_password(pw), role),
            )
        conn.commit()

    # Seed land records from CSV if empty
    cur.execute("SELECT COUNT(*) FROM land_records")
    if cur.fetchone()[0] == 0:
        csv_path = os.path.join(DATA_DIR, "land_data.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df.to_sql("land_records", conn, if_exists="append", index=False)

    conn.close()


def get_land_records() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM land_records", conn)
    conn.close()
    return df


def get_user_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(name: str, email: str, password: str, role: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (name, email, hash_password(password), role),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def save_policy_simulation(user_email, state, irrigation, forest, urbanization, dispute, score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO policy_simulations
           (user_email, state, irrigation_weight, forest_weight, urbanization_weight, dispute_resolution_weight, resulting_score)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_email, state, irrigation, forest, urbanization, dispute, score),
    )
    conn.commit()
    conn.close()
