CREATE VIEW personal_needs_dialogue_view as 
SELECT 
	d.id, 
	d.date, 
	d.valid,
	pn.macro,
	pn.name,
	pn.priority,
	regions.iso as region_iso, 
	regions.name as region_name, 
	regions.numero as region_number,
	regions.orden as region_order, 
	comunas.name as comuna_name
FROM 
	comunas,
	regions,
	personal_needs as pn, 
	dialogues as d
WHERE
	d.comuna = comunas.id and 
	comunas.region_iso = regions.iso and
	pn.diag_id = d.id
