import tensorflow as tf
import tensorflow.keras as keras
from static_variables import resolve_static


def gram_matrix(input_tensor):
    """
    Compute the gram matrix on the last dimension of the input tensor

    Args:
        input_tensor (tf.Tensor): tensor of rank 4
    Return:
        gram_matrix (tf.Tensor): tensor of rank 3
    """
    result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
    input_shape = tf.shape(input_tensor)
    num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
    return result / num_locations


@resolve_static(static_variables={'mse': keras.losses.MeanSquaredError()})
def content_loss(content_features, synthesized_features, weights):
    """
    Compute the weighted mean squared error between two dictionaries of
    corresponding tensors

    Args:
        content_features (dict): maps layer name to extracted features
        synthesized_features (dict): maps layer name to extracted features
        weights (dict): maps layer name to corresponding loss weight
    Return:
        loss_value (tf.float32): the loss value
    """
    loss_value = 0.0
    for name, features in content_features.items():
        loss_value += weights[name] * mse(features, synthesized_features[name])

    return loss_value


@resolve_static(static_variables={'mse': keras.losses.MeanSquaredError()})
def style_loss(style_gram_matrices, synthesized_features, weights):
    """
    Compute the weighted mean squared error between two dictionaries of
    gram matrices from corresponding tensors

    Args:
        style_gram_matrices (dict): maps layer name to gram matrix
        synthesized_features (dict): maps layer name to extracted features
        weights (dict): maps layer name to corresponding loss weight
    Return:
        loss_value (tf.float32): the loss value
    """
    loss_value = 0.0
    for name, true_gm in style_gram_matrices.items():
        gm = gram_matrix(synthesized_features[name])
        loss_value += weights[name] * mse(true_gm, gm)

    return loss_value
