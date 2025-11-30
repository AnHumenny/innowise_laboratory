import os
import sqlite3

DB_FILE = "grades.db"

def get_db_connection():
    """Creates a connection to the database and enables the foreign key."""

    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database():
    """Checks for the database file and creates it if it is missing."""

    db_exists = os.path.exists(DB_FILE)

    if db_exists:
        print("[INFO] The database already exists. Skipping creation.")
        return False

    print("[INFO] The database was not found. Creating a new one...")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_year INTEGER NOT NULL
        )
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 100),
    
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

    conn.commit()
    conn.close()
    print(f"The database '{DB_FILE}' has been created and is ready for use!")
    return sqlite3.connect(DB_FILE)


def check_db():
    """Creating database if not exists"""

    db_created = initialize_database()

    if db_created:
        print("[INFO] Continue the execution after creating the database.")
    else:
        print("[INFO] Continue to execute, the database has already been created.")

    conn = get_db_connection()
    print("[INFO] The connection to the database has been successfully established.")

    conn.close()
    print("[INFO] The connection to the database has been successfully closed.")

check_db()
