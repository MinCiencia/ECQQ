CREATE VIEW personal_needs_individuals_view as 
SELECT 
	ind.id, 
	ind.date, 
	ind.online,
	ind.age,
    ind.level as education,
    ind.age_range, 
	ind.is_valid,
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
	individuals as ind
WHERE
	ind.comuna_id = comunas.id and 
	comunas.region_iso = regions.iso and
	pn.ind_id = ind.id
