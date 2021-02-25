# -*- coding: utf-8 -*-

import fast_tracker.api.wsgi_application
import fast_tracker.api.in_function


def instrument_waitress_server(module):
    def wrap_wsgi_application_entry_point(server, application,
                                          *args, **kwargs):
        application = fast_tracker.api.wsgi_application.WSGIApplicationWrapper(
            application)
        args = [server, application] + list(args)
        return args, kwargs

    fast_tracker.api.in_function.wrap_in_function(module,
                                                  'WSGIServer.__init__', wrap_wsgi_application_entry_point)
