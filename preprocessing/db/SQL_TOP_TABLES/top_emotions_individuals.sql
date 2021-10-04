CREATE TABLE top_emotions_individuals AS

SELECT e.macro 
FROM emotions as e
WHERE ind_id IS NOT null and macro <> ''
GROUP BY macro 
ORDER BY COUNT(*) DESC LIMIT 10;