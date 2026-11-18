"""
Comprehensive Unit Test Suite for the Student Data Management System.

Verifies authentication, input validators, student CRUD, course enrollment,
grade encoding, GWA transcript calculation, Dean's List classification,
institutional analytics, and CSV export.
"""

import os
import unittest
import src.database as db
from src.auth import register_user, login_user
from src.students import add_student, search_students, update_student_status, delete_student
from src.enrollments import enroll_course, record_grade, get_student_transcript
from src.analytics import get_academic_summary, get_program_distribution
from src.exporter import validate_student_number, export_directory_csv
from src.honors import classify_standing, get_deans_list
from src.validators import is_valid_email, is_valid_grade, is_valid_year_level


class TestStudentSystem(unittest.TestCase):
    """End-to-end verification of all system modules."""

    def setUp(self) -> None:
        self.test_db = "test_mgmt.db"
        self.test_csv = "test_export.csv"
        for f in (self.test_db, self.test_csv):
            if os.path.exists(f):
                os.remove(f)
        db.DB_NAME = self.test_db
        db.init_db()

    def tearDown(self) -> None:
        for f in (self.test_db, self.test_csv):
            if os.path.exists(f):
                os.remove(f)

    def test_validators(self) -> None:
        self.assertTrue(is_valid_email("student@norsu.edu.ph"))
        self.assertFalse(is_valid_email("invalid-email"))
        self.assertTrue(is_valid_grade(1.25))
        self.assertFalse(is_valid_grade(6.00))
        self.assertTrue(is_valid_year_level(3))
        self.assertFalse(is_valid_year_level(0))

    def test_full_academic_workflow(self) -> None:
        self.assertTrue(register_user("admin1", "pass123", "admin"))
        self.assertIsNotNone(login_user("admin1", "pass123"))

        self.assertTrue(validate_student_number("2026-9999"))
        self.assertFalse(validate_student_number("ABC-12"))
        self.assertTrue(add_student("2026-9999", "Maria Clara", "BSCS", 2, "maria@edu.ph"))
        sid = search_students("Maria")[0]["student_id"]

        self.assertTrue(enroll_course(sid, "CS201", "OOP", 3, "1st Sem"))
        self.assertTrue(enroll_course(sid, "CS202", "DBMS", 3, "1st Sem"))
        self.assertTrue(record_grade(1, 1.50))
        self.assertTrue(record_grade(2, 1.75))

        transcript = get_student_transcript(sid)
        self.assertEqual(transcript["gwa"], 1.62)
        self.assertEqual(classify_standing(transcript["gwa"]), "Dean's Lister")
        self.assertEqual(len(get_deans_list()), 1)

        self.assertEqual(export_directory_csv(self.test_csv), 1)
        self.assertTrue(update_student_status(sid, 3, "graduated"))
        self.assertEqual(get_academic_summary()["graduated_students"], 1)
        self.assertEqual(len(get_program_distribution()), 1)

        self.assertTrue(delete_student(sid))
        self.assertEqual(get_academic_summary()["total_students"], 0)


if __name__ == "__main__":
    unittest.main()
