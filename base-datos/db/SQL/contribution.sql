CREATE TABLE contribution
(
	con_id integer PRIMARY KEY,
	text varchar(256),
	tokens json,
	label varchar(64),
	macro varchar(64)
);
