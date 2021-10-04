CREATE TABLE top_50_con_table AS

SELECT c.macro 
FROM contribution as c, person_contribution as pc 
WHERE pc.con_id=c.con_id 
GROUP BY c.macro 
ORDER BY COUNT(*) DESC LIMIT 50;
