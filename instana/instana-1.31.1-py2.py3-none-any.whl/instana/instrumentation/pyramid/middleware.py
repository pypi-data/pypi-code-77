from __future__ import absolute_import

from ...log import logger
# from ...singletons import tracer, agent
# from ...util import strip_secrets

class InstanaMiddleware(object):
    def __init__(self, app):
        logger.debug("===== HELLO =====")
        self.app = app

    def __call__(self, env, start_response):
        logger.debug(env)
        return self.app(env, start_response)

