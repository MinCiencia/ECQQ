CREATE VIEW emotions_individuals_pairs_view AS
SELECT 
	ind.id, 
	ind.date, 
	ind.online,
	ind.age,
	ind.level as education,
	ind.age_range, 
	ind.is_valid,
	e.macro,
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
	emotions as e, 
	individuals as ind,
	emotions_pairs as w
WHERE 
	ind.comuna_id = comunas.id and 
	comunas.region_iso = regions.iso and
	e.ind_id = ind.id and
	w.emotion_id = e.id and
	w.word_1 IN 
		(SELECT tnw.word_1 from top_emotions_pairs_dialogues as tnw where tnw.macro = e.macro) AND
	w.word_2 IN (SELECT tnw.word_1 from top_emotions_pairs_dialogues as tnw where tnw.macro = e.macro)
