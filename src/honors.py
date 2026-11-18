"""
Academic Standing and Dean's List Qualification Module.

Evaluates student General Weighted Averages (GWA) on a 1.00–5.00 Philippine
university grading scale (where 1.00 is highest) to determine academic honors
and probationary standing.
"""

from src.students import list_students
from src.enrollments import get_student_transcript


def classify_standing(gwa: float | None) -> str:
    """
    Classify academic standing based on unit-weighted GWA.

    Args:
        gwa (float | None): Computed General Weighted Average (1.00 = highest).

    Returns:
        str: Standing label ('Dean's Lister', 'Good Standing', 'Academic Probation', or 'No Grades Yet').
    """
    if gwa is None:
        return "No Grades Yet"
    if gwa <= 1.75:
        return "Dean's Lister"
    if gwa <= 3.00:
        return "Good Standing"
    return "Academic Probation"


def get_deans_list() -> list[dict]:
    """
    Scan all active students and return those qualifying for the Dean's List (GWA <= 1.75).

    Returns:
        list[dict]: Qualified student records with their computed GWA and standing.
    """
    honors = []
    for student in list_students():
        # Only active students with graded coursework are eligible
        if student["status"] != "active":
            continue
        transcript = get_student_transcript(student["student_id"])
        gwa = transcript.get("gwa")
        if gwa is not None and gwa <= 1.75:
            honors.append(
                {
                    "student_id": student["student_id"],
                    "student_number": student["student_number"],
                    "full_name": student["full_name"],
                    "program": student["program"],
                    "gwa": gwa,
                    "standing": classify_standing(gwa),
                }
            )
    # Sort honorees from lowest (best) GWA to highest
    honors.sort(key=lambda item: item["gwa"])
    return honors
