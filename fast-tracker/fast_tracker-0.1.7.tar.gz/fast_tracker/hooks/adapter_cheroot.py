# -*- coding: utf-8 -*-


import fast_tracker.api.wsgi_application
import fast_tracker.api.in_function


def instrument_cheroot_wsgiserver(module):

    def wrap_wsgi_application_entry_point(server, bind_addr, wsgi_app,
                                          *args, **kwargs):
        application = fast_tracker.api.wsgi_application.WSGIApplicationWrapper(
                wsgi_app)
        args = [server, bind_addr, application] + list(args)
        return args, kwargs

    fast_tracker.api.in_function.wrap_in_function(
            module,
            'Server.__init__',
            wrap_wsgi_application_entry_point)
