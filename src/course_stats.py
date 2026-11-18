"""
Course-Level Grade Distribution and Pass/Fail Analytics Module.

Computes per-subject enrollment headcount, average numerical grade,
and pass rate across all graded course enrollments.
"""

from src.database import get_connection


def get_course_performance() -> list[dict]:
    """
    Aggregate enrollment count, average grade, and pass rate per course code.

    Returns:
        list[dict]: Course performance metrics sorted by course code.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT
            course_code,
            course_title,
            COUNT(*) AS total_enrolled,
            ROUND(AVG(final_grade), 2) AS avg_grade,
            SUM(CASE WHEN final_grade IS NOT NULL AND final_grade <= 3.00 THEN 1 ELSE 0 END) AS passed_count
        FROM enrollments
        GROUP BY course_code, course_title
        ORDER BY course_code ASC
        """
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
