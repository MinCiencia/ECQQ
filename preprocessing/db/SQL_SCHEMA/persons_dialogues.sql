CREATE TABLE persons_dialogues
(
	person_id varchar(64) REFERENCES persons(id),
	diag_id varchar(64) REFERENCES dialogues(id)
);
