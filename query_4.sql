SELECT ROUND (AVG(g.grade), 2) as average_grade
FROM grades g 
ORDER BY average_grade DESC;
