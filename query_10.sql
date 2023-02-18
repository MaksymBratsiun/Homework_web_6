SELECT d.name as discipline, s.fullname as student, t.fullname as teacher
FROM grades g 
JOIN students s ON s.id = g.student_id 
JOIN disciplines d ON d.id = g.discipline_id
JOIN teachers t  ON t.id = d.teacher_id 
WHERE s.id = 1 AND t.id = 1
GROUP BY d.name;

