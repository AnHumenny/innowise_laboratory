-- =============================================
-- Student Grades Manager Database
-- SQL Queries File
-- =============================================

-- =============================================
-- CREATING TABLES
-- =============================================

-- Table of students
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
        CHECK (birth_year >= 1900)
);

-- Rating table (grade can be NULL if not yet assigned)
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER CHECK (grade BETWEEN 1 AND 100),
    FOREIGN KEY (student_id) REFERENCES students(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =============================================
-- INDEXES
-- =============================================

-- Speeds up JOIN and student grade search
CREATE INDEX IF NOT EXISTS idx_grades_student_id
    ON grades(student_id);

-- Speeds up subject queries
CREATE INDEX IF NOT EXISTS idx_grades_subject
    ON grades(subject);

-- =============================================
-- INSERTING DATA
-- =============================================

-- Adding students
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

-- Adding ratings (some can be NULL if unknown)
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

-- =============================================
-- QUERIES
-- =============================================

-- All grades for a specific student (Alice Johnson)
SELECT s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.id = 1;

-- Average score for each student (ignores NULL grades)
SELECT s.full_name, AVG(g.grade) AS average_grade
FROM students s
LEFT JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC;

-- Students born after 2004
SELECT id, full_name, birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year;

-- Subjects and their average grades (ignores NULL grades)
SELECT subject, AVG(grade) AS average_grade
FROM grades
WHERE grade IS NOT NULL
GROUP BY subject
ORDER BY average_grade DESC;

-- Top 3 students with the highest average scores (ignores NULL grades)
SELECT s.full_name, AVG(g.grade) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade IS NOT NULL
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- Students who have at least one grade below 80 (ignores NULL grades)
SELECT DISTINCT s.full_name, s.birth_year
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade IS NOT NULL AND g.grade < 80
ORDER BY s.full_name;
