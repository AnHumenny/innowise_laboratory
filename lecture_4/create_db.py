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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_year INTEGER NOT NULL
                CHECK (birth_year >= 1900)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            grade INTEGER CHECK (grade BETWEEN 1 AND 100),
            FOREIGN KEY (student_id) REFERENCES students(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    """)

    cur.execute("""
            INSERT INTO students (full_name, birth_year) VALUES
                ('Alice Johnson', 2005),
                ('Brian Smith', 2004),
                ('Carla Reyes', 2006),
                ('Daniel Kim', 2005),
                ('Eva Thompson', 2003),
                ('Felix Nguyen', 2007),
                ('Grace Patel', 2005),
                ('Henry Lopez', 2004),
                ('Isabella Martinez', 2006);
        """)

    cur.execute("""
            INSERT INTO grades (student_id, subject, grade) VALUES
                (1, 'Math', 88),
                (1, 'English', 92),
                (1, 'Science', 85),
                (2, 'Math', 75),
                (2, 'History', 83),
                (2, 'English', 79),
                (3, 'Science', 95),
                (3, 'Math', 91),
                (3, 'Art', 89),
                (4, 'Math', 84),
                (4, 'Science', 88),
                (4, 'Physical Education', 93),
                (5, 'English', 90),
                (5, 'History', 85),
                (5, 'Math', 88),
                (6, 'Science', 72),
                (6, 'Math', 78),
                (6, 'English', 81),
                (7, 'Art', 94),
                (7, 'Science', 87),
                (7, 'Math', 90),
                (8, 'History', 77),
                (8, 'Math', 83),
                (8, 'Science', 80),
                (9, 'English', 96),
                (9, 'Math', 89),
                (9, 'Art', 92);
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
