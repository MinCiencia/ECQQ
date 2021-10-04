CREATE VIEW persons_view AS

SELECT 
        persons.id as person_id,
        dialogues.id as diag_id,
        age,
        sex,
        level as education,
        age_range, 
        regions.iso as region_iso, 
        regions.name as region_name, 
        regions.numero as region_number,
	regions.orden as region_order, 
        comunas.name as comuna_name,
        dialogues.date as date 

FROM
        persons,
        comunas,
        regions,
        dialogues,
        persons_dialogues
WHERE 
        persons.comuna = comunas.id and 
        comunas.region_iso = regions.iso and
        persons.id = persons_dialogues.person_id and
        dialogues.id = persons_dialogues.diag_id;
