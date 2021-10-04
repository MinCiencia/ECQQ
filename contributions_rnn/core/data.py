import tensorflow as tf
import pandas as pd
import numpy as np
import os

def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(list_of_floats):  # float32
    return tf.train.Feature(float_list=tf.train.FloatList(value=list_of_floats))

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def label_frame(frame, labels):
    label_list = []

    for _, c in frame.iterrows():
        m1 = labels[labels['text'] == c['text']]
        m2 = labels[labels['tokens'] == c['tokens']]
        m = pd.concat([m1,m2]).drop_duplicates()

        y = m[m['label']!='NR']['label']
        if y.shape[0] != 0:
            label_list.append(y.values[0])
        else:
            label_list.append('')

    frame['label'] = label_list
    return frame

def train_val_test(frame, outdir, train_ptg, val_ptg, save=False):
    train_sets, val_sets, test_sets = [], [], []
    category_samples = frame.groupby('label')
    for label, subframe in category_samples:
        subframe = subframe.sample(frac=1)

        n_train = int(train_ptg*subframe.shape[0])
        n_val = int(val_ptg/2*subframe.shape[0])

        train = subframe.iloc[:n_train]
        val   = subframe.iloc[n_train:n_train+n_val]
        test  = subframe.iloc[n_train+n_val:]

        train_sets.append(train)
        val_sets.append(val)
        test_sets.append(test)

    train = pd.concat(train_sets)
    train['subset'] = ['train']*train.shape[0]
    val   = pd.concat(val_sets)
    val['subset'] = ['val']*val.shape[0]
    test  = pd.concat(test_sets)
    test['subset'] = ['test']*test.shape[0]

    training_set = pd.concat([train, val, test])
    if save:
        training_set.to_csv(os.path.join(outdir, 'samples.csv'), index=False)
    return training_set

def write_records(frame, label, folder, embedding):
    file = os.path.join(folder, '{}.record'.format(label))
    with tf.io.TFRecordWriter(file) as writer:
        for _, row in frame.iterrows():
            # Text encoding
            encoding = []
            for word in row['text'].split():
                try:
                    encoding.append(embedding[word])
                except:
                    continue
                    
            encoding = np.array(encoding)
            if encoding.shape[0] > 0:
                dict_sequence = dict()
                for dim in range(encoding.shape[-1]):
                    seqfeat = _float_feature(encoding[:, dim])
                    seqfeat = tf.train.FeatureList(feature = [seqfeat])
                    dict_sequence['dim_tok_{}'.format(dim)] = seqfeat
                element_lists = tf.train.FeatureLists(feature_list=dict_sequence)

                dict_features={
                'text': _bytes_feature(str(row['text']).encode()),
                'category': _bytes_feature(str(row['label']).encode()),
                'label': _int64_feature(label),
                'id': _int64_feature(int(row['id'])),
                'length': _int64_feature(int(encoding.shape[0]))
                }
                element_context = tf.train.Features(feature = dict_features)
                ex = tf.train.SequenceExample(context = element_context,
                                              feature_lists= element_lists)
                writer.write(ex.SerializeToString())

def create_records(frame, embedding, outdir, train_ptg=0.5, val_ptg=0.5):
    os.makedirs(outdir, exist_ok=True)
    subset_frame = train_val_test(frame, outdir, train_ptg, val_ptg, save=True)
    for subset in ['train', 'val', 'test']:
        partial = subset_frame[subset_frame['subset'] == subset]
        classes = partial.groupby('label')

        for k, (_, samples) in enumerate(classes):
            folder = os.path.join(outdir, subset)
            os.makedirs(folder, exist_ok=True)
            write_records(samples, k, folder, embedding)

def create_prediction_record(frame, embedding, outdir):
    folder = os.path.join(outdir, 'prediction')
    os.makedirs(folder, exist_ok=True)
    write_records(frame, 0, folder, embedding)


def _parse(sample, n_cls):


    context_features = {'label': tf.io.FixedLenFeature([],dtype=tf.int64),
                        'length': tf.io.FixedLenFeature([],dtype=tf.int64),
                        'id': tf.io.FixedLenFeature([],dtype=tf.int64),
                        'category': tf.io.FixedLenFeature([], dtype=tf.string),
                        'text': tf.io.FixedLenFeature([], dtype=tf.string)}

    sequence_features = dict()
    for i in range(300):
        sequence_features['dim_tok_{}'.format(i)] = tf.io.VarLenFeature(dtype=tf.float32)

    context, sequence = tf.io.parse_single_sequence_example(
                            serialized=sample,
                            context_features=context_features,
                            sequence_features=sequence_features
                            )

    input_dict = dict()
    input_dict['id']       = tf.cast(context['id'], tf.int32)
    input_dict['category'] = tf.cast(context['category'], tf.string)
    input_dict['text']     = tf.cast(context['text'], tf.string)
    input_dict['length']   = tf.cast(context['length'], tf.int32)
    input_dict['label']    = tf.one_hot(tf.cast(context['label'], tf.int32), n_cls)

    casted_inp_parameters = []
    for i in range(300):
        seq_dim = sequence['dim_tok_{}'.format(i)]
        seq_dim = tf.sparse.to_dense(seq_dim)
        seq_dim = tf.cast(seq_dim, tf.float32)
        casted_inp_parameters.append(seq_dim)

    input_dict['input'] = tf.stack(casted_inp_parameters, axis=2)[0]

    return input_dict

def load_records(source, batch_size, return_cls=False, return_all=False):

    if return_all:
        datasets = [os.path.join(source, x) for x in os.listdir(source)]
        n_cls = len(datasets)
        dataset = tf.data.TFRecordDataset(datasets)
        dataset = dataset.map(lambda x: _parse(x, n_cls), num_parallel_calls=8)
    else:
        datasets = [tf.data.TFRecordDataset(os.path.join(source, x)) for x in os.listdir(source)]
        n_cls = len(datasets)
        datasets = [
            dataset.map(
                lambda x: _parse(x, n_cls), num_parallel_calls=8) for dataset in datasets
        ]
        datasets = [dataset.repeat() for dataset in datasets]
        datasets = [dataset.shuffle(5000, reshuffle_each_iteration=True) for dataset in datasets]
        dataset  = tf.data.experimental.sample_from_datasets(datasets)

    dataset  = dataset.padded_batch(batch_size).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

    if return_cls:
        return dataset, n_cls
    return dataset
