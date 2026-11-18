"""
Course Enrollment and Grade Encoding Module.

Manages subject enrollments linked to student records, numerical grade
recording (1.00–5.00 scale), and automated unit-weighted General Weighted
Average (GWA) calculation for student transcripts.
"""

from src.database import get_connection


def enroll_course(
    student_id: int,
    course_code: str,
    course_title: str,
    units: int,
    semester: str,
) -> bool:
    """
    Enroll an existing student into a subject for a specified semester.

    Args:
        student_id (int): Foreign key referencing students(student_id).
        course_code (str): Subject code (e.g., CS301).
        course_title (str): Descriptive subject title.
        units (int): Credit unit weight (must be > 0).
        semester (str): Academic term label (e.g., 1st Sem 2026).

    Returns:
        bool: True if enrollment succeeded, False if student does not exist or input is invalid.
    """
    if not course_code.strip() or not course_title.strip() or units <= 0:
        return False

    conn = get_connection()
    # Verify parent student record exists before inserting enrollment
    if not conn.execute("SELECT student_id FROM students WHERE student_id = ?", (student_id,)).fetchone():
        conn.close()
        return False

    conn.execute(
        """
        INSERT INTO enrollments (student_id, course_code, course_title, units, semester)
        VALUES (?, ?, ?, ?, ?)
        """,
        (student_id, course_code.strip().upper(), course_title.strip(), units, semester.strip()),
    )
    conn.commit()
    conn.close()
    return True


def record_grade(enrollment_id: int, final_grade: float) -> bool:
    """
    Encode or update a numerical final grade on a 1.00 to 5.00 scale.

    Args:
        enrollment_id (int): Primary key of the enrollment record.
        final_grade (float): Grade value between 1.00 (highest) and 5.00.

    Returns:
        bool: True if enrollment record was updated, False otherwise.
    """
    if not (1.0 <= final_grade <= 5.0):
        return False

    conn = get_connection()
    cur = conn.execute(
        "UPDATE enrollments SET final_grade = ? WHERE enrollment_id = ?",
        (round(final_grade, 2), enrollment_id),
    )
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def get_student_transcript(student_id: int) -> dict:
    """
    Compile a student's enrolled subjects and compute their unit-weighted GWA.

    Args:
        student_id (int): Primary key ID of the student.

    Returns:
        dict: Dictionary with 'student', 'courses', and 'gwa' keys, or empty dict if not found.
    """
    conn = get_connection()
    student = conn.execute("SELECT * FROM students WHERE student_id = ?", (student_id,)).fetchone()
    if not student:
        conn.close()
        return {}

    courses = [
        dict(r)
        for r in conn.execute(
            "SELECT * FROM enrollments WHERE student_id = ? ORDER BY semester, course_code",
            (student_id,),
        ).fetchall()
    ]
    conn.close()

    # Calculate General Weighted Average: sum(grade * units) / sum(units) for graded courses
    total_units = sum(c["units"] for c in courses if c["final_grade"] is not None)
    weighted_sum = sum(c["final_grade"] * c["units"] for c in courses if c["final_grade"] is not None)
    gwa = round(weighted_sum / total_units, 2) if total_units > 0 else None

    return {"student": dict(student), "courses": courses, "gwa": gwa}
