import matplotlib.pyplot as plt
import multiprocessing as mp
import pandas as pd
import numpy as np
import os

from tensorboard.backend.event_processing import event_accumulator

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix

from joblib import Parallel, delayed


def plot_cm(y_true, y_pred, display_labels, ax):
    cm = confusion_matrix(y_true, y_pred, normalize='true')
    cm = np.round(cm, 2)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=display_labels)


    # # NOTE: Fill all variables here with default values of the plot_confusion_matrix
    disp = disp.plot(cmap='Blues', ax=ax, xticks_rotation=90)
    return ax

def get_metrics(path_logs):
    train_logs = [x for x in os.listdir(path_logs) if x.endswith('.v2')][0]
    path_train = os.path.join(path_logs, train_logs)

    ea = event_accumulator.EventAccumulator(path_train)
    ea.Reload()
    metrics = dict()
    for metric in ea.Tags()['scalars']:
        values, steps = [], []
        for t in ea.Scalars(metric):
            steps.append(t[1])
            values.append(t[2])
        metrics[metric] = {'steps':steps, 'values': values}

    return metrics

def fn(x):
    if x == ['nr']:
        x = 'NR'
    return x

def label_df(data, partial, n_jobs=None):

    n_jobs = mp.cpu_count() if n_jobs is None else n_jobs
    print('[INFO] Using {} cores'.format(n_jobs))

    def step(row, partial):
        r = partial[partial['text'] == row['text']]
        if r.shape[0] == 0:
            y_pred = 'NR'
        else:
            y_pred = r['pred'].values[0]

        return row['con_id'], row['text'], row['tokens'], row['label'], row['macro'], y_pred

    response = Parallel(n_jobs=n_jobs)(delayed(step)(row, partial) \
                        for k, row in data.iterrows())

    final = pd.DataFrame()
    final['con_id'] = [x[0] for x in response]
    final['text']   = [x[1] for x in response]
    final['tokens'] = [x[2] for x in response]
    final['label']  = [x[3] for x in response]
    final['ia90']   = [x[4] for x in response]
    final['rnn']    = [x[5] for x in response]

    # Sanity check
    final['tokens'] = final['tokens'].apply(lambda x: fn(x))
    final[final['tokens'] =='NR'] = final[final['tokens'] =='NR'].replace('Trabajo','NR')

    return final
