CREATE TABLE top_need_role_view AS
	
SELECT 
	p.person_id, 
	p.sex, 
	p.education, 
	p.region_iso, 
	p.region_name, 
	p.comuna_name, 
	p.date, 
	p.age, 
	p.age_range, 
	n.macro,
	w.palabra_inicio,
	w.palabra_fin	
FROM 
	person_view as p, 
	need as n, 
	person_need as pn,
	pair_roles as w,
	need_role_pairs as np
WHERE 
	p.person_id=pn.person_id AND 
	n.need_id=pn.need_id AND
	np.need_id=n.need_id AND
	np.pair_id=w.pair_id AND
	w.palabra_inicio IN 	
		(SELECT tnw.palabra_inicio from top_need_role_table as tnw where tnw.macro = n.macro) AND
	w.palabra_fin IN (SELECT tnw.palabra_inicio from top_need_role_table as tnw where tnw.macro = n.macro);

