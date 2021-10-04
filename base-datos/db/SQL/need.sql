CREATE TABLE need
(
	need_id integer PRIMARY KEY,
	name varchar(128),
	actor varchar(128),
	role varchar(512),
	explanation varchar(512),
	priority integer,	
	role_token json,
	exp_token json,
	macro varchar(128)
);
