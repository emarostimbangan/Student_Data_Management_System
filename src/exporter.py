"""
Student Directory CSV Export and Validation Utility.

Provides institutional student-number format verification and exports the
master student directory into a clean CSV report for registrar archiving.
"""

import csv
import re
from src.students import list_students


def validate_student_number(student_number: str) -> bool:
    """
    Verify that a student number follows the YYYY-NNNN pattern (e.g., 2026-1001).

    Args:
        student_number (str): Candidate student identification string.

    Returns:
        bool: True if format is valid, False otherwise.
    """
    return bool(re.match(r"^\d{4}-\d{4}$", student_number.strip()))


def export_directory_csv(filepath: str = "students_export.csv") -> int:
    """
    Export all student master records into a structured CSV file.

    Args:
        filepath (str): Target output CSV filename.

    Returns:
        int: Total number of student rows exported.
    """
    records = list_students()
    columns = ["student_id", "student_number", "full_name", "program", "year_level", "email", "status"]

    with open(filepath, mode="w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for student in records:
            writer.writerow({col: student[col] for col in columns})

    return len(records)
