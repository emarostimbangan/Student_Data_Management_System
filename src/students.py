"""
Student Profile Management (CRUD) Module.

Handles creating student records, listing the master student directory,
searching by student number, full name, or academic program, updating
year levels and enrollment status, and deleting records with cascade cleanup.
"""

import sqlite3
from src.database import get_connection


def add_student(
    student_number: str,
    full_name: str,
    program: str,
    year_level: int,
    email: str,
) -> bool:
    """
    Insert a new student profile into the master directory.

    Args:
        student_number (str): Unique institutional ID (e.g., 2026-1001).
        full_name (str): Complete student name.
        program (str): Degree program (e.g., BS Computer Science).
        year_level (int): Academic year level between 1 and 5.
        email (str): Student institutional or personal email address.

    Returns:
        bool: True if saved successfully, False on validation error or duplicate ID.
    """
    # Validate required fields and ensure year level stays within 1-5
    if not student_number.strip() or not full_name.strip() or not program.strip():
        return False
    if not (1 <= year_level <= 5):
        return False

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO students (student_number, full_name, program, year_level, email, status)
            VALUES (?, ?, ?, ?, ?, 'active')
            """,
            (
                student_number.strip(),
                full_name.strip(),
                program.strip(),
                year_level,
                email.strip(),
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Reject duplicate student_number values
        return False
    finally:
        conn.close()


def list_students() -> list[dict]:
    """
    Retrieve all student records sorted alphabetically by full name.

    Returns:
        list[dict]: List of student dictionaries.
    """
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students ORDER BY full_name ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_students(keyword: str) -> list[dict]:
    """
    Filter students matching a keyword across student number, name, or program.

    Args:
        keyword (str): Case-insensitive search term.

    Returns:
        list[dict]: Matching student dictionaries.
    """
    # Wrap keyword with SQL wildcards for partial substring matching
    term = f"%{keyword.strip()}%"
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM students
        WHERE student_number LIKE ? OR full_name LIKE ? OR program LIKE ?
        ORDER BY full_name ASC
        """,
        (term, term, term),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_student_status(student_id: int, year_level: int, status: str) -> bool:
    """
    Modify a student's academic year level and enrollment status.

    Args:
        student_id (int): Primary key ID of the student.
        year_level (int): Updated year level (1-5).
        status (str): Must be 'active', 'inactive', or 'graduated'.

    Returns:
        bool: True if a matching student row was updated.
    """
    clean_status = status.strip().lower()
    if clean_status not in ("active", "inactive", "graduated") or not (1 <= year_level <= 5):
        return False

    conn = get_connection()
    cur = conn.execute(
        "UPDATE students SET year_level = ?, status = ? WHERE student_id = ?",
        (year_level, clean_status, student_id),
    )
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def delete_student(student_id: int) -> bool:
    """
    Remove a student record and cascade-delete associated course enrollments.

    Args:
        student_id (int): Primary key ID of the student to remove.

    Returns:
        bool: True if the record existed and was deleted.
    """
    conn = get_connection()
    cur = conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0
