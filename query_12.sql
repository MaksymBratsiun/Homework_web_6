SELECT s.fullname, g.grade, d.name, g.date_of, g2.name 
FROM grades g 
JOIN students s ON s.id = g.student_id
JOIN disciplines d ON d.id = g.discipline_id 
JOIN [groups] g2 ON g2.id = s.group_id 
WHERE d.id = 1 AND s.group_id = 1 AND g.date_of = (
	SELECT MAX(grades.date_of)
	FROM grades
	WHERE grades.discipline_id = 1);
