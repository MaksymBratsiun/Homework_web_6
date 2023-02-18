SELECT g.name, s.fullname 
FROM students s  
JOIN [groups] g ON g.id = s.group_id  
WHERE g.id  = 1
GROUP BY s.fullname 