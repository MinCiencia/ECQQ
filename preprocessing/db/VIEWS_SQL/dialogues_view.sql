CREATE VIEW dialogues_view AS
SELECT 
	d.id, 
	d.date, 
	d.valid,
	regions.iso as region_iso, 
	regions.name as region_name, 
	regions.numero as region_number,
	regions.orden as region_order,  
	comunas.name as comuna_name
FROM 
	comunas,
	regions,
	dialogues as d
WHERE 
	d.comuna = comunas.id and 
	comunas.region_iso = regions.iso