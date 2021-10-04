CREATE TABLE top_contributions_individuals AS

SELECT c.macro 
FROM contributions as c
WHERE ind_id IS NOT null and c.macro <> ''
GROUP BY c.macro 
ORDER BY COUNT(*) DESC LIMIT 10;