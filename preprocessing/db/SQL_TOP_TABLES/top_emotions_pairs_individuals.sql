CREATE TABLE top_emotions_pairs_individuals (
    word_1 varchar(64),
    macro varchar(128)
);

CREATE OR REPLACE FUNCTION getTop10EmotionsByMacroIndividuals() RETURNS void AS $$
declare
    TEMPROW record;
BEGIN
FOR temprow IN
        SELECT * FROM top_emotions_individuals
    LOOP
        INSERT INTO top_emotions_pairs_individuals
        SELECT emotions_pairs.word_1, emotions.macro
        FROM emotions_pairs, emotions
        WHERE 
        emotions_pairs.emotion_id = emotions.id AND
        emotions.macro = temprow.macro AND
        emotions.ind_id IS NOT null
        GROUP BY emotions_pairs.word_1, emotions.macro
        ORDER BY COUNT(*) DESC LIMIT 10;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM getTop10EmotionsByMacroIndividuals();