CREATE TABLE need_role_dialogue_view AS
SELECT 
	d.file_id, 
	d.date, 
	n.macro,
	n.actor,
	region.iso as region_iso, 
	region.name as region_name, 
	region.numero as region_number, 
	comuna.name as comuna_name,
	w.palabra_inicio,
	w.palabra_fin
FROM
	comuna,
	region,
	person as p, 
	need as n, 
	person_need as pn,
	dialogue as d,
	pair_roles as w,
	need_role_pairs as np
WHERE 
	d.comuna = comuna.id and 
	comuna.region_iso = region.iso and
	p.file_id = d.file_id AND
	p.person_id=pn.person_id AND 
	n.need_id=pn.need_id AND
	np.need_id=n.need_id AND
	np.pair_id=w.pair_id AND
	w.palabra_inicio IN 
		(SELECT tnw.palabra_inicio from top_need_role_table as tnw where tnw.macro = n.macro) AND
	w.palabra_fin IN (SELECT tnw.palabra_inicio from top_need_role_table as tnw where tnw.macro = n.macro)
GROUP BY 
	d.file_id,
	d.date, 
	n.macro,
	n.actor,
	w.palabra_inicio,
	w.palabra_fin,
	region.iso, 
	region.name, 
	region.numero, 
	comuna.name;

