SELECT t.fullname, ROUND(AVG(g.grade), 2)
FROM grades g
JOIN disciplines d ON d.id = g.discipline_id
JOIN teachers t ON t.id = d.teacher_id
WHERE t.id = 1
GROUP BY t.fullname 

