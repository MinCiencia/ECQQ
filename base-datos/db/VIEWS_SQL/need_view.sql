create view need_view as 
select 	
	age,
	sex,
	level as education,
	age_range, 
	region.iso as region_iso, 
	region.name as region_name, 
	region.numero as region_number, 
	comuna.name as comuna_name, 
	need.role_token as role_token,
	need.exp_token as exp_token,
	need.role as role,
	need.explanation as explanation,
	need.macro as macro,
	dialogue.date as date
	
	
from 
	person,
	comuna,
	region,
	need,
	person_need,
	dialogue
where 
	person.comuna = comuna.id and 
	comuna.region_iso = region.iso and 
	person.person_id = person_need.person_id and 
	need.need_id = person_need.need_id and
	person.file_id = dialogue.file_id;
