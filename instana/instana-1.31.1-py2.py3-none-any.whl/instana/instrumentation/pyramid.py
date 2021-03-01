from __future__ import absolute_import

import sys

from ...log import logger
# from ...singletons import tracer, agent
# from ...util import strip_secrets

class InstanaTweenFactory:
    def __init__(self, handler, registry):
        self.handler = handler

    def __call__(self, request):
        ctx = tracer.extract(ot.Format.HTTP_HEADERS, request.headers)
        
        # request.iscope = tracer.start_active_span('pyramid', child_of=ctx)
        # span = request.iscope.span
        span = self
        
        span.set_tag("http.host", request.host)
        span.set_tag("http.method", request.method)
        span.set_tag("http.path", request.path)

        if hasattr(agent, 'extra_headers') and agent.extra_headers is not None:
            for custom_header in agent.extra_headers:
                # Headers are available in this format: HTTP_X_CAPTURE_THIS
                h = ('HTTP_' + custom_header.upper()).replace('-', '_')
                if h in request.headers:
                    span.set_tag("http.%s" % custom_header, request.headers[h])

        # if len(request.query_string):
        #    scrubbed_params = strip_secrets(request.query_string, agent.secrets_matcher, agent.secrets_list)
        #    span.set_tag("http.params", scrubbed_params)

        response = self.handler(request)

        span.set_tag("http.status", response.status)
        # span.close()

        return response

    def set_tag(self, k, v):
        logger.debug("setting tag %s -> %s" % (k, v))

raise "Meh"

try:
    import pyramid
    
    logger.debug("Instrumenting pyramid")
    from pyramid.config import Configurator
    with Configurator() as config:
        config.add_tween("InstanaTweenFactory")
        
except ImportError:
    pass
