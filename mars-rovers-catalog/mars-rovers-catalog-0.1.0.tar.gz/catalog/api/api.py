"""Query Mars RSS API module."""

from urllib.parse import urlencode

from requests import get

from ..misc import logger


API_URL = 'https://mars.nasa.gov/rss/api/'

HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}

log_api, debug_api = logger('Mars API', info_stdout=True)


def _flat_json(json) -> dict:
    """Flatten JSON dict."""
    res = {}
    for key, value in json.items():
        if isinstance(value, dict):
            res.update(_flat_json(value))
        else:
            res[key] = value
    return res


def get_json(page=0, num=100, category='mars2020', order='sol+desc'):
    """Get images list and metadata as JSON.

    Parameters
    ----------
    page: int, optional
        Page to query (default: `0`).
    num: int, optional
        Number of result per page (default: `100`).
        Currently this value is limited by the API at 100.
    category: str, optional
        Category of images to query (default: `mars2020`).
    order: str, optional
        Images sorting order (default: `sol+desc`).

    Returns
    -------
    [dict, ...]
        List of images infos (flattened).
    int
        Total number of images for the query.

    Note
    ----
    Select only the full-res and RAW images.
    Discard the thumbnails and color-processed images.

    Order by descreasing `sol`.

    """
    params = {
        'feed': 'raw_images',
        'feedtype': 'json',
        'category': category,
        'num': num,
        'page': page,
        'order': order,
        'extended': 'sample_type::full,product_type::raw',
    }

    payload = urlencode(params, safe=':+,')

    log_api.debug('Payload: %s', payload)

    resp = get(API_URL, params=payload, headers=HEADERS).json()

    imgs = [_flat_json(img) for img in resp['images']]
    total = resp['total_results']

    first_img = 1 + page * num
    last_img = min(num, len(imgs)) + page * num
    current_page = page + 1
    last_page = total // num + 1

    log_api.info('Downloaded images %i-%i/%i (page %i/%i)',
                 first_img, last_img, total, current_page, last_page)

    log_api.debug('Response: %s', resp)

    return imgs, total


def get_all(lastest=None, **kwargs):
    """Get the list of all images since the last known image.

    Parameters
    ----------
    lastest: str, optional
        Latest image id.
        If None is provided (default), the full list
        images will be downloaded.

    Returns
    -------
    [dict, ...]
        List of the latest images.

    See Also
    --------
    :py:func:`get_json`

    """
    new_imgs, total = get_json(page=0, **kwargs)

    last_page = total // len(new_imgs) + 1

    imgs = []
    for page in range(1, last_page + 1):
        imgs_id = [img['imageid'] for img in new_imgs]

        if lastest is not None and lastest in imgs_id:
            imgs.extend(new_imgs[:imgs_id.index(lastest)])
            break

        imgs.extend(new_imgs)

        if page < last_page:
            new_imgs, _ = get_json(page=page, **kwargs)

    return imgs[::-1]
