# Student Data Management System

A modular command-line **Student Data Management System** built with **Python** and **SQLite**.

## Author
- **emarostimbangan** (`emarostimbangan326@gmail.com`)

## Key Features
- **Role-Based Authentication (`src/auth.py`)**: SHA-256 password hashing supporting `admin` (Registrar) and `faculty` roles.
- **Relational SQLite Schema (`src/database.py`)**: Three normalized tables (`users`, `students`, `enrollments`) with `ON DELETE CASCADE` foreign-key constraints.
- **Student Directory CRUD (`src/students.py`)**: Register students, list profiles, search by ID/name/program, update year/status, and remove records.
- **Course Enrollment & GWA Engine (`src/enrollments.py`)**: Enroll students in subjects, encode numerical grades (`1.00–5.00`), and compute unit-weighted General Weighted Averages.
- **Academic Analytics (`src/analytics.py`)**: Generates institutional student counts, active/graduated breakdowns, average grades, and degree program distributions.
- **CSV Export & Validation (`src/exporter.py`)**: Validates `YYYY-NNNN` student numbers and exports the student directory to CSV.
- **Sample Seeder & Automated Tests (`seed.py`, `tests/test_system.py`)**: Populates realistic demo records and verifies every module via `unittest`.

## How to Run
1. Populate sample records: `python3 seed.py`
2. Run automated tests: `python3 -m unittest discover -s tests -v`
3. Launch the CLI application: `python3 main.py`
