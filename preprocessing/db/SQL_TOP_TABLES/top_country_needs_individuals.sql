CREATE TABLE top_country_needs_individuals AS

SELECT cn.macro 
FROM country_needs as cn
WHERE ind_id IS NOT null and cn.macro <> ''
GROUP BY cn.macro 
ORDER BY COUNT(*) DESC LIMIT 10;