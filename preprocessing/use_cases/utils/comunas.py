import pandas as pd
import numpy as np
import unidecode

comunas = pd.read_csv('./data/comuna.csv')
comunas_name = np.array([unidecode.unidecode(x).lower() for x in comunas['name'].to_numpy()],dtype=str)
comunas_id = np.array(comunas['id'].to_numpy(), dtype=int)

comuna_code = dict(zip(comunas_name, comunas_id))

comunas_fix = {
    'isla  de pascua': 'isla de pascua',
    'trehuaco' : 'treguaco',
    'coccepcion' : 'concepcion',
    'conce' : 'concepcion',
    'concepcion.' : 'concepcion',
    'santiago centro' : 'santiago',
    'caleta tortel' : 'tortel',
    'puente' : 'puente alto',
    'san vicente de tagua tagua' : 'san vicente',
    'san vicente tagua tagua' : 'san vicente',
    'marchigue' : 'marchihue',
    'coihaique' : 'coyhaique',
    'coyihaque' : 'coyhaique',
    'haulpen' : 'hualpen',
    'vina': 'vina del mar',
    'la  serena': 'la serena',
    'huechurabs' : 'huechuraba',
    'providenica' : 'providencia',
    'providenca' : 'providencia',
    'cowuimbo' : 'coquimbo',
    'comuna de putre' : 'putre',
    'x region, chile' : 'nr',
    'v region' : 'nr',
    'alto hospicii' : 'alto hospicio',
    'san miguel.' : 'san miguel',
    'pozo amonte' : 'pozo almonte',
    'til til' : 'tiltil',
    'qta normal' : 'quinta normal',
    'quinta norma' : 'quinta normal',
    'milina' : 'molina',
    'batuco' : 'lampa',
    'la visterna' : 'la cisterna',
    '"puerto montt' : 'puerto montt',
    'extranjero' : 'nr',
    'cerrillos.' : 'cerrillos',
    'maipu (mientras)..' : 'maipu',
    'colchagua': 'nr',
    'san antonio comuna de cartagena': 'cartagena',
    'quemchi chiloe-' : 'quemchi',
    'rocas de santo domingo' : 'santo domingo',
    'la calera' : 'calera',
    'coyhique' : 'coyhaique',
    'cancun' : 'nr',
    'estados unidos' : 'nr',
    'gladstone' : 'nr',
    'qjillota' : 'quillota',
    'pac' : 'pedro aguirre cerda',
    'paihuano' : 'paiguano',
    'puerto aysen' : 'aysen',
    'provincia' : 'nr',
    'santioago' : 'santiago',
    'quilpue  (belloto)' : 'quilpue',
    'nan' : 'nr'
}

def get_comunas_id(x, col):
    try:
        x[col] = comuna_code[x[col]]
    except KeyError:
        x[col] = comuna_code['nr']

    return x


def fix_location_online(x):
    if pd.isna(x['Comuna']):
        if pd.isna(x['Comuna.1']):
            x['Comuna'] = ''
        else:
            x['Comuna'] = x['Comuna.1']
    try:
        x['Comuna'] = comuna_code[unidecode.unidecode(x['Comuna']).lower()]
    except KeyError:
        x['Comuna'] = comuna_code[comunas_fix[unidecode.unidecode(x['Comuna']).lower()]]

    return x

def fix_location(x):
    if x['comuna'] == 'nr':
        x['comuna'] = 1

    if pd.isna(x['comuna']):
        x['comuna'] = 1

    return x
