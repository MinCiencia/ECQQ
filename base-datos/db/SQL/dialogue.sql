CREATE TABLE dialogue
(
	file_id varchar(32) PRIMARY KEY,
	date date,
	init_time time,
	end_time time,
	location varchar(128),
	address text,
	comuna integer REFERENCES comuna(id),
	n_members integer,
	group_name text
);
