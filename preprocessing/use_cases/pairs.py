import pandas as pd

words_dict = {
    'mejor': 'mejorar',
    'sueldo': 'sueldos',
    'pension': 'pensiones',
    'mayor': 'mayores',
    'vivienda': 'casa',
    'cambio': 'cambios',
    'gente': 'personas',
    'debe': 'deben',
    'hijo': 'hijos',
    'adulto': 'adultos'
}

def create_pair_token(frame, col_tokens, id_source_name):  
    rows = []
    pair_id = 1

    for index, row in frame.iterrows():
        tokens = row[col_tokens]
        for i in range(0,len(tokens) - 1):
            if tokens[i] == 'si' or tokens[i+1] == 'si':
                continue
            word_1 = ''
            word_2 = ''
            if tokens[i] in words_dict.keys():
                word_1 = words_dict[tokens[i]]
            else:
                word_1 = tokens[i]    
            if tokens[i+1] in words_dict.keys():
                word_2 = words_dict[tokens[i+1]]
            else:
                word_2 = tokens[i+1] 
            if word_1 != word_2:         
                new_row = {
                    'id' : pair_id,
                    id_source_name : row['id'],
                    'word_1' : word_1,
                    'word_2' : word_2
                }
                rows.append(new_row)
                pair_id += 1         
    pairs = pd.DataFrame(rows, columns = ['id', id_source_name ,'word_1', 'word_2'])
    return pairs 
