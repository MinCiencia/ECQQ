CREATE VIEW personal_needs_dialogues_pairs_view as
SELECT 
	d.id, 
	d.date, 
	d.valid,
	n.macro,
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
	personal_needs as n, 
	dialogues as d,
	personal_needs_pairs as w
WHERE 
	d.comuna = comunas.id and 
	comunas.region_iso = regions.iso and
	n.diag_id = d.id and
	w.personal_need_id = n.id and
	w.word_1 IN 
		(SELECT tnw.word_1 from top_personal_needs_pairs_dialogues as tnw where tnw.macro = n.macro) AND
	w.word_2 IN (SELECT tnw.word_1 from top_personal_needs_pairs_dialogues as tnw where tnw.macro = n.macro)
