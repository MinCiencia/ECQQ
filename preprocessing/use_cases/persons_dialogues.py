import pandas as pd
import numpy as np

def create_table_persons_dialogues(persons):
	new_persons = persons.copy()
	new_persons = new_persons.drop_duplicates(subset=['id'])
	new_persons = new_persons.drop(columns=['diag_id'])

	persons_dialogues = persons.copy()

	persons_dialogues = persons_dialogues[['id','diag_id']]
	persons_dialogues.columns = ['person_id', 'diag_id']

	return new_persons, persons_dialogues
