CREATE VIEW emo_dialogue AS
SELECT 
	d.file_id, 
	d.date, 
	e.macro as name,
	region.iso as region_iso, 
	region.name as region_name, 
	region.numero as region_number, 
	comuna.name as comuna_name
FROM 
	comuna,
	region,
	person as p, 
	emotion as e, 
	person_emotion as pe,
	dialogue as d
WHERE
	d.comuna = comuna.id and 
	comuna.region_iso = region.iso and
	p.file_id = d.file_id AND
	p.person_id=pe.person_id AND 
	e.emo_id=pe.emo_id
GROUP BY 
	d.file_id,
	d.date, 
	e.macro,
	region.iso, 
	region.name, 
	region.numero, 
	comuna.name;