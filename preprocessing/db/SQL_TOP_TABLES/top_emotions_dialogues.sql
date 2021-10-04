CREATE TABLE top_emotions_dialogues AS

SELECT e.macro 
FROM emotions as e
WHERE diag_id IS NOT null and macro <> ''
GROUP BY macro 
ORDER BY COUNT(*) DESC LIMIT 10;