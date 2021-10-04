CREATE TABLE person_contribution
(
	person_id integer references person(person_id),
	con_id integer references contribution(con_id)
);
