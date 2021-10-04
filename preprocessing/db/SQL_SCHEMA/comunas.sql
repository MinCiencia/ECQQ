CREATE TABLE comunas
(
	id integer PRIMARY KEY,
	region_iso varchar(64) references regions(iso),
	name varchar(64)
);
