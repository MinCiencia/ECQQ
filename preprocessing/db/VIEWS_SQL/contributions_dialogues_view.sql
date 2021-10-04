CREATE VIEW contributions_dialogues_view AS
SELECT 
	d.id, 
	d.date, 
	d.valid,
	c.macro,
	regions.iso as region_iso, 
	regions.name as region_name, 
	regions.numero as region_number,
	regions.orden as region_order, 
	comunas.name as comuna_name
FROM 
	comunas,
	regions,
	contributions as c, 
	dialogues as d
WHERE 
	d.comuna = comunas.id and 
	comunas.region_iso = regions.iso and
	c.diag_id = d.id and
	c.macro <> ''