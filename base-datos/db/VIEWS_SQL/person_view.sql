CREATE VIEW person_view AS

SELECT 
        person_id,
        age,
        sex,
        level as education,
        age_range, 
        region.iso as region_iso, 
        region.name as region_name, 
        region.numero as region_number, 
        comuna.name as comuna_name,
        dialogue.date as date

FROM
        person,
        comuna,
        region,
        dialogue
WHERE 
        person.comuna = comuna.id and 
        comuna.region_iso = region.iso and
        person.file_id = dialogue.file_id;
