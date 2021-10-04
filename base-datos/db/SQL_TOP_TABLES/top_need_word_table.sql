CREATE TABLE top_need_role_table (
    palabra_inicio varchar(64),
    macro varchar(128)
);

CREATE TABLE top_need_exp_table (
    palabra_inicio varchar(64),
    macro varchar(128)
);

CREATE OR REPLACE FUNCTION getTop10RoleByMacro() RETURNS void AS $$
declare
    TEMPROW record;
BEGIN
FOR temprow IN
        SELECT * FROM top_10_need_macro_table
    LOOP
        INSERT INTO top_need_role_table
        SELECT pair_roles.palabra_inicio, need.macro 
        FROM pair_roles, need_role_pairs, need
        WHERE 
          pair_roles.pair_id = need_role_pairs.pair_id AND
          need_role_pairs.need_id = need.need_id AND
          need.macro = temprow.macro
        GROUP BY pair_roles.palabra_inicio, need.macro
        ORDER BY COUNT(*) DESC LIMIT 10;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getTop10ExpByMacro() RETURNS void AS $$
declare
    TEMPROW record;
BEGIN
FOR temprow IN
        SELECT * FROM top_10_need_macro_table
    LOOP
        INSERT INTO top_need_exp_table
        SELECT pair_exp.palabra_inicio, need.macro 
        FROM pair_exp, need_exp_pairs, need
        WHERE 
          pair_exp.pair_id = need_exp_pairs.pair_id AND
          need_exp_pairs.need_id = need.need_id AND
          need.macro = temprow.macro
        GROUP BY pair_exp.palabra_inicio, need.macro
        ORDER BY COUNT(*) DESC LIMIT 10;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM getTop10RoleByMacro();
SELECT * FROM getTop10ExpByMacro();