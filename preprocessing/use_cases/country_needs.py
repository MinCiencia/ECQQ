import multiprocessing
import use_cases.utils.textools as tt
import pandas as pd
import numpy as np
import re, os

from joblib import Parallel, delayed


def check_priority_in_text(row):
    need = row['name']
    priority = row['priority']

    needs = [need]
    priorities = []
    # Clean Needs
    if re.search(r'\d+', need):
        cases = re.findall(r'\d+', need)
        # Asumming kind of enumeration
        if len(cases) > 1:
            cases = [int(c) for c in cases]
            delta = np.diff(cases)
            priorities = np.array(cases)+1
            # consecutive cases should be 1-spaced located
            if np.mean(delta) == 1:
                splits = re.split(r'\d', need)
                splits = [re.findall('[A-z]+', w) for w in splits]
                needs  = [s[0] for s in splits if len(s) != 0]

        # Identifying priorities in the name
        if len(cases) == 1:
            # If there is a number before the EOS token or a point
            pseudo_prior = re.search(r'\s\d($|\.)', need)
            needs = [re.search(r'\w+', need).group().strip()]

            if pseudo_prior:
                pseudo_prior = pseudo_prior.group()
                pseudo_prior = int(str(pseudo_prior).strip().split('.')[0])
                # if there is not priority
                if priority:
                    priority = pseudo_prior
            priorities.append(priority)

    if priorities == []:
        priorities = [priority]

    row['name'] = needs
    row['priority'] = priorities
    return row

def clean_string(text):
    text = tt.to_unicode(text)
    text = " ".join(text.split())
    f = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    f = re.sub(' +', ' ',f.strip())
    return f

def get_roles(role_frame, fide, need, exp, prior, who='estado'):

    exp = clean_string(exp)
    role_frame = clean_string(role_frame)

    tuples = []
    if '-' in role_frame:
        roles_frame = role_frame.split('-')
        for rol in roles_frame:
            tuples.append([fide, need, who, rol, exp, prior])
    else:
        tuples.append([fide, need, who, role_frame, exp, prior])

    return tuples

def fix_priority(x):
    if x == 'urgencia (solo una)':
        x = '' 


def get_dialogues_info(frame):
    frame = frame.replace("'",'"')
    frames = []
    for k in range(1, 6):
        need_0 = frame[['ID Archivo',
                        'P2_{}_A'.format(k),
                        'P2_{}_B'.format(k),
                        'P2_{}_C'.format(k)]]
        need_0.columns = ['file_id', 'name', 'exp', 'priority']
        need_1 = frame[['ID Archivo',
                        'P4_{}_A'.format(k),
                        'P4_{}_B'.format(k),
                        'P4_{}_C'.format(k),
                        'P4_{}_D'.format(k)]]
        need_1.columns = ['file_id', 'name', 'state_role', 'actor', 'role_actor']

        need_0 = tt.to_unicode(need_0)
        need_1 = tt.to_unicode(need_1)

        # Check priority
        need_0 = need_0.apply(lambda x: check_priority_in_text(x), 1)
        rows = [(c['file_id'], n, c['exp'], int(c['priority'][0])) for k, c in need_0.iterrows()\
                    for n in c['name']]
        need_0 = pd.DataFrame(rows, columns=['file_id','name', 'exp', 'priority'])

        need_1_other = need_1[need_1['actor'] != 'nan'][['file_id', 'name', 'actor', 'role_actor']]
        need_1_state = need_1[need_1['actor'] == 'nan'][['file_id', 'name', 'state_role']]
        need_1_state['actor'] = ['estado']*need_1_state.shape[0]
        need_1_state.columns = ['file_id', 'name', 'role', 'actor']
        need_1_other.columns = ['file_id', 'name', 'actor', 'role']
        need_1 = pd.concat([need_1_state, need_1_other])

        result = pd.concat([need_0, need_1], axis=1)

        result = pd.merge(need_0, need_1, how="outer", on=["name", "file_id"])

        frames.append(result)

    #source id + isdiag

    needs = pd.concat(frames)
    needs['name_tokens'] = tt.tokenize(needs['name'])
    needs['macro'] = ['']*needs.shape[0]
    needs['exp_tokens'] = tt.tokenize(needs['exp'])
    needs['role_tokens'] = tt.tokenize(needs['role'])
    needs = needs.rename(columns={'file_id':'diag_id'})

    needs = needs[['diag_id', 'name', 'name_tokens', 'macro', 'exp',
                    'exp_tokens', 'role', 'role_tokens', 'actor', 'priority']]

    needs = needs.fillna('')
    needs = needs.replace({'NR':'', 'nan':'', '-':'', 'nr':'', np.nan:''})
    return needs

