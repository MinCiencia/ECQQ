import use_cases.utils.textools as tt
import pandas as pd
import numpy as np
import uuid
import re, os

from use_cases.utils.formatter import (regiones_name,
									   regiones_iso,
				                       sex_wrong,
				                       education_options,
				                       education_wrong,
				                       education_name,
									   educ_dict)

from use_cases.utils.comunas import get_comunas_id

def fix_swapped(col, i):
	if col['LP_COD_SEXO_P{}'.format(i)] in sex_wrong:
		aux = col['LP_COD_SEXO_P{}'.format(i)]
		col['LP_COD_SEXO_P{}'.format(i)] = col['LP_COD_NIVEL_P{}'.format(i)]
		col['LP_COD_NIVEL_P{}'.format(i)] = aux.replace('_', ' ')

	if col['LP_COD_NIVEL_P{}'.format(i)] in education_wrong:
		aux = col['LP_COD_NIVEL_P{}'.format(i)]
		col['LP_COD_NIVEL_P{}'.format(i)] = col['LP_COD_SEXO_P{}'.format(i)].replace('_', ' ')
		col['LP_COD_SEXO_P{}'.format(i)] = aux

	return col

def apply_dict_education(col):
	col = educ_dict[col]
	return col

def invalid_person(x):
    if x['run'] == '':
        if x['age'] == '' and x['sex'] == '' and x['level'] == '' and x['comuna_id'] == 1:
            x['remove'] = True
        else:
            x['run'] = str(uuid.uuid4())
    return x 	

def distributed(frame, i):
	single = frame[['ID Archivo',
					'LP_RUN{}'.format(i),
	                'LP_EDAD{}'.format(i),
					'LP_COD_SEXO_P{}'.format(i),
					'LP_COD_NIVEL_P{}'.format(i),
					'LP_COMUNA{}'.format(i)]]

	single = tt.to_unicode(single)
	single = single.apply(lambda x: fix_swapped(x, i), 1)
	single.columns = ['diag_id', 'run', 'age', 'sex', 'level', 'comuna_id']

	single = single.apply(lambda x: get_comunas_id(x, 'comuna_id'), 1)
	single = single[~single['age'].isna()]
	single = single[single['sex'] != 'nan']
	def fn(x):
		if x == 'nr':
			return 0
		else:
			return x[:2]
	single['age'] = single['age'].apply(lambda x: fn(x))
	single['age'] = single['age'].astype(int)	
	single = tt.stratify_frame_by_age(single)
	single = single.replace({0:'', '0':'', 'nr':''})
	single['level'] = single['level'].apply(lambda x: apply_dict_education(x))
	return single

def create_table_persons(frame):
	max_member = 30
	frame['Grupo'] = tt.check_nan(frame['Grupo'])

	table_cols = []
	for i in range(1, max_member+1):
		dist = distributed(frame, i)		
		table_cols.append(dist)
	table = pd.concat(table_cols)

	table = tt.eliminate_nrs(table)

	table['remove'] = False
	table = table.apply(lambda x: invalid_person(x), 1)
	table = table[table['remove'] == False]
	table = table.drop(columns=['remove'])
	
	table = table.rename(columns={'run': 'id'})


	table = table[['id', 'diag_id', 'age', 'sex', 'level',
				   'comuna_id', 'age_range']]
			   
	return table
