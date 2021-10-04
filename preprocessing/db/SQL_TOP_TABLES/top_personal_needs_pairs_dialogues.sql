CREATE TABLE top_personal_needs_pairs_dialogues (
    word_1 varchar(64),
    macro varchar(1024)
);

CREATE OR REPLACE FUNCTION getTop10PersonalNeedByMacroDialogues() RETURNS void AS $$
declare
    TEMPROW record;
BEGIN
FOR temprow IN
        SELECT * FROM top_personal_needs_dialogues
    LOOP
        INSERT INTO top_personal_needs_pairs_dialogues
        SELECT personal_needs_pairs.word_1, personal_needs.macro
        FROM personal_needs_pairs, personal_needs
        WHERE 
        personal_needs_pairs.personal_need_id = personal_needs.id AND
        personal_needs.macro = temprow.macro AND
        personal_needs.diag_id IS NOT null
        GROUP BY personal_needs_pairs.word_1, personal_needs.macro
        ORDER BY COUNT(*) DESC LIMIT 10;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM getTop10PersonalNeedByMacroDialogues();