import cv2
import numpy as np


def load_image(image_path):
    """
    Load an RGB image from disk and check if it was loaded correctly

    Args:
        image_path (str): path to the image
    Return
        image (np.ndarray): 3-channeled image
    """
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    assert image is not None, f'Image {image_path} not found'
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def save_image(image_path, image):
    """
    Save an RGB image to disk

    Args:
        image_path (str): path to the file to save
        image (np.ndarray): 3-channeled image
    """
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(image_path, image)


def image2tensor(image):
    """
    Convert from image space to styling space by rescaling values

    Args:
        image (np.ndarray): image in uint8, range [0..255]
    Return:
        tensor (np.ndarray): tensor in float32, range [-1..1]
    """
    return image.astype(np.float32) / 127.5 - 1.0


def tensor2image(tensor):
    """
    Convert from styling space to image space by rescaling values

    Args:
        tensor (np.ndarray): tensor in float32, range [-1..1]
    Return:
        image (np.ndarray): image in uint8, range [0..255]
    """
    return ((tensor + 1.0) * 127.5).astype(np.uint8)
