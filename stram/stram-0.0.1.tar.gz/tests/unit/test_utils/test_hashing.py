from stram.utils.json_processing import Config
from stram.utils.hashing import get_image_hash, get_styling_config_hash


def test_get_image_hash(content_image, style_image, content_image_hash, style_image_hash):
    assert get_image_hash(content_image) == content_image_hash
    assert get_image_hash(style_image) == style_image_hash


def test_get_styling_config_hash():
    styling_config_1 = Config(a1='a1', a2=5.19, a3=17, a4=False)
    styling_config_2 = Config(a4=False, a1='a1', a3=17, a2=5.19)

    styling_config_1_hash = get_styling_config_hash(styling_config_1)
    styling_config_2_hash = get_styling_config_hash(styling_config_2)

    expected_hash = 'a8b5a82d3a040f5fa201c75bf054d9dc798baa2a49d8b2b9f062c2d40ea97521'
    assert styling_config_1_hash == styling_config_2_hash == expected_hash
