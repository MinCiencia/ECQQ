CREATE TABLE individuals
(
	id varchar(64) PRIMARY KEY,
	date date,
	age integer,
    comuna_id integer REFERENCES comunas(id),
	level varchar(64),
	is_valid Boolean,
	age_range varchar(8),
	online Boolean
);