import tensorflow as tf
import os 

from tensorflow.keras.callbacks import EarlyStopping, TensorBoard


def get_callbacks(basepath='./experiments/test'):
    os.makedirs(basepath, exist_ok=True)

    earlystopping = EarlyStopping(monitor="val_loss",
                                    patience=100,
                                    min_delta=1e-4,
                                    mode='min',
                                    restore_best_weights=True,
                                    verbose=1)

    tboard = TensorBoard(log_dir=basepath,
                         histogram_freq=1,
                         write_graph=True)

    checkpoint_path = os.path.join(basepath, 'train_model.h5')
    checkpoint = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                    monitor='val_Accuracy',
                                                    save_best_only=True,
                                                    verbose=0)
    return [tboard, earlystopping, checkpoint]