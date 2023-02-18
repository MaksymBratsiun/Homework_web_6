SELECT  g.name, s.fullname, gr.grade, d.name 
FROM students s
JOIN grades gr ON gr.student_id = s.id
JOIN [groups] g ON g.id = s.group_id
JOIN disciplines d ON d.id = gr.discipline_id 
WHERE gr.discipline_id = 1 AND g.id = 1;
