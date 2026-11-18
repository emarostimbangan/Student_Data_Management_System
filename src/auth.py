"""
User Authentication Module with SHA-256 Password Hashing.

Provides secure credential hashing, staff account registration, and
role-based login verification for 'admin' (Registrar) and 'faculty' roles.
"""

import hashlib
import sqlite3
from src.database import get_connection


def hash_password(password: str) -> str:
    """
    Generate a SHA-256 hexadecimal hash for a plain-text password.

    Args:
        password (str): Raw user password input.

    Returns:
        str: 64-character SHA-256 hex digest.
    """
    # Strip surrounding whitespace before encoding to UTF-8 bytes
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()


def register_user(username: str, password: str, role: str = "faculty") -> bool:
    """
    Create a new staff or registrar account in the users table.

    Args:
        username (str): Unique login identifier.
        password (str): Plain-text password to be hashed.
        role (str): Privilege level ('admin' or 'faculty').

    Returns:
        bool: True if account creation succeeded, False on invalid input or duplicate username.
    """
    clean_user = username.strip()
    clean_role = role.strip().lower()

    # Validate non-empty credentials and allowed system roles
    if not clean_user or not password.strip() or clean_role not in ("admin", "faculty"):
        return False

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (clean_user, hash_password(password), clean_role),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Triggers when username violates the UNIQUE table constraint
        return False
    finally:
        conn.close()


def login_user(username: str, password: str) -> dict | None:
    """
    Verify username and password hash against stored user accounts.

    Args:
        username (str): Account username.
        password (str): Plain-text password attempt.

    Returns:
        dict | None: Dictionary containing user_id, username, and role if valid; else None.
    """
    conn = get_connection()
    row = conn.execute(
        "SELECT user_id, username, role FROM users WHERE username = ? AND password_hash = ?",
        (username.strip(), hash_password(password)),
    ).fetchone()
    conn.close()
    return dict(row) if row else None
