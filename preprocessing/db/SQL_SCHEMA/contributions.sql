CREATE TABLE contributions
(
	id integer PRIMARY KEY,
	diag_id varchar(64) REFERENCES dialogues(id),
	ind_id varchar(64) REFERENCES individuals(id),
	text varchar(4096),
	tokens json,
	macro varchar(4096),
	is_online boolean	
);
