CREATE TABLE persons
(
	id varchar(64) PRIMARY KEY,
	age integer,
	sex varchar(5),
	level varchar(64),
	comuna integer REFERENCES comunas(id),
	age_range varchar(8)	
);