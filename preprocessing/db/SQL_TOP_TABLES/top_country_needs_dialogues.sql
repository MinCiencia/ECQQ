CREATE TABLE top_country_needs_dialogues AS

SELECT cn.macro 
FROM country_needs as cn
WHERE diag_id IS NOT null and cn.macro <> ''
GROUP BY cn.macro 
ORDER BY COUNT(*) DESC LIMIT 10;