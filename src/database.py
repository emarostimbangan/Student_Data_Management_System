"""
SQLite Database Connection and Relational Schema Initialization.

Establishes a normalized three-table SQLite database for managing student
academic records, staff authentication, and course enrollments with strict
foreign-key integrity.
"""

import sqlite3

# Local SQLite database filename stored in the project root
DB_NAME = "student_management.db"


def get_connection() -> sqlite3.Connection:
    """
    Open a SQLite connection with dictionary-style row access and foreign keys enabled.

    Returns:
        sqlite3.Connection: Active database connection object.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    # Enforce ON DELETE CASCADE and foreign-key constraints on every connection
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """
    Create the users, students, and enrollments tables if they do not exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Table 1: Staff and registrar user accounts with role-based permissions
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

    # Table 2: Master student profile directory
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

    # Table 3: Subject enrollments and numerical grades linked to students
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
