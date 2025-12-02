import os
import sqlite3

DB_FILE = "school.db"

def get_db_connection():
    """Creates a connection to the database and enables foreign keys."""

    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_database():
    """Checks for the database file and creates it if missing."""

    if os.path.exists(DB_FILE):
        print("[INFO] The database already exists. Skipping creation.")
        return False

    print("[INFO] Creating new database...")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            birth_year INTEGER NOT NULL
                CHECK (birth_year >= 1900)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            grade INTEGER CHECK (grade BETWEEN 1 AND 100),
            FOREIGN KEY (student_id) REFERENCES students(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject)")

    conn.commit()
    conn.close()

    print(f"[INFO] The database '{DB_FILE}' has been created and is ready for use!")
    return True

def check_db():
    """Creates database if it does not exist, and establishes a connection."""

    db_created = initialize_database()

    if db_created:
        print("[INFO] Continue execution after creating the database.")
    else:
        print("[INFO] Database already exists. Continuing execution.")

    conn = get_db_connection()
    print("[INFO] Connection to the database has been successfully established.")
    conn.close()
    print("[INFO] Connection to the database has been successfully closed.")

check_db()
