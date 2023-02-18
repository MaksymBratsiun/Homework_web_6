SELECT ROUND (AVG(g.grade), 2) as avarage_grade
FROM grades g 
ORDER BY avarage_grade DESC
LIMIT 1;
