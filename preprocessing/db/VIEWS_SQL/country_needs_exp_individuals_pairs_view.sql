CREATE VIEW country_needs_exp_individuals_pairs_view AS
SELECT 
	ind.id, 
	ind.date,
	ind.online,
	ind.age,
	ind.level as education,
	ind.age_range, 
	ind.is_valid, 
	n.macro,
	n.actor,
	regions.iso as region_iso, 
	regions.name as region_name, 
	regions.numero as region_number,
	regions.orden as region_order, 
	comunas.name as comuna_name,
	w.word_1,
	w.word_2
FROM
	comunas,
	regions,
	country_needs as n, 
	individuals as ind,
	country_needs_exp_pairs as w
WHERE 
	ind.comuna_id = comunas.id and 
	comunas.region_iso = regions.iso and
	n.ind_id = ind.id and
	w.country_need_id = n.id and
	w.word_1 IN 
		(SELECT tnw.word_1 from top_country_needs_exp_pairs_individuals as tnw where tnw.macro = n.macro) AND
	w.word_2 IN (SELECT tnw.word_1 from top_country_needs_exp_pairs_individuals as tnw where tnw.macro = n.macro)
