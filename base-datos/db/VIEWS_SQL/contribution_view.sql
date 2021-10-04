create view contribution_view as 
select 	
	
	age,
	sex,
	level as education,
	age_range, 
	region.iso as region_iso, 
	region.name as region_name, 
	region.numero as region_number, 
	comuna.name as comuna_name, 
	contribution.macro as contribution,
	dialogue.date as date
	
	
from 
	person,
	comuna,
	region,
	contribution,
	person_contribution,
	dialogue
where 
	person.comuna = comuna.id and 
	comuna.region_iso = region.iso and 
	person.person_id = person_contribution.person_id and 
	contribution.con_id = person_contribution.con_id and
	person.file_id = dialogue.file_id;
