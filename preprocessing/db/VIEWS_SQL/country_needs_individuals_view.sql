CREATE VIEW country_needs_individuals_view as 
SELECT 
	ind.id, 
	ind.date, 
	ind.online,
	ind.age,
	ind.level as education,
	ind.age_range, 
	ind.is_valid,
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
	individuals as ind
WHERE
	ind.comuna_id = comunas.id and 
	comunas.region_iso = regions.iso and
	cn.ind_id = ind.id
