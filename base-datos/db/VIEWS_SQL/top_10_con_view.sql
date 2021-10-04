CREATE VIEW top_10_con AS
	
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
	c.macro
	
FROM 
	person_view as p, 
	contribution as c, 
	person_contribution as pc
WHERE 
	p.person_id=pc.person_id AND 
	c.con_id=pc.con_id AND 
	c.macro IN 	
		(SELECT c.macro from top_10_con_table as c);
