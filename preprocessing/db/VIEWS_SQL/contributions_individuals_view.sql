CREATE VIEW contributions_individuals_view AS
SELECT 
	ind.id, 
	ind.date,
	ind.online,
	ind.age,
	ind.level as education,
	ind.age_range, 
	ind.is_valid,
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
	individuals as ind
WHERE 
	ind.comuna_id = comunas.id and 
	comunas.region_iso = regions.iso and
	c.ind_id = ind.id and
	c.macro <> ''