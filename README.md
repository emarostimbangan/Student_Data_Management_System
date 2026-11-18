# Student Data Management System

A modular, heavily documented command-line **Student Data Management System** built with **Python** and **SQLite**.

## Author
- **emarostimbangan** (`emarostimbangan326@gmail.com`)

## Project Architecture
- `main.py` — Interactive terminal CLI menu and role-based session controller
- `seed.py` — Sample database seeder with realistic student and enrollment records
- `src/database.py` — SQLite connection helper and 3-table relational schema (`users`, `students`, `enrollments`)
- `src/auth.py` — SHA-256 credential hashing and role-based login (`admin`, `faculty`)
- `src/students.py` — Student master directory CRUD and keyword search
- `src/enrollments.py` — Subject enrollment, grade encoding (`1.00–5.00`), and unit-weighted GWA calculator
- `src/honors.py` — Dean's List qualification (`GWA <= 1.75`) and academic standing classifier
- `src/analytics.py` — Institutional student headcount, average grade, and program distribution analytics
- `src/exporter.py` — `YYYY-NNNN` student-number format validator and CSV directory exporter
- `tests/test_system.py` — Automated end-to-end `unittest` test suite

## How to Run
1. Populate sample records: `python3 seed.py`
2. Run automated tests: `python3 -m unittest discover -s tests -v`
3. Launch the CLI application: `python3 main.py`

## Collaborator Contributions
- **shiellamari22-cell** (`shiellamari22@gmail.com`) — Course-level grade distribution, pass/fail analytics (`src/course_stats.py`), CLI reporting option 12, and dedicated course statistics unit tests (`tests/test_course_stats.py`).
