"""
Command-Line Interface (CLI) Entry Point for the Student Data Management System.

Provides an interactive menu-driven terminal interface for student directory
management, course enrollment, grade encoding, transcript GWA viewing,
Dean's List qualification reports, course grade summaries, CSV exports,
and institutional analytics.
"""

from src.database import init_db
from src.auth import register_user, login_user
from src.students import add_student, list_students, search_students, update_student_status, delete_student
from src.enrollments import enroll_course, record_grade, get_student_transcript
from src.analytics import get_academic_summary, get_program_distribution
from src.honors import classify_standing, get_deans_list
from src.exporter import validate_student_number, export_directory_csv
from src.course_stats import get_course_performance


def run_cli() -> None:
    """Initialize the database and run the main interactive CLI loop."""
    init_db()
    while True:
        print("\n=========================================")
        print("     STUDENT DATA MANAGEMENT SYSTEM")
        print("=========================================")
        print("1. Register Account\n2. Login\n3. Exit")
        choice = input("Select option (1-3): ").strip()

        if choice == "1":
            ok = register_user(input("Username: "), input("Password: "), input("Role (admin/faculty): ") or "faculty")
            print("Registered!" if ok else "Registration failed.")

        elif choice == "2":
            user = login_user(input("Username: "), input("Password: "))
            if not user:
                print("Invalid credentials.")
                continue

            while True:
                print(f"\n--- {user['username']} ({user['role'].upper()}) ---")
                print("1. View All Students\n2. Search Students\n3. Add Student\n4. Enroll Subject\n5. Encode Grade\n6. View Transcript & Standing\n7. View Dean's List")
                if user["role"] == "admin":
                    print("8. Update Student Status (Admin)\n9. Delete Student (Admin)\n10. Academic Analytics (Admin)\n11. Export Directory to CSV (Admin)\n12. Course Grade Summary (Admin)")
                print("0. Logout")
                opt = input("Option: ").strip()

                if opt == "1":
                    for s in list_students():
                        print(f"[ID:{s['student_id']}] {s['student_number']} - {s['full_name']} | {s['program']} Yr {s['year_level']} ({s['status']})")
                elif opt == "2":
                    for s in search_students(input("Keyword: ")):
                        print(f"[ID:{s['student_id']}] {s['student_number']} - {s['full_name']} | {s['program']}")
                elif opt == "3":
                    s_num = input("Student No (YYYY-NNNN): ").strip()
                    if not validate_student_number(s_num):
                        print("Invalid format! Expected YYYY-NNNN (e.g., 2026-1004).")
                        continue
                    ok = add_student(s_num, input("Full Name: "), input("Program: "), int(input("Year (1-5): ")), input("Email: "))
                    print("Student added!" if ok else "Failed.")
                elif opt == "4":
                    ok = enroll_course(int(input("Student ID: ")), input("Course Code: "), input("Title: "), int(input("Units: ")), input("Semester: "))
                    print("Enrolled!" if ok else "Failed.")
                elif opt == "5":
                    ok = record_grade(int(input("Enrollment ID: ")), float(input("Grade (1.00-5.00): ")))
                    print("Grade saved!" if ok else "Failed.")
                elif opt == "6":
                    t = get_student_transcript(int(input("Student ID: ")))
                    if t:
                        standing = classify_standing(t["gwa"])
                        print(f"Transcript: {t['student']['full_name']} | GWA: {t['gwa']} ({standing})")
                        for c in t["courses"]:
                            print(f"  [#{c['enrollment_id']}] {c['course_code']} - {c['course_title']} ({c['units']}u) | Grade: {c['final_grade']}")
                elif opt == "7":
                    honors = get_deans_list()
                    print("\n--- DEAN'S LIST QUALIFIERS (GWA <= 1.75) ---")
                    for h in honors:
                        print(f"  {h['student_number']} - {h['full_name']} ({h['program']}) | GWA: {h['gwa']}")
                elif opt == "8" and user["role"] == "admin":
                    print("Updated!" if update_student_status(int(input("Student ID: ")), int(input("Year: ")), input("Status: ")) else "Failed.")
                elif opt == "9" and user["role"] == "admin":
                    print("Deleted!" if delete_student(int(input("Student ID: "))) else "Failed.")
                elif opt == "10" and user["role"] == "admin":
                    s = get_academic_summary()
                    print(f"Total: {s['total_students']} | Active: {s['active_students']} | Enrollments: {s['total_enrollments']} | Avg Grade: {s['average_grade']}")
                    for p in get_program_distribution():
                        print(f"  - {p['program']}: {p['student_count']}")
                elif opt == "11" and user["role"] == "admin":
                    count = export_directory_csv()
                    print(f"Exported {count} student record(s) to students_export.csv!")
                elif opt == "12" and user["role"] == "admin":
                    print("\n--- COURSE PERFORMANCE SUMMARY ---")
                    for c in get_course_performance():
                        print(f"  {c['course_code']} ({c['course_title']}) | Enrolled: {c['total_enrolled']} | Avg: {c['avg_grade']} | Passed: {c['passed_count']} | Failed: {c['failed_count']}")
                elif opt == "0":
                    break
        elif choice == "3":
            break


if __name__ == "__main__":
    run_cli()
