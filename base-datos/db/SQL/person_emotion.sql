CREATE TABLE person_emotion
(
	emo_id integer references emotion(emo_id),
	person_id integer references person(person_id)
);
