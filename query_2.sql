SELECT d.name, s.fullname, ROUND (AVG(g.grade), 2) as avarage_grade
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN disciplines d ON d.id = g.discipline_id
WHERE d.id = 1
GROUP BY s.fullname 
ORDER BY avarage_grade DESC
LIMIT 1;
