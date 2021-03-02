#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import logging
import GLXCurses


class HandlersStatusbar(object):
    debug: bool

    def _handle_text_popped(self, event_signal, event_args=None):
        if self.debug:
            logging.debug(
                "{0}._handle_text_popped({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )

    def _handle_text_pushed(self, event_signal, event_args=None):
        if self.debug:
            logging.debug(
                "{0}._handle_text_pushed({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
