import numpy as np
from os.path import join, isfile

from stram.utils.image_processing import (
    load_image,
    save_image,
    image2tensor,
    tensor2image,
)


def test_load_image():
    image_path = join('tests', 'data', 'style_image.jpg')
    image = load_image(image_path)

    image_patch = image[40:42, 40:42]
    expected_patch = np.asarray(
        [[[61, 0, 0], [64, 9, 6]], [[98, 38, 40], [79, 26, 32]]], dtype=np.uint8
    )

    assert np.allclose(image_patch, expected_patch, atol=0.5)


def test_save_and_load_image(tmpdir):
    image_dir = tmpdir.mkdir('test_saving')
    image_path = join(image_dir, 'image.png')
    image = np.random.randint(0, 255, size=(128, 128, 3), dtype=np.uint8)

    save_image(image_path, image)
    image_loaded = load_image(image_path)

    assert isfile(image_path)
    assert np.allclose(image, image_loaded, atol=0.5)


def test_image2tensor_conversion():
    image = np.asarray([[0, 16, 30], [71, 135, 255]], dtype=np.uint8)
    expected_tensor = np.asarray(
        [[-1.0, -0.8745098, -0.7647059], [-0.44313723, 0.05882359, 1.0]], dtype=np.float32
    )
    resulted_tensor = image2tensor(image)

    assert np.allclose(resulted_tensor, expected_tensor, atol=1e-7)
    assert resulted_tensor.dtype == expected_tensor.dtype


def test_tensor2image_conversion():
    tensor = np.asarray([[-1.0, -0.45, 0], [0.332, 0.8005, 1.0]], dtype=np.float32)
    expected_image = np.asarray([[0, 70, 127], [169, 229, 255]], dtype=np.uint8)
    resulted_image = tensor2image(tensor)

    assert np.array_equal(resulted_image, expected_image)
    assert resulted_image.dtype == expected_image.dtype


def test_image2tensor2image_cycle_conversion():
    image = np.random.randint(low=0, high=256, size=(128, 128, 3), dtype=np.uint8)
    resulted_image = tensor2image(image2tensor(image))

    assert np.allclose(resulted_image, image, atol=1)
    assert resulted_image.dtype == image.dtype
