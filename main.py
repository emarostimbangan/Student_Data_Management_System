"""Command-Line Interface (CLI) Entry Point for the Student Data Management System."""
from src.database import init_db
from src.auth import register_user, login_user
from src.students import add_student, list_students, search_students, update_student_status, delete_student
from src.enrollments import enroll_course, record_grade, get_student_transcript
from src.analytics import get_academic_summary, get_program_distribution


def run_cli() -> None:
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
                print("1. View All Students\n2. Search Students\n3. Add Student\n4. Enroll Subject\n5. Encode Grade\n6. View Transcript & GWA")
                if user["role"] == "admin":
                    print("7. Update Student Status\n8. Delete Student\n9. Academic Analytics")
                print("0. Logout")
                opt = input("Option: ").strip()
                if opt == "1":
                    for s in list_students():
                        print(f"[ID:{s['student_id']}] {s['student_number']} - {s['full_name']} | {s['program']} Yr {s['year_level']} ({s['status']})")
                elif opt == "2":
                    for s in search_students(input("Keyword: ")):
                        print(f"[ID:{s['student_id']}] {s['student_number']} - {s['full_name']} | {s['program']}")
                elif opt == "3":
                    ok = add_student(input("Student No: "), input("Full Name: "), input("Program: "), int(input("Year (1-5): ")), input("Email: "))
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
                        print(f"Transcript: {t['student']['full_name']} | GWA: {t['gwa']}")
                        for c in t["courses"]:
                            print(f"  [#{c['enrollment_id']}] {c['course_code']} - {c['course_title']} ({c['units']}u) | Grade: {c['final_grade']}")
                elif opt == "7" and user["role"] == "admin":
                    print("Updated!" if update_student_status(int(input("Student ID: ")), int(input("Year: ")), input("Status: ")) else "Failed.")
                elif opt == "8" and user["role"] == "admin":
                    print("Deleted!" if delete_student(int(input("Student ID: "))) else "Failed.")
                elif opt == "9" and user["role"] == "admin":
                    s = get_academic_summary()
                    print(f"Total: {s['total_students']} | Active: {s['active_students']} | Enrollments: {s['total_enrollments']} | Avg Grade: {s['average_grade']}")
                    for p in get_program_distribution():
                        print(f"  - {p['program']}: {p['student_count']}")
                elif opt == "0":
                    break
        elif choice == "3":
            break


if __name__ == "__main__":
    run_cli()
