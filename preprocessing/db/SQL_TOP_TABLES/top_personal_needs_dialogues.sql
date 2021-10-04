CREATE TABLE top_personal_needs_dialogues AS

SELECT pn.macro 
FROM personal_needs as pn
WHERE diag_id IS NOT null and macro <> ''
GROUP BY pn.macro 
ORDER BY COUNT(*) DESC LIMIT 10;