"""
Academic Analytics and Program Enrollment Reporting Module.

Computes institutional summary metrics—including total students, active
headcount, graduated count, total course enrollments, and institutional
average grade—alongside per-program headcount distributions.
"""

from src.database import get_connection


def get_academic_summary() -> dict:
    """
    Aggregate institutional headcount, course enrollment volume, and average grade.

    Returns:
        dict: Summary metrics dictionary for administrative reporting.
    """
    conn = get_connection()
    # Query total, active, and graduated student counts
    total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    active = conn.execute("SELECT COUNT(*) FROM students WHERE status = 'active'").fetchone()[0]
    grad = conn.execute("SELECT COUNT(*) FROM students WHERE status = 'graduated'").fetchone()[0]

    # Query total enrolled subject rows and average numerical grade across graded rows
    enrolls = conn.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0]
    avg = conn.execute("SELECT AVG(final_grade) FROM enrollments WHERE final_grade IS NOT NULL").fetchone()[0]
    conn.close()

    return {
        "total_students": total,
        "active_students": active,
        "graduated_students": grad,
        "total_enrollments": enrolls,
        "average_grade": round(avg, 2) if avg is not None else None,
    }


def get_program_distribution() -> list[dict]:
    """
    Group students by academic degree program ordered from largest to smallest.

    Returns:
        list[dict]: List of dictionaries containing 'program' and 'student_count'.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT program, COUNT(*) AS student_count
        FROM students
        GROUP BY program
        ORDER BY student_count DESC
        """
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
