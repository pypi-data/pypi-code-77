#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import logging
import GLXCurses


class HandlersApplication:
    debug: bool

    def _handle_release_default(self, event_signal, event_args=None):
        if self.debug:
            logging.debug(
                "{0}._handle_release_default({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        if isinstance(widget, GLXCurses.Widget):

            for child in GLXCurses.Application().active_widgets:
                if hasattr(child.widget, "has_default"):
                    if child.id == widget.id:
                        child.widget.has_default = False
                if hasattr(GLXCurses.Application(), "has_default") and GLXCurses.Application().has_default:
                    if GLXCurses.Application().has_default.id == widget.id:
                        GLXCurses.Application().has_default = None

    def _handle_release_prelight(self, event_signal, event_args=None):
        if self.debug:
            logging.debug(
                "{0}._handle_release_prelight({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        if isinstance(widget, GLXCurses.Widget):

            for child in GLXCurses.Application().active_widgets:
                if hasattr(child.widget, "has_prelight"):
                    if child.id == widget.id:
                        child.widget.has_prelight = False
                if hasattr(GLXCurses.Application(), "has_prelight") and GLXCurses.Application().has_prelight:
                    if GLXCurses.Application().has_prelight.id == widget.id:
                        GLXCurses.Application().has_prelight = None

    def _handle_claim_prelight(self, event_signal, event_args=None):
        if self.debug:
            logging.debug(
                "{0}._handle_claim_prelight({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        widget_to_set = GLXCurses.Application().get_widget_by_id(event_args["id"])

        if isinstance(widget_to_set, GLXCurses.Widget):

            for child in GLXCurses.Application().active_widgets:
                if hasattr(child.widget, "has_prelight"):
                    if child.id == widget_to_set.id:
                        child.widget.has_prelight = True
                        GLXCurses.Application().has_prelight = widget_to_set
                    else:
                        child.widget.has_prelight = False

    def _handle_claim_default(self, event_signal, event_args=None):
        if self.debug:
            logging.debug(
                "{0}._handle_claim_default({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        if isinstance(widget, GLXCurses.Widget):

            for child in GLXCurses.Application().active_widgets:
                if hasattr(child.widget, "has_default"):
                    if child.id == widget.id:
                        child.widget.has_default = True
                        GLXCurses.Application().has_default = widget
                    else:
                        child.widget.has_default = False
