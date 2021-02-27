import logging
import numpy as np
import tensorflow as tf
from decouple import config as env_config
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg19 import VGG19, preprocess_input

from stram.utils.json_processing import dict2namespace
from stram.domain.methods.base_method import BaseMethod
from stram.domain.toolsets.gatys_toolset import gram_matrix, style_loss, content_loss
from stram.domain.toolsets.general_toolset import (
    clip_0_255,
    variation_loss,
    create_optimizer,
    create_summary_writer,
    EarlyStopper,
)

logger = logging.getLogger(__name__)
tf.config.optimizer.set_jit(env_config('TF_JIT', default=False, cast=bool))


class GatysMethod(BaseMethod):
    """
    Source: https://arxiv.org/abs/1508.06576
    Title: A Neural Algorithm of Artistic Style
    Authors: Leon A. Gatys, Alexander S. Ecker, Matthias Bethge

    The algorithm works by using a well pretrained classification model (VGG19) as a
    feature extractor. Content is kept by directly minimizing the loss between the
    features from the content image and the features from the synthesized image from
    various levels of VGG19. Style is enforced by mathcing statistics between the
    features of the style image and the features of the synthesized image. These
    statistics are obtained by computing the gram matrix on the channel dimension.
    """

    def __str__(self):
        return 'gatys'

    def set_up(self, content_image, style_image, config):
        content_image_reshaped = tf.expand_dims(content_image, axis=0)
        content_image_casted = tf.cast(content_image_reshaped, tf.float32)
        self.content_image_input = preprocess_input(content_image_casted)

        style_image_reshaped = tf.expand_dims(style_image, axis=0)
        style_image_casted = tf.cast(style_image_reshaped, tf.float32)
        self.style_image_input = preprocess_input(style_image_casted)

        self.synthesized_image = tf.Variable(content_image_casted, trainable=True)

        if env_config('DEBUG', default=False, cast=bool):
            self.summary_writer = create_summary_writer(env_config('SUMMARY_PATH'))
            with self.summary_writer.as_default():
                tf.summary.image('content', content_image_reshaped, step=0)
                tf.summary.image('style', style_image_reshaped, step=0)

    def process(self, config):
        logger.info('<Gatys Method>')
        content_layers_names = list(config.content_layers.keys())
        style_layers_names = list(config.style_layers.keys())
        all_layers = set(content_layers_names + style_layers_names)

        self._step_1_create_feature_extractor(all_layers)
        self._step_2_precompute_features(config)

        if env_config('DEBUG', default=False, cast=bool):
            self._train_debug_mode(config)
        else:
            self._train_release_mode(config)

    def get_synthesized_image(self):
        return np.round(self.synthesized_image.numpy()[0]).astype(np.uint8)

    def _train_release_mode(self, config):
        """
        Run the optimization loop in release mode (production environment)

        Args:
            config (Bunch): configurations for the styling process
        """
        optimizer = create_optimizer(
            config.optimizer, config.optimizer_params, config.learning_rate_params
        )
        stopper_config = dict2namespace(config.early_stopping)
        if stopper_config.enabled:
            stopper = EarlyStopper(stopper_config.delta, stopper_config.patience)

        for i in range(config.max_iterations):
            (
                content_loss_value,
                style_loss_value,
                variation_loss_value,
                total_loss,
            ) = self._train_step(config, optimizer)

            if stopper_config.enabled and stopper(total_loss):
                logger.info(f'Stopped early: iteration {i}; {stopper.deltas_info()}')
                break

    def _train_debug_mode(self, config):
        """
        Run the optimization loop in debug mode where summaries are also stored

        Args:
            config (Bunch): configurations for the styling process
        """
        import tqdm

        optimizer = create_optimizer(
            config.optimizer, config.optimizer_params, config.learning_rate_params
        )
        stopper_config = dict2namespace(config.early_stopping)
        if stopper_config.enabled:
            stopper = EarlyStopper(stopper_config.delta, stopper_config.patience)

        with self.summary_writer.as_default():
            for i in tqdm.trange(config.max_iterations, desc='Progress'):
                (
                    content_loss_value,
                    style_loss_value,
                    variation_loss_value,
                    total_loss,
                ) = self._train_step(config, optimizer)

                tf.summary.scalar('content_loss', content_loss_value, step=i)
                tf.summary.scalar('style_loss', style_loss_value, step=i)
                tf.summary.scalar('variation_loss', variation_loss_value, step=i)
                tf.summary.scalar('total_loss', total_loss, step=i)

                if i % env_config('SUMMARY_FREQUENCY_IMAGES', cast=int) == 0:
                    tb_image = tf.cast(self.synthesized_image, tf.uint8)
                    tf.summary.image('synthesized', tb_image, step=i)

                if stopper_config.enabled:
                    if stopper.actual_delta is not None:
                        tf.summary.scalar('loss_delta', stopper.actual_delta, step=i)
                    if stopper(total_loss):
                        tb_image = tf.cast(self.synthesized_image, tf.uint8)
                        tf.summary.image('synthesized', tb_image, step=i)
                        logger.info(
                            f'Stopped early: iteration {i}; {stopper.deltas_info()}'
                        )
                        break

    @tf.function(autograph=env_config('AUTOGRAPH', default=True, cast=bool))
    def _train_step(self, config, optimizer):
        """
        Perform an iteration of optimization for the synthesized image

        Args:
            config (Bunch): configurations for the styling process
            optimizer (tf.optimizers.Optimizer): the optimizer object
        Return:
            content_loss_value (tf.float32): current content loss
            style_loss_value (tf.float32): current style loss
            variation_loss_value (tf.float32): current variation loss
            total_loss (tf.float32): current total loss
        """
        with tf.GradientTape() as tape:
            preprocessed_image = preprocess_input(self.synthesized_image)
            image_features = self.feature_extractor(preprocessed_image)

            image_features_for_content = {
                name: image_features[name] for name in config.content_layers.keys()
            }
            image_features_for_style = {
                name: image_features[name] for name in config.style_layers.keys()
            }

            content_loss_value = content_loss(
                self.content_features, image_features_for_content, config.content_layers
            )
            style_loss_value = style_loss(
                self.style_gram_matrices, image_features_for_style, config.style_layers
            )
            variation_loss_value = variation_loss(self.synthesized_image)

            total_loss = (
                config.content_loss_weight * content_loss_value
                + config.style_loss_weight * style_loss_value
                + config.variation_loss_weight * variation_loss_value
            )

        gradients = tape.gradient(total_loss, self.synthesized_image)
        optimizer.apply_gradients([(gradients, self.synthesized_image)])
        self.synthesized_image.assign(clip_0_255(self.synthesized_image))

        return content_loss_value, style_loss_value, variation_loss_value, total_loss

    def _step_1_create_feature_extractor(self, layers):
        """
        Perform step 1: Create an instance of VGG19 that's specialized for returning the
        intermediate represenations from the requested layers

        Args:
            layers (list): name of the VGG19 layers used for feature extraction
        """
        vgg = VGG19(include_top=False, weights='imagenet')
        vgg.trainable = False
        outputs = {name: vgg.get_layer(name).output for name in layers}

        self.feature_extractor = Model([vgg.input], outputs)
        self.feature_extractor.trainable = False

    def _step_2_precompute_features(self, config):
        """
        Perform step 2: Extract features from the original content and style images.
        Pre-compute gram matrices from the style image features

        Args:
            config (Bunch): configurations for the styling process
        """
        assert hasattr(self, 'feature_extractor'), 'Cannot perform step 2 before step 1'

        raw_content_features = self.feature_extractor(self.content_image_input)
        self.content_features = {
            name: raw_content_features[name] for name in config.content_layers.keys()
        }

        raw_style_features = self.feature_extractor(self.style_image_input)
        style_features = {
            name: raw_style_features[name] for name in config.style_layers.keys()
        }
        self.style_gram_matrices = {
            name: gram_matrix(features) for name, features in style_features.items()
        }
