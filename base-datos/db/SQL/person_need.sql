CREATE TABLE person_need
(
	person_id integer references person(person_id),
	need_id integer references need(need_id)
);
