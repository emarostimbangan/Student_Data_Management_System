"""
Academic Standing and Dean's List Qualification Module.

Evaluates student General Weighted Averages (GWA) on a 1.00–5.00 Philippine
university grading scale (where 1.00 is highest) to determine academic honors
and probationary standing.
"""

from src.students import list_students
from src.enrollments import get_student_transcript

# Maximum GWA threshold required to qualify for the Dean's List
DEANS_LIST_CUTOFF = 1.75
# Maximum GWA threshold for good academic standing before probation
GOOD_STANDING_CUTOFF = 3.00


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
    if gwa <= DEANS_LIST_CUTOFF:
        return "Dean's Lister"
    if gwa <= GOOD_STANDING_CUTOFF:
        return "Good Standing"
    return "Academic Probation"


def get_deans_list() -> list[dict]:
    """
    Scan all active students and return those qualifying for the Dean's List.

    Returns:
        list[dict]: Qualified student records sorted from best (lowest) GWA to highest.
    """
    honors = []
    for student in list_students():
        # Exclude inactive or already-graduated students from active semester honors
        if student["status"] != "active":
            continue

        transcript = get_student_transcript(student["student_id"])
        gwa = transcript.get("gwa")

        # Include students whose graded coursework meets the Dean's List cutoff
        if gwa is not None and gwa <= DEANS_LIST_CUTOFF:
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

    # Rank honorees from lowest numerical GWA (1.00) upward
    honors.sort(key=lambda item: item["gwa"])
    return honors
