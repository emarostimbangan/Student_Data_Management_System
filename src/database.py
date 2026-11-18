"""
SQLite Database Connection and Relational Schema Initialization.

Defines three normalized tables:
1. users       - Registrar/admin and faculty user accounts.
2. students    - Master academic records (student number, name, program, year level).
3. enrollments - Subject enrollment and grade records linked via foreign key.
"""

import sqlite3

DB_NAME = "student_management.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite connection with row factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """Initialize all required database tables if they do not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'faculty'))
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            program TEXT NOT NULL,
            year_level INTEGER NOT NULL CHECK(year_level BETWEEN 1 AND 5),
            email TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'graduated'))
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_code TEXT NOT NULL,
            course_title TEXT NOT NULL,
            units INTEGER NOT NULL DEFAULT 3,
            final_grade REAL,
            semester TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
        );
        """
    )

    conn.commit()
    conn.close()
