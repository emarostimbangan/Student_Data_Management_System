"""Automated Unit Tests for the Student Data Management System."""
import os, unittest
import src.database as db
from src.auth import register_user, login_user
from src.students import add_student, search_students
from src.enrollments import enroll_course, record_grade, get_student_transcript


class TestStudentSystem(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_mgmt.db"
        if os.path.exists(self.test_db): os.remove(self.test_db)
        db.DB_NAME = self.test_db
        db.init_db()

    def tearDown(self):
        if os.path.exists(self.test_db): os.remove(self.test_db)

    def test_lifecycle(self):
        self.assertTrue(register_user("admin1", "pass123", "admin"))
        self.assertIsNotNone(login_user("admin1", "pass123"))
        self.assertTrue(add_student("2026-9999", "Maria Clara", "BSCS", 2, "maria@edu.ph"))
        sid = search_students("Maria")[0]["student_id"]
        self.assertTrue(enroll_course(sid, "CS201", "OOP", 3, "1st Sem"))
        self.assertTrue(record_grade(1, 1.50))
        self.assertEqual(get_student_transcript(sid)["gwa"], 1.50)


if __name__ == "__main__":
    unittest.main()
