import cv2
import logging
import numpy as np
import tensorflow as tf
from os.path import join
from decouple import config as env_config
from scipy.sparse import identity, csc_matrix, linalg

from stram.utils.json_processing import dict2namespace
from stram.domain.methods.base_method import BaseMethod
from stram.domain.toolsets.general_toolset import create_summary_writer
from stram.domain.toolsets.yijun_toolset import (
    get_num_levels,
    whitening_transform,
    colouring_transform,
    compute_input_paddings,
    matting_affinity_laplacian,
)

logger = logging.getLogger(__name__)
tf.config.optimizer.set_jit(env_config('TF_JIT', default=False, cast=bool))


class YijunMethod(BaseMethod):
    """
    Source: https://arxiv.org/abs/1802.06474
    Title: A Closed-form Solution to Photorealistic Image Stylization
    Authors: Yijun Li, Ming-Yu Liu, Xueting Li, Ming-Hsuan Yang, Jan Kautz

    The algorithm works in 2 steps. The first, called photorealistic stylization, embbeds
    the content and style images using intermediary layers VGG19 encoders and attempts to
    make the content feature correlations match the style feature correlations by appying
    the whitening-colouring transform (WCT). The resulted feature map is then decoded
    back to RGB space using some pretrained VGG19 layer decoders. The second step, called
    photorealistic smoothing, takes the result from step 1 and the original content image
    and tries to ensure consistency between the stylizations of semantically similar
    regions (using the content image as reference). There are two options for this step,
    the precise optimization using the matting affinity laplacian and the faster guided
    image filtering.
    """

    ARTIFACTS_PATH = env_config('ARTIFACTS_PATH', default='artifacts')
    SMOOTHING_TOOLS = ('off', 'matting_affinity', 'guided_filter')

    def __str__(self):
        return 'yijun'

    def set_up(self, content_image, style_image, config):
        assert (
            config.smoothing_tool in YijunMethod.SMOOTHING_TOOLS
        ), 'Invalid smoothing method. It must be one of "{}", "{}" or "{}"'.format(
            *YijunMethod.SMOOTHING_TOOLS
        )

        content_image_reshaped = tf.expand_dims(content_image, axis=0)
        self.content_image_tf = tf.cast(content_image_reshaped, tf.float32)
        self.content_image_np = content_image

        style_image_reshaped = tf.expand_dims(style_image, axis=0)
        self.style_image_tf = tf.cast(style_image_reshaped, tf.float32)

        if env_config('DEBUG', default=False, cast=bool):
            self.step = 0
            self.summary_writer = create_summary_writer(env_config('SUMMARY_PATH'))
            with self.summary_writer.as_default():
                tf.summary.image('content', content_image_reshaped, step=0)
                tf.summary.image('style', style_image_reshaped, step=0)

    def process(self, config):
        logger.info('<Yijun Method>')
        logger.info('\tLoading encoder-decoders...')
        self._step_1_load_encoder_decoder_pairs(config.style_bottom_layer)

        logger.info('\tRunning stylization...')
        self._step_2_run_multilevel_stylization(config.style_strength)

        if config.smoothing_tool != 'off':
            logger.info('\tRunning smoothing...')
            smoothing_config = dict2namespace(config.smoothing)

            if config.smoothing_tool == 'matting_affinity':
                self._step_3_run_matting_affinity_smoothing(smoothing_config)
            else:
                self._step_3_run_guided_filter_smoothing(smoothing_config)

        logger.info('\tComplete')

    def get_synthesized_image(self):
        return np.round(self.synthesized_image).astype(np.uint8)

    def _step_1_load_encoder_decoder_pairs(self, style_bottom_layer):
        """
        Load the VGG19 encoders and decoders based on how many levels are involved in
        the stylization process

        Args:
            style_bottom_layer (str): name of the lowest level VGG19 encoder needed;
                                      encoders and decoders from all higher levels will
                                      also be loaded
        """
        layers = [f'block{x}_conv2' for x in range(1, 6)]
        if style_bottom_layer not in layers:
            raise ValueError(f'{style_bottom_layer} is not available for autoencoders')

        self.encoder = {}
        self.decoder = {}
        self.styling_layers = []

        for layer_name in layers:
            models_path = join(YijunMethod.ARTIFACTS_PATH, f'vgg19_{layer_name}')
            self.encoder[layer_name] = tf.saved_model.load(join(models_path, 'encoder'))
            self.decoder[layer_name] = tf.saved_model.load(join(models_path, 'decoder'))
            self.styling_layers = [layer_name] + self.styling_layers

            if layer_name == style_bottom_layer:
                break

    def _step_2_run_multilevel_stylization(self, alpha):
        """
        Run multilevel stylization upwards starting from the bottom encoder-decoder pair
        This implementation follows the algorithm from: https://arxiv.org/abs/1705.08086
        and uses the same variable names

        Args:
            alpha (float): value between 0 and 1 represeting the strength of stylization
        """
        assert 0 <= alpha <= 1.0, 'Styling strength (alpha) must be in range [0..1]'
        synthesized = self.content_image_tf
        image_shape = tf.shape(synthesized).numpy()

        for layer_name in self.styling_layers:
            # pad the input image to preserve shape consistency when upsampling
            num_levels = get_num_levels(layer_name)
            paddings = compute_input_paddings(image_shape, num_levels)
            synthetic_tensor = tf.pad(synthesized, paddings, 'REFLECT')

            # obtain the encodings of both content and style images
            fc_encoded = self.encoder[layer_name](synthetic_tensor)
            fs_encoded = self.encoder[layer_name](self.style_image_tf)
            if isinstance(fc_encoded, list):
                fc_4d, *pooling_argmaxes = fc_encoded
                fs_4d = fs_encoded[0]
            else:
                fc_4d, pooling_argmaxes = fc_encoded, []
                fs_4d = fs_encoded

            # flatten feature vectors
            fc_3d = fc_4d[0]
            fs_3d = fs_4d[0]
            fc_3d_shape = tf.shape(fc_3d).numpy()
            fs_3d_shape = tf.shape(fs_3d).numpy()
            fc = tf.reshape(fc_3d, (fc_3d_shape[0] * fc_3d_shape[1], fc_3d_shape[2]))
            fs = tf.reshape(fs_3d, (fs_3d_shape[0] * fs_3d_shape[1], fs_3d_shape[2]))

            # apply the WCT transform
            fc_hat = whitening_transform(fc)
            fcs = colouring_transform(fc_hat, fs)
            fcs_3d = tf.reshape(fcs, fc_3d_shape)

            # blend according to the syling strength
            fcs_hat_3d = alpha * fcs_3d + (1 - alpha) * fc_3d

            # decode the image back to RGB space
            fcs_hat_4d = tf.expand_dims(fcs_hat_3d, axis=0)
            if len(pooling_argmaxes) > 0:
                decoder_inputs = [fcs_hat_4d] + pooling_argmaxes
            else:
                decoder_inputs = fcs_hat_4d

            synthetic_tensor = self.decoder[layer_name](decoder_inputs)
            synthesized = tf.image.crop_to_bounding_box(
                image=synthetic_tensor,
                offset_height=paddings[1][0],
                offset_width=paddings[2][0],
                target_height=image_shape[1],
                target_width=image_shape[2],
            )

            if env_config('DEBUG', default=False, cast=bool):
                with self.summary_writer.as_default():
                    tb_image = tf.cast(synthesized, tf.uint8)
                    tf.summary.image('synthesized', tb_image, step=self.step)
                    self.step += 1

        self.synthesized_image = synthesized.numpy()[0]

    def _step_3_run_matting_affinity_smoothing(self, smoothing_config):
        """
        Apply smoothing to encourage consistent stylization within semantically similar
        regions. This implementation follows the algorithm from:
        https://arxiv.org/abs/1802.06474 and uses the same variable names

        Args:
            smoothing_config (Bunch): configurations for the smoothing process
        """
        # pad image to avoid creating artifacts at the edges
        pad = smoothing_config.window_radius + 1
        paddings = [[pad, pad], [pad, pad], [0, 0]]

        synthesized_pad = np.pad(self.synthesized_image, pad_width=paddings, mode='edge')
        content_image_pad = np.pad(self.content_image_np, pad_width=paddings, mode='edge')

        height, width, channels = synthesized_pad.shape
        Y = np.reshape(synthesized_pad, (height * width, channels)) / 255.0

        # compute the affinity matrix W
        W = matting_affinity_laplacian(
            content_image_pad / 255.0,
            smoothing_config.epsilon,
            smoothing_config.window_radius,
        )
        W = W.tocsc()

        # compute the degree matrix D and D_hat = D ^ (-1 / 2)
        D = W.sum(axis=0)
        indices = np.arange(0, height * width)
        D_hat = np.sqrt(np.power(D, -1)).A.squeeze()
        D_hat = csc_matrix((D_hat, (indices, indices)))

        # compute the normalized laplacian matrix S
        S = D_hat.dot(W).dot(D_hat)

        # compute the final smoothed image
        alpha = 1 / (1 + smoothing_config.lambda_)
        I = identity(height * width)

        A = (I - alpha * S).tocsc()
        solver = linalg.factorized(A)

        V = np.zeros((height * width, channels))
        for c in range(channels):
            V[:, c] = solver(Y[:, c])

        R = (1 - alpha) * V
        R = R.reshape(height, width, channels)[pad:-pad, pad:-pad]
        self.synthesized_image = np.clip(R * 255, 0, 255)

        if env_config('DEBUG', default=False, cast=bool):
            with self.summary_writer.as_default():
                tb_image = tf.cast(self.synthesized_image, tf.uint8)
                tb_image = tf.expand_dims(tb_image, axis=0)
                tf.summary.image('synthesized', tb_image, step=self.step)

    def _step_3_run_guided_filter_smoothing(self, smoothing_config):
        """
        Apply smoothing to encourage consistent stylization within semantically similar
        regions. It uses the guided image filtering described here:
        http://kaiminghe.com/eccv10/

        Args:
            smoothing_config (Bunch): configurations for the smoothing process
        """
        self.synthesized_image = cv2.ximgproc.guidedFilter(
            self.content_image_np,
            self.get_synthesized_image(),
            smoothing_config.window_radius,
            smoothing_config.epsilon,
        )
