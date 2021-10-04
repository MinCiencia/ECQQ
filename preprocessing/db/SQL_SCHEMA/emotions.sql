CREATE TABLE emotions
(
	id integer PRIMARY KEY,
	diag_id varchar(64) REFERENCES dialogues(id),
	ind_id varchar(64) REFERENCES individuals(id),
	name varchar(2048),
	name_tokens json,
	macro varchar(2048),
	exp varchar(2048),
	exp_tokens json,
	is_online boolean
);