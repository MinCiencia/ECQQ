CREATE TABLE top_country_needs_exp_pairs_individuals (
    word_1 varchar(64),
    macro varchar(128)
);


CREATE OR REPLACE FUNCTION getTop10CountryNeedExpByMacroIndividuals() RETURNS void AS $$
declare
    TEMPROW record;
BEGIN
FOR temprow IN
        SELECT * FROM top_country_needs_individuals
    LOOP
        INSERT INTO top_country_needs_exp_pairs_individuals
        SELECT country_needs_exp_pairs.word_1, country_needs.macro
        FROM country_needs_exp_pairs, country_needs
        WHERE 
        country_needs_exp_pairs.country_need_id = country_needs.id AND
        country_needs.macro = temprow.macro AND
        country_needs.ind_id IS NOT null
        GROUP BY country_needs_exp_pairs.word_1, country_needs.macro
        ORDER BY COUNT(*) DESC LIMIT 10;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM getTop10CountryNeedExpByMacroIndividuals();