def get_individuals_info(frame, indiv_path, online_path):
    ocols = [1]+list(range(12,21))+list(range(27,39))
    p4_online = pd.read_excel(online_path, 'Sheet1', usecols=ocols)
    ocols = [1]+list(range(8, 21))    

    p4_handwritten = pd.read_excel(indiv_path, 'P4_ORDEN_CUESTIONARIO',
                                   usecols=ocols)

    frame = frame.replace("'",'"')
    p4_online = p4_online.replace("'",'"')
    p4_handwritten = p4_handwritten.replace("'",'"')

    frames = []
    for i in range(1, 4):
        # ======== ONLINE ========
        online = p4_online[['RUN',
                            # '{} >> Necesidad que enfrenta el país'.format(i),
                            '{} >> Explique lo mencionado.1'.format(i),
                            '{} >> Urgencia (solo una)'.format(i),
                            '{} >> Necesidades del país identificadas'.format(i),
                            '{} >> Rol del Estado (Describa)'.format(i),
                            '{} >> Actor social (empresa, organizaciones sociales, medios de comunicación, comunidad, etc)'.format(i),
                            '{} >> Rol del actor social (Describa)'.format(i)]]

        online.columns = ['ind_id', 'exp', 'priority', 'name', 'state_role', 'actor', 'actor_role']

        online = tt.to_unicode(online)


        online['actor'] = online['actor'].apply(lambda x: tt.check_string(x))
        online = online.replace({'nr':'', 'nan':'', 'NR':'', 'NaN':'', np.nan:''})

        online_a = online[online['actor'] == ''][['ind_id', 'exp', 'priority', 'name', 'state_role']]
        online_a['actor'] = ['estado']*online_a.shape[0]
        online_a = online_a.rename(columns={'state_role':'role'})

        online_b = online[online['actor'] != ''][['ind_id','exp', 'priority', 'name', 'actor', 'actor_role']]
        online_b = online_b.rename(columns={'actor_role':'role'})


        online = pd.concat([online_a, online_b])

        online['priority'] = online['priority'].apply(lambda x: fix_priority(x), 1)

        # ======== HANDWRITTEN ========
        handwritten = p4_handwritten[['correlativo_digitación',
                                      'p4_n{}'.format(i),
                                      'p4_re_{}'.format(i),
                                      'p4_oa_{}'.format(i),
                                      'p4_roa_{}'.format(i)]]

        ids = [frame[frame['correlativo_digitación'] == corr]['id'].values[0]\
                            for corr in handwritten['correlativo_digitación']]

        handwritten['ind_id'] = ids
        handwritten = handwritten.replace({'nr':'','nan':'', 'NR':'', 'NaN':'', np.nan:''})
        handwritten = handwritten[handwritten['p4_n{}'.format(i)] != '']
        handwritten.columns = ['cd', 'name', 'state_role', 'actor', 'actor_role', 'ind_id']

        handwritten_a = handwritten[handwritten['actor'] == ''][['ind_id', 'name', 'state_role']]
        handwritten_a['actor'] = ['estado']*handwritten_a.shape[0]
        handwritten_a = handwritten_a.rename(columns={'state_role':'role'})
        handwritten_b = handwritten[handwritten['actor'] != ''][['ind_id', 'name', 'actor', 'actor_role']]
        handwritten_b = handwritten_b.rename(columns={'actor_role':'role'})
        handwritten = pd.concat([handwritten_a, handwritten_b])
        handwritten = tt.to_unicode(handwritten)

        handwritten_2 = frame[['id',
                               'p2_{}_a'.format(i),
                               'p2_{}_b'.format(i),
                               'p2_urg']]

        handwritten_2.columns = ['ind_id', 'name', 'arg', 'priority']
        handwritten_2 = handwritten_2.replace({'nr':'','nan':'', 'NR':'', 'NaN':'', np.nan:''})
        handwritten_2 = tt.to_unicode(handwritten_2)

        handwritten = pd.merge(handwritten, handwritten_2,
                               how="outer", on=["name", "ind_id"])

        handwritten['is_online'] = False
        online['is_online'] = True

        result = pd.concat([handwritten, online])

        frames.append(result)

    needs = pd.concat(frames)
    needs['name_tokens'] = tt.tokenize(needs['name'])
    needs['macro'] = ['']*needs.shape[0]
    needs['exp_tokens'] = tt.tokenize(needs['exp'])
    needs['role_tokens'] = tt.tokenize(needs['role'])

    needs = needs[['ind_id', 'name', 'name_tokens', 'macro', 'exp',
                    'exp_tokens', 'role', 'role_tokens', 'actor', 'priority', 'is_online']]

    needs = needs.fillna('')
    needs = needs.replace({'NR':'', 'nan':'', '-':''})
    return needs


