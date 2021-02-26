import pytest
import torch

from metlibvi.targets import Gaussian


@pytest.fixture(scope="session")
def get_gaussian_target():
    loc = torch.tensor([10., -10.])
    cov = torch.eye(2)
    target = Gaussian(loc=loc, covariance_matrix=cov)
    return target
