# Student Data Management System

A modular command-line **Student Data Management System** built with **Python** and **SQLite**.

## Author
- **emarostimbangan** — Relational SQLite schema, SHA-256 authentication, student directory CRUD, course enrollment & GWA transcript engine, institutional academic analytics, sample seeder, and automated unit tests

## Project Structure
- `main.py` — Interactive CLI menu and user session controller
- `seed.py` — Sample database seeder for immediate testing
- `src/__init__.py` — Package initializer
- `src/database.py` — SQLite connection and 3-table schema (`users`, `students`, `enrollments`)
- `src/auth.py` — SHA-256 registration and role-based login (`admin`, `faculty`)
- `src/students.py` — Student master directory CRUD and search
- `src/enrollments.py` — Course enrollment, grade encoding, and GWA transcript calculator
- `src/analytics.py` — Institutional academic summary and program distribution reports
- `tests/test_system.py` — Automated end-to-end unit test suite

## How to Run
1. Populate sample records: `python3 seed.py`
2. Run automated tests: `python3 -m unittest discover -s tests -v`
3. Launch the CLI application: `python3 main.py`
