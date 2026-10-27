
SELECT
    students.name,
    students.marks,
    departments.department
FROM students
INNER JOIN departments
ON students.id = departments.student_id;

SELECT
    departments.department,
    AVG(students.marks) AS average_marks,
    COUNT(students.id) AS total_students
FROM students
INNER JOIN departments
ON students.id = departments.student_id
GROUP BY departments.department
ORDER BY average_marks DESC;

SELECT name, marks
FROM students
WHERE marks > (
    SELECT AVG(marks)
    FROM students
);

SELECT name, marks
FROM students
ORDER BY marks DESC
LIMIT 3;

SELECT name, marks
FROM students
WHERE marks >= 70
ORDER BY marks DESC;

SELECT
    COUNT(*) AS total_students,
    AVG(marks) AS average_marks,
    MAX(marks) AS highest_marks,
    MIN(marks) AS lowest_marks
FROM students;

