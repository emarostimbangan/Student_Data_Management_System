"""
User Authentication Module with SHA-256 Password Hashing.

Supports account registration and role-based login ('admin' or 'faculty').
"""

import hashlib
import sqlite3
from src.database import get_connection


def hash_password(password: str) -> str:
    """Return a SHA-256 hexadecimal digest for a plain-text password."""
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()


def register_user(username: str, password: str, role: str = "faculty") -> bool:
    """Register a new system account with 'admin' or 'faculty' privileges."""
    username = username.strip()
    role = role.strip().lower()
    if not username or not password.strip() or role not in ("admin", "faculty"):
        return False

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hash_password(password), role),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username: str, password: str) -> dict | None:
    """Authenticate credentials and return user dictionary if valid."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, username, role FROM users WHERE username = ? AND password_hash = ?",
        (username.strip(), hash_password(password)),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
