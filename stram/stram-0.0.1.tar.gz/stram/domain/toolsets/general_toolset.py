import datetime
import tensorflow as tf
from math import inf
from os.path import join
from collections import deque


def clip_0_255(image):
    """
    Clip image values to be in range [0..255]

    Args:
        image (tf.Tensor): an input image tensor
    Return:
        image (tf.Tensor): the image tensor with the values clipped
    """
    return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=255.0)


def create_optimizer(optimizer_name, optimizer_params, learning_rate_params):
    """
    Create an optimizer with polynomial decay

    Args:
        optimizer_name (str): the name of the optimizer (Adam, SGD, etc.)
        optimizer_params (dict): parameters for the optimizer
        learning_rate_params (dict): parameters for the learning rate scheduler
    Return:
        optimizer (tf.optimizers.Optimizer): the optimizer object
    """
    lr_scheduler = tf.optimizers.schedules.PolynomialDecay(**learning_rate_params)
    Optimizer = getattr(tf.optimizers, optimizer_name)

    return Optimizer(learning_rate=lr_scheduler, **optimizer_params)


def create_summary_writer(path):
    """
    Create a summary writer for monitoring loss functions and image styling progress
    It should only be used for debugging purposes (not in production)

    Args:
        path (str): the location where the summary folder will be created
    Return:
        summary_writer (tf.summary.SummaryWriter): the summary writer object
    """
    summary_folder = join(path, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    return tf.summary.create_file_writer(summary_folder)


def variation_loss(image):
    """
    Loss value for the pixel variation computed by averaging the absolute differences
    between all pairs of neighbouring pixels

    Args:
        image (tf.Tensor): an input image tensor
    Return:
        loss_value (tf.float32): the loss value
    """
    image_area = tf.shape(image)[-2] * tf.shape(image)[-3]
    total_variation_loss = tf.image.total_variation(image)[0]

    return tf.cast(total_variation_loss, tf.float32) / tf.cast(image_area, tf.float32)


class EarlyStopper:
    """
    Tracks a metric over time and flags when its improvement stagnates according
    to some preconfigured properties like patience and delta

    Args:
        delta (float): minimum relative improvement expected over the history buffer;
                       if this improvement percentage is not attained, then STOP
        patience (int): size of the buffer that holds the history of values
    """

    def __init__(self, delta, patience):
        self.actual_delta = None
        self.expected_delta = delta

        self.min_value = inf
        self.patience = patience
        self.history = deque([], self.patience)

    def __call__(self, value):
        """
        Adds the value to the history buffer and informs the external caller if the
        training should stop

        Args:
            value (float): current metric value
        Return:
            stop (bool): True for "should stop", False for "should continue"
        """
        self.min_value = min(self.min_value, value)

        if len(self.history) < self.patience:
            self.history.appendleft(value)
            return False

        ancient_value = self.history.pop()
        self.actual_delta = (ancient_value - self.min_value) / ancient_value

        if self.expected_delta < self.actual_delta:
            self.history.appendleft(value)
            return False

        return True

    def deltas_info(self):
        """
        Return a message that displays the values for actual_delta and expected_delta

        Return
            message (str): displays the current values for deltas
        """
        return (
            f'expected_delta={self.expected_delta}; '
            + f'actual_delta={self.actual_delta:.10f}'
        )
