import pandas as pd
import numpy as np
import os

from core.vectorize import WordVecVectorizer
from sklearn.model_selection import StratifiedKFold

from gensim.models.keyedvectors import KeyedVectors
from gensim import corpora, models

def map_to_reduced(data):
    # Reducing from 20 to 13 classes.

    exchange = {'Participación Ciudadana':'Participacion', 
            'Familia':'Reciprocidad-Redes', 
            'Participación Electoral':'Participacion', 
            'Protesta Social':'Protesta Social', 
            'Reciprocidad-Redes':'Reciprocidad-Redes', 
            'Sustentabilidad Ambiental':'Sustentabilidad Ambiental', 
            'Compromiso con la Educación y Autoeducación':'Educación y autoeducación', 
            'Difusión de la Información':'Educación y autoeducación', 
            'Voluntariado':'Voluntariado', 
            'Cultura':'Cultura', 
            'Trabajo':'Trabajo',
            'Accountability':'Confianza en las instituciones', 
            'Combatir Delincuencia':'Combatir Delincuencia', 
            'Defensa de derechos':'Defensa de derechos', 
            'Defensa de derechos, Inclusión y Diversidad':'Inclusión y Diversidad',
            'Inclusión y Diversidad':'Inclusión y Diversidad', 
            'Apoyo a Pueblos Originarios':'Inclusión y Diversidad', 
            'Emprendimiento':'Trabajo', 
            'Autocuidado y Salud':'Autocuidado y Salud', 
            'Erradicar violencia contra la Mujer':'Erradicar violencia contra la Mujer', 
            'Tenencia Responsable':'Tenencia Responsable', 
            'Confiar en la Institucionalidad':'Confianza en las instituciones',
            'NR': 'NR'}
    
    data['resume'] = data.resume.map(exchange)
    return data


def generate_embeddings(args, embedding_filename):
    data_path = '{}/contributions.xlsx'.format(args.data_path)
    data = pd.read_excel(data_path)
    
    # FILTERING THE NON LABELED NR VALUES
    if args.reduced_classes:
        data = map_to_reduced(data)

    #GENERATE EMBEDDINGS FROM FASTTEXT TRAINED ON SBW CORPUS.
    w2v = WordVecVectorizer('../word-embeddings/fasttext-sbwc.vec')

    id_ = data.con_id.values.reshape(-1,1)
    tokens = data.tokens.values
    labels = data.resume.values.reshape(-1,1)

    embedding = w2v.transform(tokens)
    
    lbl_list = labels.reshape(-1)

    labeled_data = np.concatenate([id_[lbl_list!='NR'], labels[lbl_list!='NR'], embedding[lbl_list!='NR']], axis=1)
    unlabeled_data = np.concatenate([id_[lbl_list=='NR'], labels[lbl_list=='NR'], embedding[lbl_list=='NR']], axis=1)

    np.save('{}/{}'.format(args.data_path, embedding_filename), labeled_data)
    np.save('{}/unlabeled_{}'.format(args.data_path, embedding_filename), unlabeled_data)
    print('Embeddings saved.')

    skf = StratifiedKFold(n_splits=3)
    for i, (train_index, test_index) in enumerate(skf.split(labeled_data[:,2:], labeled_data[:,1])):
        np.save('{}/split_{}_train.npy'.format(args.data_path, i), train_index)
        np.save('{}/split_{}_test.npy'.format(args.data_path, i), test_index)
    print('train/test splits created.')

def load_data(args):
    if args.reduced_classes:
        embedding_filename = 'contributions_fasttext-sbwc_reduced.npy'
    else:
        embedding_filename = 'contributions_fasttext-sbwc.npy'
    
    if args.create_embedding:
        generate_embeddings(args, embedding_filename)

    data = np.load('{}/{}'.format(args.data_path, embedding_filename), allow_pickle=True)
    train_ixs = np.load('{}/split_{}_train.npy'.format(args.data_path, args.split), allow_pickle=True)
    test_ixs = np.load('{}/split_{}_test.npy'.format(args.data_path, args.split), allow_pickle=True)

    return data[train_ixs][:,2:], data[test_ixs][:,2:], data[train_ixs][:,1], data[test_ixs][:,1]

