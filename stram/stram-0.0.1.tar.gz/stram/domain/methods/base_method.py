from abc import ABC, abstractmethod


class BaseMethod(ABC):
    @abstractmethod
    def set_up(self, content_image, style_image, config):
        """
        Set up the method by performing all steps that must be done only for
        initialization

        Args:
            content_image (np.ndarray): the image to apply the style on (uint8)
            style_image (np.ndarray): the image whose style to apply (uint8)
            config (Bunch): configurations for the styling process
        """
        pass

    @abstractmethod
    def process(self, config):
        """
        Run the process of applying the style to the content image

        Args:
            config (Bunch): configurations for the styling process
        """
        pass

    @abstractmethod
    def get_synthesized_image(self):
        """
        Return the synthesized image

        Return:
            synthesized_image (np.ndarray): the resulting image (uint8)
        """
        pass
