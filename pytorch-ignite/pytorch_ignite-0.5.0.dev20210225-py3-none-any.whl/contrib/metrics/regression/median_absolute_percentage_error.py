from typing import Callable

import torch

from ignite.contrib.metrics.regression._base import _BaseRegressionEpoch


def median_absolute_percentage_error_compute_fn(y_pred: torch.Tensor, y: torch.Tensor) -> float:
    e = torch.abs(y.view_as(y_pred) - y_pred) / torch.abs(y.view_as(y_pred))
    return 100.0 * torch.median(e).item()


class MedianAbsolutePercentageError(_BaseRegressionEpoch):
    r"""Calculates the Median Absolute Percentage Error.

    .. math::
        \text{MdAPE} = 100 \cdot \text{MD}_{j=1,n} \left( \frac{|A_j - P_j|}{|A_j|} \right)

    where :math:`A_j` is the ground truth and :math:`P_j` is the predicted value.

    More details can be found in `Botchkarev 2018`__.

    - ``update`` must receive output of the form ``(y_pred, y)`` or ``{'y_pred': y_pred, 'y': y}``.
    - `y` and `y_pred` must be of same shape `(N, )` or `(N, 1)` and of type `float32`.

    .. warning::

        Current implementation stores all input data (output and target) in as tensors before computing a metric.
        This can potentially lead to a memory error if the input data is larger than available RAM.


    __ https://arxiv.org/abs/1809.03006

    """

    def __init__(self, output_transform: Callable = lambda x: x):
        super(MedianAbsolutePercentageError, self).__init__(
            median_absolute_percentage_error_compute_fn, output_transform
        )
