CREATE TABLE person
(
	person_id integer PRIMARY KEY,
	file_id varchar(32) REFERENCES dialogue(file_id),
	age integer,
	sex varchar(16),
	level varchar(64),
	age_range varchar(5),	
	comuna integer REFERENCES comuna(id)
);
