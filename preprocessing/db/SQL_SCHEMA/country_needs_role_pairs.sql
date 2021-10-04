CREATE TABLE country_needs_role_pairs
(
	id integer PRIMARY KEY,
	country_need_id integer references country_needs(id),
	word_1 varchar(64),
	word_2 varchar(64)
);
