import argparse
import pickle
import json
import os

from core.data import load_data
from core.plots import plot_confusion_matrix
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix


def evaluate(args, model, data, labels):
    
    predictions = model.predict(data)
    
    #COMPUTING METRICS
    accuracy = accuracy_score(labels, predictions) * 100
    f1 = f1_score(labels, predictions, average='macro')*100
    cfm = confusion_matrix(labels, predictions)

    print('Model Performance: {}'.format(args.model))
    print('Accuracy = {:0.2f}%.'.format(accuracy))
    print('F1-Score = {:0.2f}%.'.format(f1))
    
    # SAVING METRICS AND PLOTTING CONFUSION MATRIX
    exp_path = './experiments/{}'.format(args.model)
    os.makedirs(exp_path, exist_ok=True)
    with open('{}/test_metrics.json'.format(exp_path), 'w') as json_file:
        json.dump({'F1 Macro': f1,
                   'Accuracy': accuracy}, json_file)
    plot_confusion_matrix(exp_path, cfm, model.classes_)

def train(args):
    x_train, x_test, y_train, y_test = load_data(args)
    
    #LOAD MODELS' HYPERPARAMETERS
    exp_path = './experiments/{}'.format(args.model)
    with open(exp_path+'/conf.json') as file:
        hyperparams = json.load(file)
     
    if args.model=='rf':
        from sklearn.ensemble import RandomForestClassifier
    elif args.model=='balanced-rf':
        from imblearn.ensemble import BalancedRandomForestClassifier as RandomForestClassifier
        
    rf = RandomForestClassifier(criterion=hyperparams['criterion'],
                                n_estimators=hyperparams['n_estimators'],
                                max_depth=hyperparams['max_depth'],
                                max_features=hyperparams['max_features'])
    rf.fit(x_train, y_train)
    evaluate(args, rf, x_test, y_test)
    pickle.dump(rf, open('{}/trained_model.sav'.format(exp_path), 'wb'))
    return rf
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # TRAINING PAREMETERS
    parser.add_argument('--data_path', default='./data/records/all_contrib', type=str,
                        help='Dataset folder containing the records files')
    parser.add_argument('--reduced_classes', default=True, type=bool,
                        help='If the number of classes will be 20 or 13.')
    parser.add_argument('--create_embedding', default=False, type=bool,
                        help='If the embeddings need to be computed')
    parser.add_argument('--model', default='balanced-rf', type=str, choices=['rf', 'balanced-rf'],
                        help='Model to be used for the experiments.')
    parser.add_argument('--split', default=0, type=int,
                        help='split to be used to report metrics.')

    args = parser.parse_args()

    train(args)
