import tensorflow as tf

from tensorflow.keras.layers import (Input,
                                     Layer,
                                     LSTMCell,
                                     StackedRNNCells,
                                     RNN,
                                     Dense)
from tensorflow_addons.rnn import LayerNormLSTMCell
from tensorflow.keras import Model

from core.masking import create_mask


class RNNModel(Model):
    def __init__(self, num_units, num_layers, num_cls, dropout, **kwargs):
        super(RNNModel, self).__init__(**kwargs)

        rnn_cells = [LayerNormLSTMCell(num_units, dropout=dropout) for _ in range(num_layers)]
        stacked_lstm = StackedRNNCells(rnn_cells)
        self.lstm_layer = RNN(stacked_lstm)
        self.dense = Dense(num_cls, activation='softmax')

    def model(self, batch_size):
        serie_1  = Input(shape=(100, 300), batch_size=batch_size, name='Serie1')
        serie_2  = Input(shape=(100, 1), batch_size=batch_size, name='Mask')
        data = (serie_1, serie_2)
        return Model(inputs=data, outputs=self.call(data))

    def call(self, inputs, training=False):
        x, mask = inputs
        x = self.lstm_layer(x, mask=mask, training=training)
        x = self.dense(x)
        return x

    def train_step(self, data):
        mask = create_mask(data['input'], data['length'])
        with tf.GradientTape() as tape:
            y_pred = self((data['input'], mask), training=True)
            t_loss = self.compiled_loss(data['label'], y_pred)

        gradients = tape.gradient(t_loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.trainable_variables))
        self.compiled_metrics.update_state(data['label'], y_pred)
        return {m.name: m.result() for m in self.metrics}

    def test_step(self, data):
        mask = create_mask(data['input'], data['length'])
        with tf.GradientTape() as tape:
            y_pred = self((data['input'], mask), training=False)
            t_loss = self.compiled_loss(data['label'], y_pred)

        self.compiled_metrics.update_state(data['label'], y_pred)
        return {m.name: m.result() for m in self.metrics}

    def predict_step(self, data):
        mask = create_mask(data['input'], data['length'])
        y_pred = self((data['input'], mask), training=False)

        if 'label' in data.keys():
            return tf.argmax(y_pred, 1),  tf.argmax(data['label'], 1), data['text']
        else:
            return tf.argmax(y_pred, 1),  data['text']

    def predict_proba(self, data):

        probas = []
        trues = []
        texts = []
        for batch in data:
            mask = create_mask(batch['input'], batch['length'])
            y_pred = self((batch['input'], mask), training=False)
            probas.append(y_pred)
            trues.append(tf.argmax(batch['label'], 1))
            texts.append(batch['text'])
        return tf.concat(probas, 0), tf.concat(trues, 0), tf.concat(texts, 0)

    def get_latent(self, data):

        states = []
        trues = []
        texts = []
        for batch in data:
            mask = create_mask(batch['input'], batch['length'])

            h = self.lstm_layer(batch['input'], mask=mask, training=False)
            states.append(h)
            trues.append(tf.argmax(batch['label'], 1))
            texts.append(batch['text'])

        return tf.concat(states, 0), tf.concat(trues, 0), tf.concat(texts, 0)
