CREATE TABLE top_emotions_pairs_dialogues (
    word_1 varchar(64),
    macro varchar(1024)
);

CREATE OR REPLACE FUNCTION getTop10EmotionsByMacroDialogues() RETURNS void AS $$
declare
    TEMPROW record;
BEGIN
FOR temprow IN
        SELECT * FROM top_emotions_dialogues
    LOOP
        INSERT INTO top_emotions_pairs_dialogues
        SELECT emotions_pairs.word_1, emotions.macro
        FROM emotions_pairs, emotions
        WHERE 
        emotions_pairs.emotion_id = emotions.id AND
        emotions.macro = temprow.macro AND
        emotions.diag_id IS NOT null
        GROUP BY emotions_pairs.word_1, emotions.macro
        ORDER BY COUNT(*) DESC LIMIT 10;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM getTop10EmotionsByMacroDialogues();