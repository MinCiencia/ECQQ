CREATE TABLE top_personal_needs_individuals AS

SELECT pn.macro 
FROM personal_needs as pn
WHERE ind_id IS NOT null and macro <> ''
GROUP BY pn.macro 
ORDER BY COUNT(*) DESC LIMIT 10;