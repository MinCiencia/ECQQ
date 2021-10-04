import tensorflow as tf 
from tensorflow.keras.losses import SparseCategoricalCrossentropy


class MaskedCrossEntropy(tf.keras.losses.Loss):
    def __init__(self, name="CrossEntropy"):
        super(MaskedCrossEntropy, self).__init__(name=name)
        self.loss_object = SparseCategoricalCrossentropy(from_logits=True)

    def call(self, y_true, y_pred, sample_weight=None):
        true = tf.squeeze(tf.slice(y_true, [0,0,0], [-1,-1,1]))
        mask = tf.slice(y_true, [0,0,1], [-1,-1,1])

        loss_ = self.loss_object(true, y_pred)
        mask = tf.cast(mask, dtype=loss_.dtype)
        loss_ *= mask
        return tf.reduce_sum(loss_)/tf.reduce_sum(mask)

