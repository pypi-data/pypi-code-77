#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import logging
import GLXCurses


class HandlersWindow(object):
    debug: bool

    def _handle_activate_default(self, event_signal, event_args=None):
        """
        The activate-default signal is a keybinding signal which gets emitted when the user activates
        the default widget of ``window``.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data set when the signal handler was connected.
        :type event_args: dit
        """
        if self.debug:
            logging.debug(
                "{0}._handle_activate_default({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        window = GLXCurses.application.get_widget_by_id(event_args["id"])
        del event_args["id"]

        user_data = event_args

    def _handle_activate_focus(self, event_signal, event_args=None):
        """
        The ::activate-focus signal is a keybinding signal which gets emitted when the user activates
        the currently focused widget of ``window``.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data set when the signal handler was connected.
        :type event_args: dit
        """
        if self.debug:
            logging.debug(
                "{0}._handle_activate_focus({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        window = GLXCurses.application.get_widget_by_id(event_args["id"])
        del event_args["id"]

        user_data = event_args

        raise NotImplementedError('"enable-debugging" signal is not implemented yet')

    def _handle_enable_debugging(self, event_signal, event_args=None):
        """
        The ::enable-debugging signal is a keybinding signal which gets emitted when the user enables or disables
        interactive debugging. When toggle is ``True``, interactive debugging is toggled on or off, when it is
        ``False``, the debugger will be pointed at the widget under the pointer.

        The default bindings for this signal are Ctrl-Shift-I and Ctrl-Shift-D.

        Return: ``True`` if the key binding was handled

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data set when the signal handler was connected.
        :type event_args: dit
        """
        if self.debug:
            logging.debug(
                "{0}._handle_enable_debugging({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        window = GLXCurses.application.get_widget_by_id(event_args["id"])
        del event_args["id"]

        toggle = event_args["toggle"]
        del event_args["toggle"]

        user_data = event_args

    def _handle_keys_changed(self, event_signal, event_args=None):
        """
        The ::keys-changed signal gets emitted when the set of accelerators or mnemonics that are
        associated with ``window`` changes.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data set when the signal handler was connected.
        :type event_args: dit
        """
        if self.debug:
            logging.debug(
                "{0}._handle_keys_changed({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        window = GLXCurses.application.get_widget_by_id(event_args["id"])
        del event_args["id"]

        user_data = event_args

    def _handle_set_focus(self, event_signal, event_args=None):
        """
        This signal is emitted whenever the currently focused widget in this window changes.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data set when the signal handler was connected.
        :type event_args: dit
        """
        if self.debug:
            logging.debug(
                "{0}._handle_set_focus({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        window = GLXCurses.application.get_widget_by_id(event_args["id"])
        del event_args["id"]

        user_data = event_args
