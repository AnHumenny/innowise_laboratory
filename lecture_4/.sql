-- =============================================
-- Student Grades Manager Database
-- SQL Queries File
-- =============================================

-- CREATING TABLES
-- =============================================

-- Table of students
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

-- Rating table
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 100),

    FOREIGN KEY (student_id) REFERENCES students(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

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

-- Adding ratings
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


-- All grades for a specific student (Alice Johnson)
SELECT s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.full_name = 'Alice Johnson';

-- Average score for each student
SELECT s.full_name, AVG(g.grade) as average_grade
FROM students s
LEFT JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC;

-- Students born after 2004
SELECT id, full_name, birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year;

-- Subjects and their average grades
SELECT subject, AVG(grade) as average_grade
FROM grades
GROUP BY subject
ORDER BY average_grade DESC;

-- Top 3 students with the highest average scores
SELECT s.full_name, AVG(g.grade) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- Students who have at least one grade below 80
SELECT DISTINCT s.full_name, s.birth_year
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80
ORDER BY s.full_name;

-- Getting a Student ID
SELECT id FROM students
WHERE full_name = 'Alice Johnson'
AND birth_year = 2005;

-- Adding to database a new student
INSERT INTO students (full_name, birth_year)
VALUES ('John Doe', 2000);

-- Insert new grade
INSERT INTO grades (student_id, subject, grade)
SELECT id, 'Math', 100
FROM students
WHERE full_name = 'Alice Johnson';

-- Delete student
DELETE FROM students
WHERE full_name = 'Alice Johnson';

-- All grades of a particular student (by ID)
SELECT subject, grade
FROM grades
WHERE student_id = 1;

-- All students
SELECT id, full_name, birth_year
FROM students;

-- Student's grades (numeric values only)
SELECT grade
FROM grades
WHERE student_id = 1;

-- CREATING INDEXES FOR OPTIMIZATION
-- =============================================

-- An index to search for students by name and year of birth
CREATE INDEX idx_students_name_birthyear
ON students(full_name, birth_year);

-- Index for searching grades by student_id
CREATE INDEX idx_grades_student_id
ON grades(student_id);

-- An index for searching by subject
CREATE INDEX idx_grades_subject
ON grades(subject);

-- Index for filtering by year of birth
CREATE INDEX idx_students_birthyear
ON students(birth_year);

-- Index for filtering by estimates
CREATE INDEX idx_grades_grade
ON grades(grade);

-- VERIFICATION REQUESTS
-- =============================================

-- Checking the number of records
SELECT 'Students count: ' || COUNT(*) FROM students;
SELECT 'Grades count: ' || COUNT(*) FROM grades;

-- Viewing all data
SELECT * FROM students;
SELECT * FROM grades;