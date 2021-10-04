# * We aknowledge Jorge Pérez from DCC UChile for provide the embeddings.
import os
import gzip
import wget
import shutil
import numpy as np

from gensim.models.keyedvectors import KeyedVectors
from gensim import corpora, models

def unzip_vector(filename, vector_file):
    with gzip.open(filename, 'rb') as f_in:
        with open(vector_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def download_embeddings(vector_file):
    url = 'http://dcc.uchile.cl/~jperez/word-embeddings/fasttext-sbwc.vec.gz' # *
    filename = wget.download(url)
    os.makedirs('../word-embeddings', exist_ok=True)

    #UNZIPPING THE EMBEDDING.
    unzip_vector(filename, vector_file)

    #REMOVING DOWNLOADED FILE.
    os.remove(filename)


class WordVecVectorizer(object):
    def __init__(self, vectorfile):
        try:
            self.wordvector = KeyedVectors.load_word2vec_format(vectorfile, limit=100000)
            print('embedding loaded.')
        except:
            print('downloading embeding files...')
            download_embeddings(vectorfile)
            self.wordvector = KeyedVectors.load_word2vec_format(vectorfile, limit=100000)
            print('embedding loaded.')
        self.dim = 300

    def transform(self, X):
        mean_vector = np.array([np.mean([self.wordvector[word] for word in sentence if word in self.wordvector] 
                               or [np.zeros(self.dim)], axis=0) for sentence in X])
                       
        return mean_vector