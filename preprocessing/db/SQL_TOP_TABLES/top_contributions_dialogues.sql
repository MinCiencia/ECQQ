CREATE TABLE top_contributions_dialogues AS

SELECT c.macro 
FROM contributions as c
WHERE diag_id IS NOT null and c.macro <> ''
GROUP BY c.macro 
ORDER BY COUNT(*) DESC LIMIT 10;