def create_table_country_needs(diag_frame, ind_survey, indiv_path, online_path):


    needs = get_dialogues_info(diag_frame)
    needs['is_online'] = False

    needs_i = get_individuals_info(ind_survey, indiv_path, online_path)   

    need_table = pd.concat([needs, needs_i])

    need_table = need_table.fillna('')
    need_table = tt.eliminate_nrs(need_table)
    need_table = need_table[need_table['name'] != '']
    need_table['id'] = range(0, need_table.shape[0])

    need_table = need_table[['id', 'diag_id', 'ind_id', 'name', 'name_tokens',
                              'macro', 'exp', 'exp_tokens', 'role',
                              'role_tokens', 'actor', 'priority', 'is_online' ]]

    need_table = need_table.drop(need_table[(need_table['diag_id'] == '') & (need_table['ind_id'] == '')].index)                              
    return need_table

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

        role = row['role'].replace('\'','')
        role_tokens = row['role_tokens']

        actor = row['actor'].replace('\'','')  
        priority = row['priority']    

        if priority == '':
            priority = 'NULL'
        else:
            priority = int(priority)    
        
        is_online = row['is_online']     

        name_tokens_str = tt.tokens_to_str(name_tokens)

        exp_tokens_str = tt.tokens_to_str(exp_tokens)

        role_tokens_str = tt.tokens_to_str(role_tokens)

        diag_id = row['diag_id']
        ind_id = row['ind_id']
        if diag_id == '':
            string_value = '''({},NULL,\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},{})'''.format(
                id,
                ind_id,
                name,
                name_tokens_str,
                macro,
                exp,
                exp_tokens_str,
                role,
                role_tokens_str,
                actor,
                priority,
                is_online
            )
            values.append(string_value)
        
        elif ind_id == '':
            string_value = '''({},\'{}\',NULL,\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},{})'''.format(
                id,
                diag_id, 
                name,
                name_tokens_str,
                macro,
                exp,
                exp_tokens_str,
                role,
                role_tokens_str,
                actor,
                priority,
                is_online
            )
            values.append(string_value)
        else:    
            string_value = '''({},\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',{},{})'''.format(
                id,
                diag_id, 
                ind_id,
                name,
                name_tokens_str,
                macro,
                exp,
                exp_tokens_str,
                role,
                role_tokens_str,
                actor,
                priority,
                is_online
            )
            values.append(string_value)     

    with open(output_file, 'w') as new_file:
        for index, value in enumerate(values):
            if index == 0:
                print('INSERT INTO country_needs VALUES {},'.format(value), file=new_file)
            elif index == len(values) - 1:
                print('''{};'''.format(value), file=new_file)
            else:
                print('{},'.format(value), file=new_file)

