SELECT t.fullname , d.name 
FROM disciplines d 
JOIN teachers t ON t.id = d.teacher_id 
WHERE t.id = 1
GROUP BY d.name 