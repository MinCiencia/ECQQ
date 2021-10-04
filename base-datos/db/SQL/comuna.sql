CREATE TABLE comuna
(
	id integer PRIMARY KEY,
	region_iso varchar(64) references region(iso),
	name varchar(64)
);
