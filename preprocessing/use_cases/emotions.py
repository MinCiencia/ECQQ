import use_cases.utils.textools as tt
import pandas as pd
import numpy as np
import re, os



def get_dialogues_info(frame):
    
    frame = frame.replace("'",'"')
    question_cols = [x for x in frame.columns if re.search(r'P1_\d_[A|B]', x)]

    emo_list, explanations = [], []
    emo_token, exp_token = [], []
    file_ids = []
    for column in question_cols:
        if column.endswith('A'):
            name = tt.to_unicode(frame[column])
            emo_token.append(tt.tokenize(name))
            emo_list.append(name)
            file_ids.append(frame['ID Archivo'])

        elif column.endswith('B'):
            exp = tt.to_unicode(frame[column])
            explanations.append(exp)
            exp_token.append(tt.tokenize(exp))

    file_ids = pd.concat(file_ids)
    emo_token = pd.concat(emo_token)
    emo_list = pd.concat(emo_list)
    explanations = pd.concat(explanations)
    exp_token = pd.concat(exp_token)

    df_emo = pd.DataFrame()
    df_emo['diag_id'] = file_ids
    df_emo['name'] = emo_list
    df_emo['name_tokens'] = emo_token
    df_emo['macro'] = emo_list
    df_emo['exp'] = explanations
    df_emo['exp_tokens'] = exp_token
    cond  = ~df_emo['name'].isna()
    df_emo = df_emo[cond]
    df_emo = df_emo.replace({'nr':''})

    df_emo['diag_id'] = tt.to_unicode(df_emo['diag_id'])
    return df_emo

def get_individual_info(frame_path, frame_online):    
    frame = pd.read_excel(frame_path, 'P1_HOMOLOGADA')

    frame = frame.replace("'",'"')
    frame_online = frame_online.replace("'",'"')

    frames = []
    for i in range(1, 3):
        handwritten = frame[['id', 'p1_{}_a'.format(i), 'p1_{}_b'.format(i)]]
        handwritten.columns = ['ind_id', 'name', 'exp']

        online = frame_online[['RUN',
                               '{} >> Emociones / Sentimientos / Sensaciones'.format(i),
                               '{} >> Explique lo mencionado'.format(i)]]
        online.columns = ['ind_id', 'name', 'exp']

        handwritten['is_online'] = False
        online['is_online'] = True

        p = pd.concat([handwritten, online])
        p['name'] = tt.to_unicode(p['name'])
        p['exp'] = tt.to_unicode(p['exp'])
        frames.append(p)

    table = pd.concat(frames)
    table = table.fillna('')
    table = table.replace({'nr':'','nan':'', 'NR':'', 'NaN':'', np.nan:''})
    table['name_tokens'] = tt.tokenize(table['name'])
    table['exp_tokens'] = tt.tokenize(table['exp'])
    return table


def create_table_emotions(frame, frame_ind_path, frame_ind_online):
    
    emo_diag = get_dialogues_info(frame)
    ind_diag = get_individual_info(frame_ind_path, frame_ind_online)

    emo_diag['is_online'] = True

    table = pd.concat([emo_diag, ind_diag])

    table = table.fillna('')
    table = tt.eliminate_nrs(table)
    table = table[table['name'] != '']
    table['id'] = range(0, table.shape[0])
    table = table[['id', 'diag_id','ind_id','name',
                   'name_tokens', 'macro', 'exp', 'exp_tokens',
                   'is_online']]
    return table

def to_sql(frame, output_file):
    values = list()

    for index, row in frame.iterrows():
        id = row['id']        
        
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
        
        is_online = row['is_online']     

        name_tokens_str = tt.tokens_to_str(name_tokens)

        exp_tokens_str = tt.tokens_to_str(exp_tokens)

        diag_id = row['diag_id']
        ind_id = row['ind_id']
        if diag_id == '':
            string_value = '''({},NULL,\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{})'''.format(
                id,                 
                ind_id,
                name,
                name_tokens_str,
                macro,
                exp,
                exp_tokens_str,
                is_online
            )
            values.append(string_value)
        
        elif ind_id == '':
            string_value = '''({},\'{}\',NULL,\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{})'''.format(
                id,                 
                diag_id,
                name,
                name_tokens_str,
                macro,
                exp,
                exp_tokens_str,
                is_online
            )
            values.append(string_value)
        else:    
            string_value = '''({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{})'''.format(
                id,
                diag_id, 
                ind_id,
                name,
                name_tokens_str,
                macro,
                exp,
                exp_tokens_str,
                is_online
                )
            values.append(string_value)     

    with open(output_file, 'w') as new_file:
        for index, value in enumerate(values):
            if index == 0:
                print('INSERT INTO emotions VALUES {},'.format(value), file=new_file)
            elif index == len(values) - 1:
                print('''{};'''.format(value), file=new_file)
            else:
                print('{},'.format(value), file=new_file)    
