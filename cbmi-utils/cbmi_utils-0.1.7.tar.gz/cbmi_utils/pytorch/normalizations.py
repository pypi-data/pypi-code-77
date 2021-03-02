from typing import Tuple

from torch import batch_norm, moments, nn, ones, zeros


class GANAdaptiveInstanceNorm(nn.Module):
    """
    Base class, should not be called directly.

    Custom Adaptive Instance Normalization from https://github.com/AdalbertoCq/Pathology-GAN/blob/master/models/generative/normalization.py (conditional_batch_norm)

    GAN related AdaIN Paper: https://arxiv.org/pdf/1812.04948.pdf
    """

    def __init__(self, inputs, c, spectral: bool = False):
        super(GANAdaptiveInstanceNorm, self).__init__()

        def block_dense(in_feat, out_feat, spectral=True, activation=True):
            # Linear + Spectral Norm (optional) + Relu (optional)
            if spectral:
                layers = [nn.utils.spectral_norm(
                    nn.Linear(in_feat, out_feat), n_power_iterations=1, eps=1e-12)]
            else:
                layers = [nn.Linear(in_feat, out_feat)]

            if activation:
                layers.append(nn.ReLU(inplace=True))

            return layers

        if len(inputs) == 3:
            channels, _, _ = inputs
        else:
            channels = inputs

        self.decay = 0.9
        self.epsilon = 1e-5

        self.test_mean = zeros([channels], requires_grad=False)
        self.test_variance = ones([channels], requires_grad=False)

        # MLP for gamma, and beta
        # TODO handle c, will throw error
        inter_dim = int((channels+c.shape.as_list()[-1])/2)

        self.net = nn.Sequential(
            *block_dense(in_feat=c, out_feat=inter_dim, spectral=spectral, activation=True))

        self.gamma = nn.Sequential(
            *block_dense(in_feat=inter_dim, out_feat=channels, spectral=spectral, activation=True))

        self.beta = nn.Sequential(
            *block_dense(in_feat=inter_dim, out_feat=channels, spectral=spectral, activation=False))

        self.init_weights()

    def forward(self, x):
        # TODO check if split is required at all
        # if  len(x) == 4:
        # 	self.gamma = tf.expand_dims(tf.expand_dims(self.gamma, 1), 1)
        # 	self.beta = tf.expand_dims(tf.expand_dims(self.beta, 1), 1)

        # TODO check if split is handled correctly
        if len(x) == 4:
            batch_mean, batch_variance = moments(
                x, axes=[1, 2], keep_dims=True)
        else:
            batch_mean, batch_variance = moments(x, axes=[1], keep_dims=True)

        batch_norm_output = batch_norm(
            x, batch_mean, batch_variance, self.beta, self.gamma, self.epsilon)

        return batch_norm_output

    def init_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                nn.init.orthogonal_(module.weight, gain=1e-4)
                nn.init.constant_(module.bias, 0)


class GANAdaptiveInstanceNorm1d(GANAdaptiveInstanceNorm):
    """
    Custom Adaptive Instance Normalization 1d Wrapper
    """
    # TODO specify type of c

    def __init__(self, inputs: int, c, spectral: bool = False):
        super(GANAdaptiveInstanceNorm1d, self).__init__(
            inputs=inputs, c=c, spectral=spectral)


class GANAdaptiveInstanceNorm2d(GANAdaptiveInstanceNorm):
    """
    Custom Adaptive Instance Normalization 2d Wrapper
    """
    # TODO specify type of c

    def __init__(self, inputs: Tuple[int, int, int], c, spectral: bool = False):
        super(GANAdaptiveInstanceNorm2d, self).__init__(
            inputs=inputs, c=c, spectral=spectral)

