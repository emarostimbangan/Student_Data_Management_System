"""
Unit Tests for Course-Level Grade Distribution and Pass/Fail Analytics.

Verifies per-course enrollment counts, average numerical grade computation,
passed/failed tallies, and top-performing subject ranking.
"""

import os
import unittest
import src.database as db
from src.students import add_student, search_students
from src.enrollments import enroll_course, record_grade
from src.course_stats import get_course_performance, get_top_performing_courses


class TestCourseStats(unittest.TestCase):
    """Test suite for src/course_stats.py."""

    def setUp(self) -> None:
        self.test_db = "test_course_stats.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        db.DB_NAME = self.test_db
        db.init_db()

    def tearDown(self) -> None:
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_course_performance_and_ranking(self) -> None:
        add_student("2026-2001", "Student One", "BSCS", 2, "one@norsu.edu.ph")
        add_student("2026-2002", "Student Two", "BSCS", 2, "two@norsu.edu.ph")
        s1 = search_students("One")[0]["student_id"]
        s2 = search_students("Two")[0]["student_id"]

        enroll_course(s1, "CS101", "Intro to Computing", 3, "1st Sem")
        enroll_course(s2, "CS101", "Intro to Computing", 3, "1st Sem")
        record_grade(1, 1.50)
        record_grade(2, 3.50)

        stats = get_course_performance()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]["total_enrolled"], 2)
        self.assertEqual(stats[0]["avg_grade"], 2.50)
        self.assertEqual(stats[0]["passed_count"], 1)
        self.assertEqual(stats[0]["failed_count"], 1)

        top = get_top_performing_courses(limit=1)
        self.assertEqual(top[0]["course_code"], "CS101")


if __name__ == "__main__":
    unittest.main()
