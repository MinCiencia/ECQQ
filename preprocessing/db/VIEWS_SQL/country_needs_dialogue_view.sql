CREATE VIEW country_needs_dialogue_view as 
SELECT 
	d.id, 
	d.date, 
	d.valid,
	cn.macro,
	cn.name,
	cn.role,
	cn.actor,
	cn.priority,
	regions.iso as region_iso, 
	regions.name as region_name, 
	regions.numero as region_number,
	regions.orden as region_order, 
	comunas.name as comuna_name
FROM 
	comunas,
	regions,
	country_needs as cn, 
	dialogues as d
WHERE
	d.comuna = comunas.id and 
	comunas.region_iso = regions.iso and
	cn.diag_id = d.id
