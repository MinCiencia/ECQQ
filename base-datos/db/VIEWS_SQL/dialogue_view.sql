CREATE VIEW dialogue_view AS
SELECT 
	d.file_id, 
	d.date, 
	region.iso as region_iso, 
	region.name as region_name, 
	region.numero as region_number, 
	comuna.name as comuna_name
FROM 
	comuna,
	region,
	person as p, 
	dialogue as d
WHERE 
	d.comuna = comuna.id and 
	comuna.region_iso = region.iso and
	p.file_id = d.file_id 
GROUP BY 
	d.file_id,
	d.date, 
	region.iso, 
	region.name, 
	region.numero, 
	comuna.name;