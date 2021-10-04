CREATE VIEW emotions_dialogue_view AS
SELECT 
	d.id, 
	d.date, 
	d.valid,
	e.macro,
	regions.iso as region_iso, 
	regions.name as region_name, 
	regions.numero as region_number,
	regions.orden as region_order, 
	comunas.name as comuna_name
FROM 
	comunas,
	regions,
	emotions as e, 
	dialogues as d
WHERE
	d.comuna = comunas.id and 
	comunas.region_iso = regions.iso and
	e.diag_id = d.id and
	e.macro <> ''