"""Student Profile Management (CRUD) Module."""
import sqlite3
from src.database import get_connection


def add_student(student_number: str, full_name: str, program: str, year_level: int, email: str) -> bool:
    """Insert a new student record into the master directory."""
    if not student_number.strip() or not full_name.strip() or not program.strip() or not (1 <= year_level <= 5):
        return False
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO students (student_number, full_name, program, year_level, email, status) VALUES (?, ?, ?, ?, ?, 'active')",
            (student_number.strip(), full_name.strip(), program.strip(), year_level, email.strip()),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def list_students() -> list[dict]:
    """Retrieve all student profiles ordered by full name."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students ORDER BY full_name ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_students(keyword: str) -> list[dict]:
    """Search students by student number, full name, or academic program."""
    term = f"%{keyword.strip()}%"
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM students WHERE student_number LIKE ? OR full_name LIKE ? OR program LIKE ? ORDER BY full_name ASC",
        (term, term, term),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_student_status(student_id: int, year_level: int, status: str) -> bool:
    """Update a student's year level and enrollment status."""
    status = status.strip().lower()
    if status not in ("active", "inactive", "graduated") or not (1 <= year_level <= 5):
        return False
    conn = get_connection()
    cur = conn.execute("UPDATE students SET year_level = ?, status = ? WHERE student_id = ?", (year_level, status, student_id))
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def delete_student(student_id: int) -> bool:
    """Delete a student record and cascade-remove associated enrollments."""
    conn = get_connection()
    cur = conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0
