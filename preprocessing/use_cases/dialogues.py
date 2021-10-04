import use_cases.utils.textools as tt
from use_cases.utils.comunas import get_comunas_id
import pandas as pd
import numpy as np
import re, os

def change_valid_to_bool(x):
    if x == '1':
        x = True
    else:
        x = False
    return x         

def create_table_dialogues(frame, filter):
    new_frame = frame.copy()
    filter = filter.rename(columns={'ID_diag': 'ID'})
    new_frame['Grupo'] = tt.check_nan(new_frame['Grupo'])
    new_frame = pd.merge(new_frame, filter, how="inner", on=["ID"])    

    new_frame = new_frame[['ID Archivo', 'Fecha', 'Hora Inicio',
                    'Hora Termino', 'Lugar', 'Dirección',
                    'Comuna', 'Participantes',
                    'Grupo', 'Valido']]


    new_frame = tt.to_unicode(new_frame)
    new_frame = tt.eliminate_nrs(new_frame)
    new_frame = new_frame.rename(columns={'file_id':'diag_id'})

    new_frame.columns =['id', 'date', 'init_time', 'end_time',
                    'location', 'address', 'comuna_id', 'n_members',
                    'group_name', 'valid']

    new_frame = new_frame.apply(lambda x: get_comunas_id(x, 'comuna_id'), 1)
    new_frame['valid'] = new_frame['valid'].apply(lambda x: change_valid_to_bool(x), 1)

    return new_frame
