CREATE TABLE top_10_emo_table AS

SELECT e.name 
FROM emotion as e, person_emotion as pe 
WHERE pe.emo_id=e.emo_id 
GROUP BY name 
ORDER BY COUNT(*) DESC LIMIT 10;


