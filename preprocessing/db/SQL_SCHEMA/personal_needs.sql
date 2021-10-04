CREATE TABLE personal_needs
(
	id integer PRIMARY KEY,
	diag_id varchar(64) REFERENCES dialogues(id),
	ind_id varchar(64) REFERENCES individuals(id),
	name varchar(1024),
	name_tokens json,
	macro varchar(513),
	exp varchar(2048),
	exp_tokens json,
	priority integer,	
	is_online boolean	
);
