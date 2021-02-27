import logging

from stram.domain.style_product import StyleProduct
from stram.services.method_factory import create_method
from stram.utils.exceptions import InvalidOrderException

logger = logging.getLogger(__name__)


def execute_orders(content_image, style_image, orders):
    """
    Delegate the execution of styling orders by creating the appropriate method
    objects and running the processes

    Args:
        content_image (np.ndarray): the image to apply the style on
        style_image (np.ndarray): the image whose style to apply
        orders (dict): maps styling config hash to styling config
    Return:
        style_products (Iterator): a generator of StyleProduct objects
    """
    for styling_hash, styling_config in orders.items():
        try:
            method = create_method(styling_config.method)
            method.set_up(content_image, style_image, styling_config)
            method.process(styling_config)
            synthesized_image = method.get_synthesized_image()

            yield StyleProduct(styling_hash, styling_config, synthesized_image)

        except InvalidOrderException as ioe:
            logger.error(f'{ioe}. Order is skipped')
