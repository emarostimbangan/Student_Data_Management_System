"""Academic Analytics and Program Enrollment Reporting Module."""
from src.database import get_connection


def get_academic_summary() -> dict:
    """Compute aggregate student counts, enrollments, and average GPA."""
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    active = conn.execute("SELECT COUNT(*) FROM students WHERE status = 'active'").fetchone()[0]
    grad = conn.execute("SELECT COUNT(*) FROM students WHERE status = 'graduated'").fetchone()[0]
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
    """Return student headcount grouped by academic degree program."""
    conn = get_connection()
    rows = conn.execute("SELECT program, COUNT(*) AS student_count FROM students GROUP BY program ORDER BY student_count DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
