import multiprocessing
import use_cases.utils.textools as tt
import pandas as pd
import numpy as np
import re, os

from joblib import Parallel, delayed



def get_dialogues_info(frame):
    frame = frame.replace("'",'"')
    # Init Pipeline
    frame['Grupo'] = tt.check_nan(frame['Grupo'])

    frames = []
    for i in range(1, 6):
        col = frame[['ID Archivo', 'P5_{}'.format(i)]]
        col.columns = ['diag_id', 'text']
        col['text'] = tt.to_unicode(col['text'])
        frames.append(col)

        table = pd.concat(frames)
        table = table[['diag_id', 'text']]

    table['diag_id'] = tt.to_unicode(table['diag_id'])

    return table

def get_individuals_info(frame, frame_online):
    frame = frame.replace("'",'"')
    frame_online = frame_online.replace("'",'"')

    online = frame_online[['RUN',
    '5. Pregunta: ¿Cuál es mi contribución personal para construir el Chile que queremos?']]

    handwritten = frame[['id', 'p5']]
    handwritten.columns = ['ind_id', 'text']
    online.columns = ['ind_id', 'text']

    handwritten = tt.to_unicode(handwritten)
    online = tt.to_unicode(online)

    handwritten['is_online'] = False
    online['is_online'] = True
    table = pd.concat([handwritten, online])
    return table

def create_table_contributions(frame, frame_ind, frame_online_ind):
    dialog = get_dialogues_info(frame)
    individual = get_individuals_info(frame_ind, frame_online_ind)

    dialog['is_online'] = False

    table = pd.concat([dialog, individual])

    table['id'] = range(0, table.shape[0])
    table['tokens'] = tt.tokenize(table['text'])
    table['macro'] = table['text']
    table = table.fillna('')
    table = tt.eliminate_nrs(table)
    table = table[table['text'] != '']
    table = table[['id', 'diag_id','ind_id', 'text', 'tokens',
                   'macro', 'is_online']]
    return table

def to_sql(frame, output_file):
    values = list()

    for index, row in frame.iterrows():
        id = row['id']
        text = row['text'].replace('\'','')
        is_online = row['is_online']
        
        macro = row['macro']

        if macro != None:
            if macro == '\'':
                macro = ''
            if macro != '':
                macro = macro.replace('\'','')    

        tokens = row['tokens']

        tokens_str = tt.tokens_to_str(tokens) 

        diag_id = row['diag_id']
        ind_id = row['ind_id']
        if diag_id == '':
            string_value = '''({},NULL,\'{}\',\'{}\',\'{}\',\'{}\',{})'''.format(
                id,
                ind_id,
                text, 
                tokens_str, 
                macro,
                is_online
            )
            values.append(string_value)  
        
        elif ind_id == '':
            string_value = '''({},\'{}\',NULL,\'{}\',\'{}\',\'{}\',{})'''.format(
                id,
                diag_id, 
                text, 
                tokens_str, 
                macro,
                is_online
            )
            values.append(string_value)  
        else:    
            string_value = '''({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{})'''.format(
                id,
                diag_id, 
                ind_id,
                text, 
                tokens_str, 
                macro,
                is_online
            )
            values.append(string_value)  

    with open(output_file, 'w') as new_file:
        for index, value in enumerate(values):
            if index == 0:
                print('INSERT INTO contributions VALUES {},'.format(value), file=new_file)
            elif index == len(values) - 1:
                print('''{};'''.format(value), file=new_file)
            else:
                print('{},'.format(value), file=new_file)
