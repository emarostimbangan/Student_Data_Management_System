"""
Course-Level Grade Distribution and Pass/Fail Analytics Module.

Computes per-subject enrollment headcount, average numerical grade,
passing student counts, and pass-rate percentages across all graded
course enrollments in the SQLite database.
"""

from src.database import get_connection

# Passing grade ceiling on the 1.00–5.00 Philippine university scale (1.00 = highest, 3.00 = passing)
PASSING_GRADE_LIMIT = 3.00


def get_course_performance() -> list[dict]:
    """
    Aggregate enrollment count, average grade, and pass count per course code.

    Returns:
        list[dict]: Course performance dictionaries ordered alphabetically by course code.
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT
            course_code,
            course_title,
            COUNT(*) AS total_enrolled,
            ROUND(AVG(final_grade), 2) AS avg_grade,
            SUM(CASE WHEN final_grade IS NOT NULL AND final_grade <= ? THEN 1 ELSE 0 END) AS passed_count,
            SUM(CASE WHEN final_grade IS NOT NULL AND final_grade > ? THEN 1 ELSE 0 END) AS failed_count
        FROM enrollments
        GROUP BY course_code, course_title
        ORDER BY course_code ASC
        """,
        (PASSING_GRADE_LIMIT, PASSING_GRADE_LIMIT),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_top_performing_courses(limit: int = 5) -> list[dict]:
    """
    Return the top-performing subjects ranked by lowest (best) average grade.

    Args:
        limit (int): Maximum number of courses to return.

    Returns:
        list[dict]: Graded course summaries ordered from highest academic performance upward.
    """
    graded = [c for c in get_course_performance() if c["avg_grade"] is not None]
    graded.sort(key=lambda item: item["avg_grade"])
    return graded[:limit]
