CREATE TABLE dialogues
(
	id varchar(32) PRIMARY KEY,
	date date,
	init_time time,
	end_time time,
	location varchar(128),
	address text,
	comuna integer REFERENCES comunas(id),
	n_members integer,
	group_name text,
	valid Boolean
);
