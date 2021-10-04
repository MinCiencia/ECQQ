CREATE TABLE top_50_need_macro_table AS

SELECT n.macro 
FROM need as n, person_need as pn
WHERE pn.need_id=n.need_id 
GROUP BY n.macro 
ORDER BY COUNT(*) DESC LIMIT 50;
