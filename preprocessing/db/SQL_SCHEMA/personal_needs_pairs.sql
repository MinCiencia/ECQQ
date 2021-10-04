CREATE TABLE personal_needs_pairs
(
	id integer PRIMARY KEY,
	personal_need_id integer references personal_needs(id),
	word_1 varchar(128),
	word_2 varchar(128)
);
