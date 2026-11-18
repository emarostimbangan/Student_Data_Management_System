"""
Input Validation and Data Sanitization Helpers.

Centralizes validation rules for institutional email addresses, Philippine
university numerical grades (1.00 to 5.00), and year levels (1 to 5) before
database insertion or updates.
"""

import re


def is_valid_email(email: str) -> bool:
    """
    Check whether an email address matches standard user@domain.tld format.

    Args:
        email (str): Candidate email string.

    Returns:
        bool: True if structurally valid, False otherwise.
    """
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email.strip()))


def is_valid_grade(grade: float) -> bool:
    """
    Verify that a numerical grade falls within the 1.00 to 5.00 academic scale.

    Args:
        grade (float): Candidate grade value.

    Returns:
        bool: True if within [1.00, 5.00], False otherwise.
    """
    return 1.0 <= grade <= 5.0


def is_valid_year_level(year_level: int) -> bool:
    """
    Ensure academic year level is an integer between 1 and 5 inclusive.

    Args:
        year_level (int): Student year level.

    Returns:
        bool: True if valid, False otherwise.
    """
    return isinstance(year_level, int) and (1 <= year_level <= 5)
