"""Sample Data Seeder for the Student Data Management System."""
from src.database import init_db, get_connection
from src.auth import register_user
from src.students import add_student, list_students
from src.enrollments import enroll_course, record_grade


def seed_database() -> None:
    init_db()
    conn = get_connection()
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        print("Already seeded.")
        return
    conn.close()
    register_user("registrar_admin", "admin123", "admin")
    register_user("prof_santos", "faculty123", "faculty")
    add_student("2026-1001", "Emaro Stimbangan", "BS Computer Science", 3, "emaro@norsu.edu.ph")
    add_student("2026-1002", "Sequil Hisona", "BS Computer Science", 3, "sequil@norsu.edu.ph")
    add_student("2026-1003", "Alexander Amparado Jr.", "BS Information Technology", 2, "alex@norsu.edu.ph")
    sid = list_students()[0]["student_id"]
    enroll_course(sid, "CS301", "Data Structures and Algorithms", 3, "1st Sem 2026")
    enroll_course(sid, "CS302", "Database Management Systems", 3, "1st Sem 2026")
    record_grade(1, 1.25)
    record_grade(2, 1.50)
    print("Seeding complete! Login -> registrar_admin / admin123")


if __name__ == "__main__":
    seed_database()
