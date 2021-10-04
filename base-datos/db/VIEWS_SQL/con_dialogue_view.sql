CREATE VIEW con_dialogue AS
SELECT 
	d.file_id, 
	d.date, 
	c.macro,
	region.iso as region_iso, 
	region.name as region_name, 
	region.numero as region_number, 
	comuna.name as comuna_name
FROM 
	comuna,
	region,
	person as p, 
	contribution as c, 
	person_contribution as pc,
	dialogue as d
WHERE 
	d.comuna = comuna.id and 
	comuna.region_iso = region.iso and
	p.file_id = d.file_id AND
	p.person_id=pc.person_id AND 
	c.con_id=pc.con_id
GROUP BY 
	d.file_id,
	d.date, 
	c.macro,
	region.iso, 
	region.name, 
	region.numero, 
	comuna.name;