
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    marks INTEGER
);

INSERT OR IGNORE INTO students VALUES
(1, 'Nidhi', 85),
(2, 'Rahul', 65),
(3, 'Priya', 92),
(4, 'Aman', 72),
(5, 'Neha', 55);

SELECT * FROM students;
SELECT COUNT(*) AS total_students FROM students;
SELECT AVG(marks) AS average_marks FROM students;
SELECT MAX(marks) AS max_marks FROM students;
SELECT MIN(marks) AS min_marks FROM students;

SELECT SUM(marks) AS total_marks
FROM students;

SELECT
    CASE
        WHEN marks >= 70 THEN 'Good'
        ELSE 'Needs Improvement'
    END AS category,
    COUNT(*) AS total_students
FROM students
GROUP BY category;

SELECT
    students.name,
    students.marks,
    departments.department
FROM students
INNER JOIN departments
ON students.id = departments.student_id;

SELECT * FROM departments;

PRAGMA table_info(departments);

SELECT * FROM departments;

SELECT
    students.name,
    students.marks,
    departments.department
FROM students
INNER JOIN departments
ON students.id = departments.student_id;
