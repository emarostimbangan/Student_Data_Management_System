"""Course Enrollment and Grade Encoding Module."""
from src.database import get_connection


def enroll_course(student_id: int, course_code: str, course_title: str, units: int, semester: str) -> bool:
    """Enroll a student in a subject for a given academic semester."""
    if not course_code.strip() or not course_title.strip() or units <= 0:
        return False
    conn = get_connection()
    if not conn.execute("SELECT student_id FROM students WHERE student_id = ?", (student_id,)).fetchone():
        conn.close()
        return False
    conn.execute(
        "INSERT INTO enrollments (student_id, course_code, course_title, units, semester) VALUES (?, ?, ?, ?, ?)",
        (student_id, course_code.strip().upper(), course_title.strip(), units, semester.strip()),
    )
    conn.commit()
    conn.close()
    return True


def record_grade(enrollment_id: int, final_grade: float) -> bool:
    """Encode or update a numerical final grade (1.00 to 5.00 scale)."""
    if not (1.0 <= final_grade <= 5.0):
        return False
    conn = get_connection()
    cur = conn.execute("UPDATE enrollments SET final_grade = ? WHERE enrollment_id = ?", (round(final_grade, 2), enrollment_id))
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def get_student_transcript(student_id: int) -> dict:
    """Retrieve all enrolled courses and compute unit-weighted GWA."""
    conn = get_connection()
    student = conn.execute("SELECT * FROM students WHERE student_id = ?", (student_id,)).fetchone()
    if not student:
        conn.close()
        return {}
    courses = [dict(r) for r in conn.execute("SELECT * FROM enrollments WHERE student_id = ? ORDER BY semester, course_code", (student_id,)).fetchall()]
    conn.close()
    units = sum(c["units"] for c in courses if c["final_grade"] is not None)
    weighted = sum(c["final_grade"] * c["units"] for c in courses if c["final_grade"] is not None)
    return {"student": dict(student), "courses": courses, "gwa": round(weighted / units, 2) if units > 0 else None}
