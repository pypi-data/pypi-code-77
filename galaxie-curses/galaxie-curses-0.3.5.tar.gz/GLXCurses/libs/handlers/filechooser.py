#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import logging
import GLXCurses


class HandlersFileChooser:
    debug: bool

    def _handle_current_folder_changed(self, event_signal, event_args=None):
        """
        This signal is emitted when the current folder in a FileChooser changes.

        This can happen due to the user performing some action that changes folders, such as selecting a bookmark or
        visiting a folder on the file list.

        It can also happen as a result of calling a function to explicitly change the current folder in a file chooser.

        Applications should never connect to this signal, but use the “clicked” signal.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data
        :type event_args: dit
        """
        if self.debug:
            logging.debug(
                "{0}._handle_current_folder_changed({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])
        widget.update_directory_list()

        # if hasattr(widget, 'active'):
        #     widget.active = not widget.active

    def _handle_file_activated(self, event_signal, event_args=None):
        """
        This signal is emitted when the user "activates" a file in the file chooser.

        This can happen by double-clicking on a file in the file list, or by pressing Enter.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data
        :type event_args: dit
        """
        if self.debug:
            logging.debug(
                "{0}._handle_file_activated({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        # if hasattr(widget, 'active'):
        #     widget.active = not widget.active

    def _handle_selection_changed(self, event_signal, event_args=None):
        """
        This signal is emitted when there is a change in the set of selected files in a FileChooser.
        This can happen when the user modifies the selection with the mouse or the keyboard, or when explicitly
        calling functions to change the selection.

        Normally you do not need to connect to this signal, as it is easier to wait for the file chooser to
        finish running, and then to get the list of selected files using the functions mentioned below.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data
        :type event_args: dit
        """
        if self.debug:
            logging.debug(
                "{0}._handle_selection_changed({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        # if hasattr(widget, 'active'):
        #     widget.active = not widget.active

    def _handle_update_preview(self, event_signal, event_args=None):
        """
        This signal is emitted when the preview in a file chooser should be regenerated. For example, this can
        happen when the currently selected file changes. You should use this signal if you want your file chooser
        to have a preview widget.

        Once you have installed a preview widget with set_preview_widget(), you should update it
        when this signal is emitted. You can use the functions get_preview_filename() or
        get_preview_uri() to get the name of the file to preview. Your widget may not be able to
        preview all kinds of files; your callback must call set_preview_widget_active() to inform
        the file chooser about whether the preview was generated successfully or not.

        :param event_signal: signal name
        :type event_signal: str
        :param event_args: user data
        :type event_args: dit
        """
        if self.debug:
            logging.debug(
                "{0}._handle_update_preview({1}, {2})".format(
                    self.__class__.__name__, event_signal, event_args
                )
            )
        widget = GLXCurses.application.get_widget_by_id(event_args["id"])

        # if hasattr(widget, 'active'):
        #     widget.active = not widget.active
