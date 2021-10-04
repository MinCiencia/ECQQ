import tensorflow as tf 

def create_mask(tensor, lengths):
    ''' Create mask given a tensor and true length '''
    lengths_transposed = tf.expand_dims(lengths, 1)
    rangex = tf.range(0, tf.shape(tensor)[1], 1)
    range_row = tf.expand_dims(rangex, 0)
    # Use the logical operations to create a mask
    mask = tf.less(range_row, lengths_transposed)
    return mask