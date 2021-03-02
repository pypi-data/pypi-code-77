import pytest

import cuenca

cuenca.configure('AKEkpBFilfTKisGRlcYIlpMA', '3sWzgw45tWxnzP01Cc3S9WkQ-4iG8GfKVWMB-XBrWuL7JIJ2tSK9ptSaLyW_8C76UTTaGieChEE26DgMYBeudg', sandbox=True)


@pytest.fixture(scope='module')
def vcr_config():
    config = dict()
    config['filter_headers'] = [
        ('Authorization', 'DUMMY'),
        ('X-Cuenca-Token', 'DUMMY'),
    ]
    return config
