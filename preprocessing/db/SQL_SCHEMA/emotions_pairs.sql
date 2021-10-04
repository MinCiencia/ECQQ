CREATE TABLE emotions_pairs
(
	id integer PRIMARY KEY,
	emotion_id integer references emotions(id),
	word_1 varchar(64),
	word_2 varchar(64)
);
