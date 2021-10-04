import use_cases.utils.textools as tt
import pandas as pd
import numpy as np
import re, os


def get_dialogues_info(frame):
    frame = frame.replace("'",'"')
    # Init Pipeline
    frame['Grupo'] = tt.check_nan(frame['Grupo'])

    frames = []
    for k in range(1, 6):
        partial = pd.DataFrame()
        partial['diag_id'] = frame['ID Archivo']
        partial['name'] = tt.to_unicode(frame['P3_{}_A'.format(k)])
        partial['exp'] = tt.to_unicode(frame['P3_{}_B'.format(k)])

        frames.append(partial)

    needs = pd.concat(frames)
    needs['name_tokens'] = tt.tokenize(needs['name'])
    needs['exp_tokens'] = tt.tokenize(needs['exp'])
    needs['macro'] = needs['name']
    diag_groups = needs.groupby('diag_id')
    needs['priority'] = [i for g, f in diag_groups for i in range(f.shape[0])]
    needs['priority'] = needs['priority'].astype(int)
    needs    = needs[['diag_id', 'name', 'name_tokens',
    'exp', 'exp_tokens', 'macro', 'priority']]
    needs = needs[~needs['name'].isna()]
    needs = needs.replace({'NR': '', 'nr':'', 'nan':''})
    return needs

def get_individuals_info(frame, frame_online):
    frame = frame.replace("'",'"')
    frame_online = frame_online.replace("'",'"')
    
    frames = []
    for i in range(1, 4):
        p1 = frame[['id', 'p3_1_a', 'p3_1_b']]
        p1.columns = ['ind_id', 'name', 'exp']

        p2 = frame_online[[
        'RUN',
        '{} >> Necesidades que enfrento personalmente o que existen en mi hogar o familia'.format(i),
        '{} >> Explique lo mencionado.2'.format(i)]]
        p2.columns = ['ind_id', 'name', 'exp']

        p1['name'] =  tt.to_unicode(p1['name'])
        p1['exp'] =  tt.to_unicode(p1['exp'])
        p1['priority'] = np.ones(p1.shape[0], dtype=int)*i
        p2['name'] =  tt.to_unicode(p2['name'])
        p2['exp'] =  tt.to_unicode(p2['exp'])
        p2['priority'] = np.ones(p2.shape[0], dtype=int)*i

        p1['is_online'] = False
        p2['is_online'] = True

        p = pd.concat([p1, p2])


        frames.append(p)

    needs = pd.concat(frames)

    needs['name_tokens'] = tt.tokenize(needs['name'])
    needs['exp_tokens'] = tt.tokenize(needs['exp'])
    needs['macro'] = needs['name']

    needs    = needs[['ind_id', 'name', 'name_tokens',
    'exp', 'exp_tokens', 'macro', 'priority', 'is_online']]
    needs = needs[~needs['name'].isna()]
    needs = needs.replace({'NR': '', 'nr':'', 'nan':''})

    return needs

def create_table_personal_needs(frame, indv_frame, indv_online_frame):
    need_diag = get_dialogues_info(frame)
    need_ind = get_individuals_info(indv_frame, indv_online_frame)

    need_diag['is_online'] = False

    need_table = pd.concat([need_diag, need_ind])

    need_table = need_table.fillna('')
    need_table = tt.eliminate_nrs(need_table)
    need_table = need_table[need_table['name'] != '']
    need_table['id'] = range(0, need_table.shape[0])
    need_table['priority'] = need_table['priority'].astype(int)
    need_table['diag_id'] = tt.to_unicode(need_table['diag_id'])
    need_table = need_table[['id', 'diag_id', 'ind_id', 'name', 'name_tokens',
                             'exp', 'exp_tokens', 'macro', 'priority',
                             'is_online']]

    need_table = need_table.drop(need_table[(need_table['diag_id'] == '') & (need_table['ind_id'] == '')].index)                         
    return need_table

def to_sql(frame, output_file):
    values = list()

    for index, row in frame.iterrows():
        id = row['id']
        diag_id = row['diag_id']
        ind_id = row['ind_id']
        name = row['name'].replace('\'','')
        name_tokens = row['name_tokens']       
        
        macro = row['macro']
        if macro != None:
            if macro == '\'':
                macro = ''
            if macro != '':
                macro = macro.replace('\'','')

        exp = row['exp'].replace('\'','') 
        exp_tokens =  row['exp_tokens'] 

        priority = row['priority']    
        
        is_online = row['is_online']     

        name_tokens_str = tt.tokens_to_str(name_tokens)

        exp_tokens_str = tt.tokens_to_str(exp_tokens)

        if diag_id == '':
            string_value = '''({},NULL,\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},{})'''.format(
                id,
                ind_id,
                name,
                name_tokens_str,
                macro,
                exp,
                exp_tokens_str,
                priority,
                is_online
            )
            values.append(string_value)  
        
        elif ind_id == '':
            string_value = '''({},\'{}\',NULL,\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},{})'''.format(
                id,
                diag_id, 
                name,
                name_tokens_str,
                macro,
                exp,
                exp_tokens_str,
                priority,
                is_online
            )
            values.append(string_value)  
        else:    
            string_value = '''({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},{})'''.format(
                id,
                diag_id, 
                ind_id,
                name,
                name_tokens_str,
                macro,
                exp,
                exp_tokens_str,
                priority,
                is_online
            )
            values.append(string_value)  

    with open(output_file, 'w') as new_file:
        for index, value in enumerate(values):
            if index == 0:
                print('INSERT INTO personal_needs VALUES {},'.format(value), file=new_file)
            elif index == len(values) - 1:
                print('''{};'''.format(value), file=new_file)
            else:
                print('{},'.format(value), file=new_file)
