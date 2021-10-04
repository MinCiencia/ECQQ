CREATE TABLE top_country_needs_role_pairs_dialogues (
    word_1 varchar(64),
    macro varchar(128)
);

CREATE OR REPLACE FUNCTION getTop10CountryNeedRoleByMacroDialogues() RETURNS void AS $$
declare
    TEMPROW record;
BEGIN
FOR temprow IN
        SELECT * FROM top_country_needs_dialogues
    LOOP
        INSERT INTO top_country_needs_role_pairs_dialogues
        SELECT country_needs_role_pairs.word_1, country_needs.macro
        FROM country_needs_role_pairs, country_needs
        WHERE 
        country_needs_role_pairs.country_need_id = country_needs.id AND
        country_needs.macro = temprow.macro AND
        country_needs.diag_id IS NOT null
        GROUP BY country_needs_role_pairs.word_1, country_needs.macro
        ORDER BY COUNT(*) DESC LIMIT 10;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM getTop10CountryNeedRoleByMacroDialogues();