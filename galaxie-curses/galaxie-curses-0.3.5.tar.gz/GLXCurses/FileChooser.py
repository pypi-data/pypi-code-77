#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

# Created on 4 avr. 2015


import curses
import os
import time
import logging

import GLXCurses
from GLXCurses.libs.FileChooserFunctions import FileChooserUtils


# https://developer.gnome.org/gtk3/stable/GtkFileChooser.html
class FileSelect(GLXCurses.Widget, FileChooserUtils):
    def __init__(self):
        # Load heritage
        GLXCurses.Widget.__init__(self)
        FileChooserUtils.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = "GLXCurses.FileSelect"
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        # Variables:

        # self.__item_list = None
        self.__item_info_list = None
        self.__item_it_can_be_display = None
        self.__item_scroll_pos = None
        self.__selected_item_pos = None
        self.__selected_item_info_list = None

        # Object use for clickable Text

        self.name_text_object = None
        self.size_text_object = None
        self.mtime_text_object = None

        self.display_history_menu = 0
        self.display_history_text = "History"
        self.history_dir_list_object = None
        self.history_dir_list_prev_object = None
        self.history_dir_list_next_object = None
        self.history_dir_list = list()
        self.history_menu_selected_item = 0
        self.history_menu_selected_item_value = "."
        self.history_menu_item_list_scroll = 0
        self.history_menu_can_be_display = 0
        self.history_menu_item_number = 0

        # Scroll

        # Set thing for the first time, yes like a boss ...

        self.item_it_can_be_display = 0
        self.item_scroll_pos = 0
        self.selected_item_pos = 0
        self.selected_item_info_list = dict()

        # Size management
        self.border_len = 2

        # States
        self.curses_mouse_states = {
            curses.BUTTON1_PRESSED: "BUTTON1_PRESS",
            curses.BUTTON1_RELEASED: "BUTTON1_RELEASED",
            curses.BUTTON1_CLICKED: "BUTTON1_CLICKED",
            curses.BUTTON1_DOUBLE_CLICKED: "BUTTON1_DOUBLE_CLICKED",
            curses.BUTTON1_TRIPLE_CLICKED: "BUTTON1_TRIPLE_CLICKED",
            curses.BUTTON2_PRESSED: "BUTTON2_PRESSED",
            curses.BUTTON2_RELEASED: "BUTTON2_RELEASED",
            curses.BUTTON2_CLICKED: "BUTTON2_CLICKED",
            curses.BUTTON2_DOUBLE_CLICKED: "BUTTON2_DOUBLE_CLICKED",
            curses.BUTTON2_TRIPLE_CLICKED: "BUTTON2_TRIPLE_CLICKED",
            curses.BUTTON3_PRESSED: "BUTTON3_PRESSED",
            curses.BUTTON3_RELEASED: "BUTTON3_RELEASED",
            curses.BUTTON3_CLICKED: "BUTTON3_CLICKED",
            curses.BUTTON3_DOUBLE_CLICKED: "BUTTON3_DOUBLE_CLICKED",
            curses.BUTTON3_TRIPLE_CLICKED: "BUTTON3_TRIPLE_CLICKED",
            # curses.BUTTON4_PRESSED: 'BUTTON4_PRESSED',
            # curses.BUTTON4_RELEASED: 'BUTTON4_RELEASED',
            # curses.BUTTON4_CLICKED: 'BUTTON4_CLICKED',
            # curses.BUTTON4_DOUBLE_CLICKED: 'BUTTON4_DOUBLE_CLICKED',
            # curses.BUTTON4_TRIPLE_CLICKED: 'BUTTON4_TRIPLE_CLICKED',
            curses.REPORT_MOUSE_POSITION: "MOUSE_WHEEL_DOWN",
            curses.BUTTON4_PRESSED: "MOUSE_WHEEL_UP",
            curses.BUTTON_SHIFT: "BUTTON_SHIFT",
            curses.BUTTON_CTRL: "BUTTON_CTRL",
            curses.BUTTON_ALT: "BUTTON_ALT",
        }

        # self.model = model
        self.rep_sup_text = "UP--DIR"
        self.name_text = "Name"
        self.size_text = "Size"
        self.mtime_text = "Modify time"
        self.sort_name_letter = self.name_text[0].lower()
        self.sort_size_letter = self.size_text[0].lower()
        self.sort_mtime_letter = self.mtime_text[0].lower()
        self.history_button_text_prev = "<"
        self.history_button_text_list = ".[^]"
        self.history_button_text_next = ">"

        # Sensitive
        self.can_default = True
        self.can_focus = True
        self.can_prelight = True
        self.sensitive = True
        self.states_list = None
        self._focus_without_selecting = False

        self.label_information_disk_usage = GLXCurses.Label()
        self.label_information_disk_usage.parent = self.parent
        # Subscription
        # Mouse
        self.connect("MOUSE_EVENT", FileSelect._handle_mouse_event)
        # Keyboard
        self.connect("CURSES", FileSelect._handle_key_event)

        self.update_directory_list()

    @property
    def item_it_can_be_display(self):
        """
        Get the number of item it can be display, as set by _set_item_it_can_be_display().

        :return: The number of item it can be display
        :rtype: int
        """
        return self.__item_it_can_be_display

    @item_it_can_be_display.setter
    def item_it_can_be_display(self, value=None):
        """
        Get the number of item it can be display

        :param value: the number of item it can be display
        :type value: int
        :raise TypeError: when ``value`` argument is not a int
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError("'value' must be a int type or None")
        if self.item_it_can_be_display != GLXCurses.clamp_to_zero(value):
            self.__item_it_can_be_display = GLXCurses.clamp_to_zero(value)

    @property
    def item_scroll_pos(self):
        """
        Get the number of item it can be display, as set by _set_item_it_can_be_display().

        :return: The Position on the scroll list
        :rtype: int
        """
        return self.__item_scroll_pos

    @item_scroll_pos.setter
    def item_scroll_pos(self, value=None):
        """
        Position on the scroll list. value=None for reset to 0.

        Default 0

        :param value: the position
        :type value: int or None
        :raise TypeError: when ``value`` argument is not a int or None
        """
        if value is None:
            value = 0

        # Exit as soon of possible
        if type(value) != int:
            raise TypeError("'value' must be a int type")

        # just in case it make teh job
        if self.item_scroll_pos != value:
            self.__item_scroll_pos = value

    @property
    def selected_item_pos(self):
        """
        Position of the selected item.

        :return: The Position on the scroll list
        :rtype: int
        """
        return self.__selected_item_pos

    @selected_item_pos.setter
    def selected_item_pos(self, value=None):
        """
        Position of the selected item in parallel of the scroll list.

        value=None for reset to 0.

        Default: 0

        :param value: the position
        :type value: int or None
        :raise TypeError: when ``value`` argument is not a int or None
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError("'value' must be a int type")
        if self.selected_item_pos != value:
            self.__selected_item_pos = value

    @property
    def selected_item_info_list(self):
        """
        Get the selected file information's list.

        The line_info information's store position:
            item_name_text in position [0]
            item_path_sys in position [1]
            item_size_text in position [2]
            item_time_text in position [3]

        :return: information's about selected item.
        :rtype: dict
        """
        return self.__selected_item_info_list

    @selected_item_info_list.setter
    def selected_item_info_list(self, file_info_list=None):
        """
        Set the files list, internally use for list directory.

        :param file_info_list: a file list
        :type file_info_list: dict
        :raise TypeError: when ``line_info`` argument is not a list or None
        """
        if file_info_list is None:
            file_info_list = list()
        if type(file_info_list) != dict:
            raise TypeError("'line_info' must be a list type")
        if self.selected_item_info_list != file_info_list:
            self.__selected_item_info_list = file_info_list

    @property
    def x_pos_history_next_label(self):
        if self.get_decorated():
            return GLXCurses.round_down(self.width - 1 - self.border_len / 2)
        else:
            return self.width - 1

    @property
    def x_pos_history_list_label(self):
        return self.x_pos_history_next_label - len(self.history_button_text_list)

    @property
    def x_pos_history_prev_label(self):
        if self.get_decorated():
            return GLXCurses.round_down(self.border_len / 2)
        else:
            return 0

    @property
    def x_pos_history_actual_path(self):
        return self.x_pos_history_prev_label + len(self.history_button_text_prev) + 1

    @property
    def x_pos_history_actual_path_allowed_size(self):
        return self.x_pos_history_next_label - self.x_pos_history_actual_path

    @property
    def x_pos_title_mtime(self):
        return GLXCurses.round_down(
            self.mtime_column_width + 1 + (len(str(self.mtime_text)) - 1 / 2) - 4
        )

    @property
    def x_pos_title_size(self):
        return GLXCurses.round_down(
            self.mtime_column_width
            - self.size_column_width
            + 1
            + (len(str(self.size_text)) - 1 / 2)
        )

    @property
    def x_pos_title_name(self):
        return GLXCurses.round_down(
            ((self.mtime_column_width - self.size_column_width) / 2)
            - (len(self.name_text) / 2)
            + 1
        )

    @property
    def x_pos_line_start(self):
        if self.get_decorated():
            return GLXCurses.round_down(self.border_len / 2)
        return 0

    @property
    def x_pos_line_stop(self):
        if self.get_decorated():
            return GLXCurses.round_down(
                self.width - 1 - (self.border_len / 2) - 1
            )
        return self.width - 1 - 1

    @property
    def y_pos_history(self):
        return 0

    @property
    def y_pos_titles(self):
        return self.y_pos_history + 1

    @property
    def y_pos_items(self):
        return self.y_pos_titles + 1

    @property
    def name_column_width(self):
        if self.get_decorated():
            name_column_width = self.width
            name_column_width -= 16
            name_column_width -= self.size_column_width
            name_column_width -= 2
            name_column_width -= self.border_len
        else:
            name_column_width = self.width
            name_column_width -= 16
            name_column_width -= self.size_column_width
            name_column_width -= 2
        return name_column_width

    @property
    def mtime_column_width(self):
        if self.get_decorated():
            mtime_column_width = (
                    self.width - 1 - GLXCurses.round_down(self.border_len / 2)
            )
            mtime_column_width -= len(
                time.strftime("%d/%m/%Y  %H:%M", time.localtime(time.time()))
            )
        else:
            mtime_column_width = self.width - 1
            mtime_column_width -= len(
                time.strftime("%d/%m/%Y  %H:%M", time.localtime(time.time()))
            )
        return GLXCurses.round_down(mtime_column_width)

    @property
    def size_column_width(self):
        return 8

    # Internal function
    def _scroll_up(self):
        if self.selected_item_pos > 0:
            self.selected_item_pos -= 1
            self.emit("selection-changed", {"id": self.id})
        elif self.item_scroll_pos > 0:
            self.item_scroll_pos -= 1
            self.emit("selection-changed", {"id": self.id})

    def _scroll_down(self):
        if (
                self.item_it_can_be_display - 1 != self.selected_item_pos
                and self.__selected_item_pos != len(self.directory_view) - 1
        ):
            self.selected_item_pos += 1
            self.emit("selection-changed", {"id": self.id})
        elif self.item_scroll_pos + self.item_it_can_be_display < len(
                self.directory_view
        ):
            self.item_scroll_pos += 1
            self.emit("selection-changed", {"id": self.id})

    def _history_scroll_up(self):
        if not self.history_menu_selected_item == 0:
            self.history_menu_selected_item -= 1
        else:
            if not self.history_menu_item_list_scroll == 0:
                self.history_menu_item_list_scroll -= 1

    def _history_scroll_down(self):
        if (
                not self.history_menu_can_be_display == self.history_menu_selected_item
                and not self.history_menu_selected_item + 1 == len(self.history_dir_list)
                and not len(self.history_dir_list) == 0
        ):
            self.history_menu_selected_item += 1
        else:
            if (
                    self.history_menu_item_list_scroll + self.history_menu_can_be_display
                    < self.history_menu_item_number + 1
            ):
                self.history_menu_item_list_scroll += 1

    # Curses Display
    def draw_widget_in_area(self):
        self._check_selected()

        self._draw_background()

        self._draw_box_top()
        self._draw_box_bottom()

        if self.widget_decorated:
            self._draw_box_top()
            self._draw_box_bottom()

        self._draw_filechooser()

        if self.widget_decorated:
            self._draw_box_left_side()
            self._draw_box_right_side()
            self._draw_box_upper_left_corner()
            self._draw_box_upper_right_corner()
            self._draw_box_bottom_right_corner()
            self._draw_box_bottom_left_corner()

    def _draw_filechooser(self):
        # History Line
        # History arrow for navigate inside history directory list
        self._draw_history_hline()
        self._draw_history_prev()
        self._draw_history_actual_path()
        self._draw_history_button()
        self._draw_history_next()

        # Titles Column
        self._draw_column_title_sorted_order()

        # Create 3 clickable elements for "Name", "Size", "Modify Time"
        self._draw_column_title_name()
        self._draw_column_title_size()
        self._draw_column_title_mtime()

        # Create 2 Vertical Lines for create columns for Name, Size and Modify Time
        self._draw_column_vline_mtime()
        self._draw_column_vline_size()

        # FOR it use all the window
        count = 0
        for line_number in range(self.y_pos_items, self.height - 2):

            if count < len(self.directory_view):

                # Force the selected high color line to stay on the available box size
                if self.selected_item_pos + 1 > self.item_it_can_be_display:
                    self.selected_item_pos -= 1

                try:
                    # Draw normal line
                    self._draw_line_normal(
                        line_number, self.directory_view[count + self.item_scroll_pos]
                    )

                    # Draw the selected Line
                    # That is the selected line enjoy, cher !!!!
                    if self.selected_item_pos == count:
                        self.selected_item_info_list = self.directory_view[
                            count + self.item_scroll_pos
                            ]
                        self._draw_line_selected(
                            line_number,
                            self.directory_view[count + self.item_scroll_pos],
                        )
                        self._draw_information_text(
                            self.directory_view[count + self.item_scroll_pos]
                        )
                except IndexError:
                    continue

            count += 1

        # Information part
        self._draw_information_hline()

        # If the item value is '..' it use Directory setting
        # if self.get_has_focus():
        #     self._draw_information_text(line_info)

        # Disk Usage
        self._draw_information_disk_usage()

        # Test if the history widget should be display
        if self.display_history_menu:
            self.history_dialog_box = GLXCurses.FileChooserMenu(
                y=self.y_pos_history - 1,
                x=self.x_pos_history_list_label,
                label=self.display_history_text,
            )
            self.history_dialog_box.parent = self
            self.history_dialog_box.history_dir_list = self.history_dir_list

    def _draw_line_normal(self, line_number, line_info):
        if type(line_info) != dict:
            raise TypeError("Need a Dict")
        if type(line_number) != int:
            raise TypeError("Need a int")

        # Background
        self.add_horizontal_line(
            y=line_number,
            x=self.x_pos_line_start,
            character=" ",
            length=self.x_pos_line_stop - self.x_pos_line_start,
            color=self.color_normal,
        )

        # Name
        name_to_display = GLXCurses.resize_text(
            "{0}{1}".format(line_info["to_display_symbol"], line_info["name"]),
            self.name_column_width,
        )

        self.add_string(
            y=line_number,
            x=self.x_pos_line_start,
            text=name_to_display,
            color=self.style.color(
                fg=line_info["to_display_color"],
                bg=self.background_color_normal,
                attributes=False,
            )
                  | line_info["to_display_attributes"],
        )

        # Size
        name_to_display = GLXCurses.resize_text(
            str(line_info["to_display_size"]), self.size_column_width
        )

        self.add_string(
            y=line_number,
            x=self.mtime_column_width - len(name_to_display),
            text=name_to_display,
            color=self.style.color(
                fg=line_info["to_display_color"],
                bg=self.background_color_normal,
                attributes=False,
            )
                  | line_info["to_display_attributes"],
        )

        # Date
        self.add_string(
            y=line_number,
            x=self.mtime_column_width + 1,
            text=str(line_info["to_display_mtime"]),
            color=self.style.color(
                fg=line_info["to_display_color"],
                bg=self.background_color_normal,
                attributes=False,
            )
                  | line_info["to_display_attributes"],
        )

        # Draw the first vertical lines with high light color
        self.add_vertical_line(
            y=line_number,
            x=self.mtime_column_width - self.size_column_width,
            character=curses.ACS_VLINE,
            length=1,
            color=self.color_normal,
        )

        # Draw the second vertical lines with high light color
        self.add_vertical_line(
            y=line_number,
            x=self.mtime_column_width,
            character=curses.ACS_VLINE,
            length=1,
            color=self.color_normal,
        )

    def _draw_line_selected(self, line_number, file_info_list):
        if self.has_prelight:
            # Line Background
            self.add_horizontal_line(
                y=line_number,
                x=self.x_pos_line_start,
                character=" ",
                length=self.x_pos_line_stop - self.x_pos_line_start,
                color=self.style.color(fg=(0, 255, 255), bg=(0, 0, 0), attributes=False)
                      | GLXCurses.GLXC.A_REVERSE,
            )

            # Name
            name_to_display = GLXCurses.resize_text(
                "{0}{1}".format(
                    file_info_list["to_display_symbol"],
                    file_info_list["name"],
                ),
                self.name_column_width,
            )

            self.add_string(
                y=line_number,
                x=self.x_pos_line_start,
                text=name_to_display,
                color=self.style.color(fg=(0, 255, 255), bg=(0, 0, 0), attributes=False)
                      | GLXCurses.GLXC.A_REVERSE,
            )

            # Size
            name_to_display = GLXCurses.resize_text(
                str(file_info_list["to_display_size"]), self.size_column_width
            )
            # print(line_info)
            self.add_string(
                y=line_number,
                x=self.mtime_column_width - len(name_to_display),
                text=name_to_display,
                color=self.style.color(fg=(0, 255, 255), bg=(0, 0, 0), attributes=False)
                      | GLXCurses.GLXC.A_REVERSE,
            )

            # Date
            self.add_string(
                y=line_number,
                x=self.mtime_column_width + 1,
                text=str(file_info_list["to_display_mtime"]),
                color=self.style.color(fg=(0, 255, 255), bg=(0, 0, 0), attributes=False)
                      | GLXCurses.GLXC.A_REVERSE,
            )

            # Draw the first vertical lines with high light color
            self.add_vertical_line(
                y=line_number,
                x=self.mtime_column_width - self.size_column_width,
                character=curses.ACS_VLINE,
                length=1,
                color=self.style.color(fg=(0, 255, 255), bg=(0, 0, 0), attributes=False)
                      | GLXCurses.GLXC.A_REVERSE,
            )

            # Draw the second vertical lines with high light color
            self.add_vertical_line(
                y=line_number,
                x=self.mtime_column_width,
                character=curses.ACS_VLINE,
                length=1,
                color=self.style.color(fg=(0, 255, 255), bg=(0, 0, 0), attributes=False)
                      | GLXCurses.GLXC.A_REVERSE,
            )

    def _draw_information_hline(self):
        if self.get_decorated():
            self.add_horizontal_line(
                y=self.height - 3,
                x=self.x_pos_line_start,
                character=curses.ACS_HLINE,
                length=self.x_pos_line_stop + 2 - self.x_pos_line_start,
                color=self.color_normal,
            )

        else:
            self.add_horizontal_line(
                y=self.height - 3,
                x=self.x_pos_line_start,
                character=curses.ACS_HLINE,
                length=self.width - self.x_pos_line_start,
                color=self.color_normal,
            )

    def _draw_information_text(self, item):

        self.add_string(
            y=self.height - 2,
            x=self.x_pos_line_start,
            text=GLXCurses.resize_text(
                str(item["to_display_name"]), self.width - 2
            ),
            color=self.color_normal,
        )

    def _draw_information_disk_usage(self):
        # Add Disk usage
        disk_space_line = GLXCurses.disk_usage(self.cwd)
        if self.get_decorated():
            self.add_string(
                y=self.height - 1,
                x=self.width
                  - 1
                  - int(self.border_len / 2)
                  - len(disk_space_line),
                text=disk_space_line,
                color=self.color_normal,
            )
        else:
            self.add_string(
                y=self.height - 1,
                x=self.width - len(disk_space_line),
                text=disk_space_line,
                color=self.color_normal,
            )

    def _draw_history_hline(self):
        self.add_horizontal_line(
            y=self.y_pos_history,
            x=self.x_pos_line_start,
            character=curses.ACS_HLINE,
            length=self.x_pos_line_stop - self.x_pos_line_start,
            color=self.color_normal,
        )

    def _draw_history_prev(self):
        # History arrow for navigate inside history directory list
        self.add_character(
            y=self.y_pos_history,
            x=self.x_pos_history_prev_label,
            character=self.history_button_text_prev,
            color=self.color_normal,
        )

    def _draw_history_actual_path(self):
        spacing = 2
        internal_spacing = 2
        prepend_text = "..."

        label_dir = self.cwd
        label_dir = label_dir.replace(os.path.expanduser("~"), "~")
        ce_que_je_retire = self.x_pos_history_actual_path_allowed_size
        ce_que_je_retire -= self.x_pos_history_actual_path
        ce_que_je_retire -= spacing

        if internal_spacing >= 2:
            space_to_add = " " * int(internal_spacing / 2)
            label_dir = space_to_add + label_dir + space_to_add

        label_dir = label_dir[-ce_que_je_retire:]

        if self.has_focus:
            color = (
                    self.style.color(fg=(255, 255, 255), bg=(0, 0, 0), attributes=False)
                    | GLXCurses.GLXC.A_REVERSE
            )
        else:
            color = self.color_normal

        if ce_que_je_retire > 1:
            self.add_string(
                y=self.y_pos_history,
                x=self.x_pos_history_actual_path,
                text=label_dir,
                color=color,
            )

            if ce_que_je_retire <= len(label_dir):
                self.add_string(
                    y=self.y_pos_history,
                    x=self.x_pos_history_actual_path,
                    text=prepend_text,
                    color=color,
                )

    def _draw_history_button(self):
        # History button for display the history dialog window
        self.add_string(
            y=self.y_pos_history,
            x=self.x_pos_history_list_label,
            text=self.history_button_text_list,
            color=self.color_normal,
        )

    def _draw_history_next(self):
        # History next arrow for navigate inside history directory list
        self.add_character(
            y=self.y_pos_history,
            x=self.x_pos_history_next_label,
            character=self.history_button_text_next,
            color=self.color_normal,
        )

    def _draw_column_vline_size(self):
        self.add_vertical_line(
            y=self.y_pos_titles,
            x=self.mtime_column_width - self.size_column_width,
            character=curses.ACS_VLINE,
            length=self.height - 2 - self.y_pos_titles,
            color=self.color_normal,
        )

    def _draw_column_vline_mtime(self):
        self.add_vertical_line(
            y=self.y_pos_titles,
            x=self.mtime_column_width,
            character=curses.ACS_VLINE,
            length=self.height - 2 - self.y_pos_titles,
            color=self.color_normal,
        )

    def _draw_column_title_mtime(self):
        self.add_string(
            y=self.y_pos_titles,
            x=self.x_pos_title_mtime,
            text=self.mtime_text,
            color=self.style.color(
                fg=self.style.attribute_to_rgb("mid", "STATE_NORMAL"),
                bg=self.background_color_normal,
            ),
        )

    def _draw_column_title_size(self):
        self.add_string(
            y=self.y_pos_titles,
            x=self.x_pos_title_size,
            text=self.size_text,
            color=self.style.color(
                fg=self.style.attribute_to_rgb("mid", "STATE_NORMAL"),
                bg=self.background_color_normal,
            ),
        )

    def _draw_column_title_name(self):
        self.add_string(
            y=self.y_pos_titles,
            x=self.x_pos_title_name,
            text=self.name_text,
            color=self.style.color(
                fg=self.style.attribute_to_rgb("mid", "STATE_NORMAL"),
                bg=self.background_color_normal,
            ),
        )

    def _draw_column_title_sorted_order(self):
        # Verify which short type is selected and display ('n) (.n) ('s) (.s) ('m) (.m)
        if self.sort_by_name:
            if self.sort_name_order:
                symbol = "'n"
            else:
                symbol = ".n"
        elif self.sort_by_size:
            if self.sort_size_order:
                symbol = "'s"
            else:
                symbol = ".s"
        elif self.sort_by_mtime:
            if self.sort_mtime_order:
                symbol = "'t"
            else:
                symbol = ".t"
        else:
            symbol = ""

        self.add_string(
            y=self.y_pos_titles,
            x=self.x_pos_line_start,
            text=symbol,
            color=self.style.color(
                fg=self.style.attribute_to_rgb("mid", "STATE_NORMAL"),
                bg=self.background_color_normal,
            ),
        )

    def _check_selected(self):
        if self.can_default:
            if GLXCurses.Application().has_default:
                if GLXCurses.Application().has_default.id == self.id:
                    self.has_default = True
                else:
                    self.has_default = False
        # if self.can_focus:
        #     if GLXCurses.Application().has_focus:
        #         if GLXCurses.Application().has_focus.id == self.id:
        #             self.has_focus = True
        #         else:
        #             self.has_focus = False
        if self.can_prelight:
            if GLXCurses.Application().has_prelight:
                if GLXCurses.Application().has_prelight.id == self.id:
                    self.has_prelight = True
                else:
                    self.has_prelight = False

    # def _grab_focus(self):
    #     """
    #     Internal method, for Select the contents of the Entry it take focus.
    #
    #     See: grab_focus_without_selecting ()
    #     """
    #     if self.can_focus:
    #         GLXCurses.Application().has_focus = self
    #         GLXCurses.Application().has_default = self
    #         GLXCurses.Application().has_prelight = self
    #         self._check_selected()

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
        if (
                self.sensitive
                and isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement)
                and GLXCurses.Application().has_focus.id == self.id
        ):
            # setting
            key = event_args[0]

            if not self.display_history_menu == 1:
                # Touch Escape
                if key == GLXCurses.GLXC.KEY_ESC:
                    self.emit(
                        "RELEASE_FOCUS",
                        {"class": self.__class__.__name__, "id": self.id},
                    )
                    self._check_selected()

                if key == curses.KEY_UP:
                    self._scroll_up()

                if key == curses.KEY_DOWN:
                    self._scroll_down()

                if key == curses.KEY_HOME:
                    self.selected_item_pos = 0
                    self.item_scroll_pos = 0

                # END Touch
                if key == curses.KEY_END:
                    # Scroll to down like curses.KEY_DOWN via a loop it have the len of item in directory,
                    for line_number in range(0, len(self.directory_view)):
                        self._scroll_down()

                if key == curses.KEY_NPAGE:
                    for line_number in range(0, self.item_it_can_be_display - 1):
                        self._scroll_down()

                if key == curses.KEY_PPAGE:
                    for line_number in range(0, self.item_it_can_be_display - 1):
                        self._scroll_up()

                if key == ord("n"):
                    self.sort_by_name = True
                    self.sort_by_size = False
                    self.sort_by_mtime = False
                    self.sort_name_order = not self.sort_name_order

                if key == ord("s"):
                    self.sort_by_name = False
                    self.sort_by_size = True
                    self.sort_by_mtime = False
                    self.sort_size_order = not self.sort_size_order

                if key == ord("t"):
                    self.sort_by_name = False
                    self.sort_by_size = False
                    self.sort_by_mtime = True
                    self.sort_mtime_order = not self.sort_mtime_order

                if key == ord("h"):
                    self.display_history_menu = not self.display_history_menu

                if key == curses.KEY_ENTER or key == ord("\n"):

                    # We gat the line go do something
                    if os.path.isdir(self.selected_item_info_list["path"]):
                        self.emit(
                            "current-folder-changed",
                            {"class": self.__class__.__name__, "id": self.id},
                        )
                        self.cwd = self.selected_item_info_list["path"]

                        self.selected_item_pos = 0
                        self.item_scroll_pos = 0

                        found = 0
                        for item in self.history_dir_list:
                            if item == self.cwd:
                                found = 1
                        if not found == 1:
                            self.history_dir_list.append(self.cwd)

                    else:
                        self.emit(
                            "file-activated",
                            {"class": self.__class__.__name__, "id": self.id},
                        )

            # When history i display enable special shortcut
            elif self.display_history_menu == 1:
                if key == GLXCurses.GLXC.KEY_ESC:
                    # Escape was pressed
                    self.display_history_menu = not self.display_history_menu

                elif key == curses.KEY_UP:
                    self._history_scroll_up()

                elif key == curses.KEY_DOWN:
                    self._history_scroll_down()

                elif key == curses.KEY_ENTER or key == ord("\n"):
                    self.display_history_menu = not self.display_history_menu
                    if os.path.isdir(self.history_menu_selected_item_value):
                        self.cwd = self.history_menu_selected_item_value
                        self.selected_item = 0
                        self.item_list_scroll = 0

                elif key == ord("h"):
                    self.display_history_menu = not self.display_history_menu

            # Create a Dict with everything
            instance = {
                "class": self.__class__.__name__,
                "id": self.id,
                "event_signal": event_signal,
            }
            # EVENT EMIT
            # Application().emit(self.curses_mouse_states[event], instance)
            self.emit(str(key), instance)

    def _handle_mouse_event(self, event_signal, event_args):

        if self.sensitive:
            (mouse_event_id, x, y, z, event) = event_args

            # Be sure we select really the Button
            y -= self.y
            x -= self.x
            that_for_me = (
                    0 <= y <= self.height - 1
                    and 0 <= x <= self.width - 1
            )

            if that_for_me:
                self.emit("grab-focus", {"id": self.id})

                # First line Prev / Next / History
                if y == 0:
                    if (
                            self.x_pos_history_prev_label
                            <= x
                            <= self.x_pos_history_prev_label
                    ):
                        # logging.debug('x:' + str(x) + " y:" + str(y))
                        if not self.history_menu_selected_item == 0:
                            self.history_menu_selected_item -= 1

                        if os.path.isdir(
                                os.path.realpath(
                                    self.history_dir_list[self.history_menu_selected_item]
                                )
                        ):
                            self.cwd = os.path.realpath(
                                self.history_dir_list[self.history_menu_selected_item]
                            )

                            self.selected_item_pos = 0
                            self.item_scroll_pos = 0

                    if (
                            self.x_pos_history_list_label
                            <= x
                            <= self.x_pos_history_list_label
                            - 1
                            + len(self.history_button_text_list)
                    ):
                        self.display_history_menu = not self.display_history_menu

                    if (
                            self.x_pos_history_next_label
                            <= x
                            <= self.x_pos_history_next_label
                    ):

                        if (
                                len(self.history_dir_list)
                                > self.history_menu_selected_item + 1
                        ):
                            self.history_menu_selected_item += 1

                            if os.path.isdir(
                                    self.history_dir_list[self.history_menu_selected_item]
                            ):
                                self.cwd = self.history_dir_list[
                                    self.history_menu_selected_item
                                ]

                                self.selected_item_pos = 0
                                self.item_scroll_pos = 0
                # Titles
                if y == self.y_pos_titles:
                    if (
                            event == curses.BUTTON1_PRESSED
                            or event == curses.BUTTON2_PRESSED
                            or event == curses.BUTTON3_PRESSED
                            or event == curses.BUTTON4_PRESSED
                            or event == curses.BUTTON1_CLICKED
                            or event == curses.BUTTON2_CLICKED
                            or event == curses.BUTTON3_CLICKED
                            or event == curses.BUTTON4_CLICKED
                    ):
                        x_pos_name_start = self.x_pos_title_name - self.x - 1
                        if (
                                x_pos_name_start
                                <= x
                                <= self.x_pos_title_name + len(self.name_text) - 1
                        ):
                            self.sort_by_name = True
                            self.sort_by_size = False
                            self.sort_by_mtime = False
                            self.sort_name_order = not self.sort_name_order
                            self.update_directory_list()
                        if (
                                self.x_pos_title_size
                                <= x
                                <= self.x_pos_title_size + len(self.size_text) - 1
                        ):
                            self.sort_by_name = False
                            self.sort_by_size = True
                            self.sort_by_mtime = False
                            self.sort_size_order = not self.sort_size_order
                            self.update_directory_list()
                        if (
                                self.x_pos_title_mtime
                                <= x
                                <= self.x_pos_title_mtime + len(self.mtime_text) - 1
                        ):
                            self.sort_by_name = False
                            self.sort_by_size = False
                            self.sort_by_mtime = True
                            self.sort_mtime_order = not self.sort_mtime_order
                            self.update_directory_list()

                # Mouse wheel
                if (
                        self.y_pos_titles + 1 <= y <= self.height - 3
                        and event != 524288
                        and event != 134217728
                        and event != curses.BUTTON4_PRESSED
                ):
                    clicked_line = y - self.y_pos_titles - 1
                    if 0 <= x <= self.width - 1:

                        if event == curses.BUTTON1_DOUBLE_CLICKED:
                            if os.path.isdir(self.selected_item_info_list["path"]):
                                self.emit(
                                    "current-folder-changed",
                                    {"class": self.__class__.__name__, "id": self.id},
                                )
                                self.cwd = self.selected_item_info_list["path"]

                                self.selected_item_pos = 0
                                self.item_scroll_pos = 0

                                found = 0
                                for item in self.history_dir_list:
                                    if item == self.cwd:
                                        found = 1
                                if not found == 1:
                                    self.history_dir_list.append(self.cwd)

                            else:
                                self.emit(
                                    "file-activated",
                                    {"class": self.__class__.__name__, "id": self.id},
                                )

                        if (
                                event == curses.BUTTON1_CLICKED
                                or event == curses.BUTTON1_PRESSED
                        ):
                            if clicked_line <= len(self.directory_view):
                                self.selected_item_pos = clicked_line
                            else:
                                # Scroll to down like curses.KEY_DOWN via a loop
                                # it have the len of item in directory,
                                for line_number in range(0, len(self.directory_view)):
                                    self._scroll_down()

                if event == 524288 or event == 65536:
                    if (
                            self.display_history_menu != 1
                            and self.display_history_menu != 1
                    ):
                        # self._scroll_up()

                        for line_number in range(
                                0, int((self.item_it_can_be_display - 1) / 2)
                        ):
                            self._scroll_up()

                    else:
                        self._history_scroll_up()

                if event == 134217728 or event == 2097152:
                    if not self.display_history_menu == 1:
                        self._scroll_down()

                        for line_number in range(
                                0, int((self.item_it_can_be_display - 1) / 2)
                        ):
                            self._scroll_down()

                    else:
                        self._history_scroll_down()

                # EVENT EMIT
                self.emit(
                    self.curses_mouse_states[event],
                    {
                        "class": self.__class__.__name__,
                        "event_signal": event_signal,
                        "id": self.id,
                    },
                )
            else:
                # The widget is not selected
                self.has_focus = False
                self._check_selected()
        else:
            if self.debug:
                logging.debug(
                    "{0} -> id:{1}, object:{2}, is not sensitive".format(
                        self.__class__.__name__, self.id, self
                    )
                )

    def update_preferred_sizes(self):
        # it_can_be_display
        # what is 5 or 4 ????
        self.preferred_width = self.width
        self.preferred_height = self.height
        self.item_it_can_be_display = self.height - 5
