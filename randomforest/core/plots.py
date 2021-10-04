import matplotlib.pyplot as plt
import numpy as np
import itertools

def plot_confusion_matrix(path, cm, classes,
                          normalize=True,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = np.round((cm.astype('float') / cm.sum(axis=1)[:, np.newaxis])*100)

    fig, ax = plt.subplots(figsize=(20, 12))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90, fontsize = 10, color='k')
    plt.yticks(tick_marks, classes, fontsize = 10, color='k')

    fmt = '.1f' if normalize else 'd'
    
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, "%d"%  (cm[i, j]),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black",fontsize = 14)

    plt.tight_layout()
    plt.ylabel('True label',fontsize = 18, color='white')
    plt.xlabel('Predicted label',fontsize = 18, color='white')
    plt.title('Confusion Matrix', fontsize = 18, color='white')
    plt.savefig('{}/cm.png'.format(path))
    plt.show()

