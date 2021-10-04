CREATE TABLE country_needs
(
	id integer PRIMARY KEY,
	diag_id varchar(64) REFERENCES dialogues(id),
	ind_id varchar(64) REFERENCES individuals(id),
	name varchar(4096),
	name_tokens json,
	macro varchar(257),
	exp varchar(2048),
	exp_tokens json,
	role varchar(1025),
	role_tokens json,
	actor varchar(4097),
	priority integer,	
	is_online boolean	
);
