from pelican import signals

import multiprocessing
import htmlmin
import os
import re

import logging
logger = logging.getLogger(__name__)


def run(pelican):
    """called after the website has been build to minify the html pages"""

    if pelican.settings.get(
            'HTMLMIN_ENABLED', logger.getEffectiveLevel() > logging.DEBUG
    ) is False:
        logger.debug("'pelican-htmlmin' disabled")
        return

    options = pelican.settings.get(
        'HTMLMIN_OPTIONS', {
            'remove_comments': True,
            'remove_all_empty_space': True,
            'remove_optional_attribute_quotes': False})
    for key, value in options.items():
        logger.debug('htmlmin: using option: %s = %s', key, value)

    htmlfile = re.compile(
        pelican.settings.get('HTMLMIN_MATCH', r'.html?$'))

    pool = multiprocessing.Pool()

    for base, _, files in os.walk(pelican.settings['OUTPUT_PATH']):
        for page in filter(htmlfile.search, files):
            filepath = os.path.join(base, page)
            pool.apply_async(worker, (filepath, options))

    pool.close()
    pool.join()


def worker(filepath, options):
    """use htmlmin to minify the given file"""

    with open(filepath, encoding='utf-8') as page:
        rawhtml = page.read()

    with open(filepath, 'w', encoding='utf-8') as page:
        logger.debug('htmlmin: Minifying %s', filepath)
        try:
            compressed = htmlmin.minify(rawhtml, **options)
            page.write(compressed)
        except Exception as e:
            logger.critical('htmlmin: Failed to minify %s: %s',
                            filepath, e)


def register():
    """minify HTML at the end of the pelican build"""
    signals.finalized.connect(run)
