import logging
import numpy as np
from typing import List
from torch import Tensor

from determined.pytorch import MetricReducer


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=level,
    )


def expand_like(arrays: List[np.ndarray], fill=-100) -> np.ndarray:
    full_shape = list(arrays[0].shape)
    if len(full_shape) == 1:
        return np.concatenate(arrays)
    full_shape[0] = sum([a.shape[0] for a in arrays])
    full_shape[1] = max([a.shape[1] for a in arrays])
    result = np.full(full_shape, fill)
    row_offset = 0
    for a in arrays:
        result[row_offset : row_offset + a.shape[0], : a.shape[1]] = a
        row_offset += a.shape[0]
    return result


def numpify(x) -> np.ndarray:
    if isinstance(x, np.ndarray):
        return x
    if isinstance(x, List):
        return np.array(x)
    if isinstance(x, Tensor):
        return x.cpu().numpy()
    raise NotImplementedError


class PredLabelFnReducer(MetricReducer):
    def __init__(self, fn):
        self.fn = fn
        self.reset()

    def reset(self):
        self.predictions = []
        self.labels = []

    def update(self, preds, labels):
        self.predictions.append(numpify(preds))
        self.labels.append(numpify(labels))

    def per_slot_reduce(self):
        return expand_like(self.predictions), expand_like(self.labels)

    def cross_slot_reduce(self, per_slot_metrics):
        predictions, labels = zip(*per_slot_metrics)
        return self.fn(expand_like(predictions), expand_like(labels))
