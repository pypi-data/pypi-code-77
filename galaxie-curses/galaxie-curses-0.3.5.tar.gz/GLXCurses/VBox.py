#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class VBox(GLXCurses.Box, GLXCurses.Dividable):
    def __init__(self):
        # Load heritage
        GLXCurses.Box.__init__(self)
        GLXCurses.Dividable.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = "GLXCurses.VBox"
        self.name = "{0}{1}".format(self.__class__.__name__, self.id)

        self.preferred_height = 2
        self.preferred_width = 2

        # Default Value
        self.spacing = 0
        self.homogeneous = True

    def new(self, homogeneous=True, spacing=None):
        """
        Creates a new GLXCurses :class:`VBox <GLXCurses.VBox.VBox>`

        :param homogeneous: True if all children are to be given equal space allotments.
        :type homogeneous: bool
        :param spacing: The number of characters to place by default between children.
        :type spacing: int
        :return: a new :class:`VBox <GLXCurses.VBox.VBox>`.
        :raise TypeError: if ``homogeneous`` is not bool type
        :raise TypeError: if ``spacing`` is not int type or None
        """
        if type(homogeneous) != bool:
            raise TypeError('"homogeneous" argument must be a bool type')
        if spacing is not None:
            if type(spacing) != int:
                raise TypeError('"spacing" must be int type or None')

        self.__init__()
        self.spacing = GLXCurses.clamp_to_zero(spacing)
        self.homogeneous = homogeneous
        return self

    def draw_widget_in_area(self):
        # in case it have children attach to the widget.
        if self.children:
            coordinates = GLXCurses.Dividable.get_child_x_coordinates(
                children=self.children,
                length=self.height,
            )
            # for each children
            used_height_spacing = 0
            for child in self.children:
                if used_height_spacing < self.height:
                    child.widget.stdscr = self.stdscr
                    child.widget.x = self.x
                    child.widget.y = coordinates[child.properties.position]['start'] + self.y
                    child.widget.width = self.width
                    # child.widget.width = coordinates[child.properties.position]['stop'] - \
                    #                      coordinates[child.properties.position]['start'] + 1
                    if child.properties.position == len(self.children) - 1:
                        child.widget.height = coordinates[child.properties.position]['stop'] - \
                                             coordinates[child.properties.position]['start']
                    else:
                        child.widget.height = coordinates[child.properties.position]['stop'] - \
                                             coordinates[child.properties.position]['start'] + 1

                    if hasattr(child.widget, 'update_preferred_sizes'):
                        child.widget.update_preferred_sizes()
                        child.widget.draw_widget_in_area()
                        used_height_spacing += child.widget.height

    def update_preferred_sizes(self):
        if self.children:

            preferred_height = 0
            preferred_width = 0

            for child in self.children:
                preferred_height += child.widget.preferred_height
                if preferred_width < child.widget.preferred_width:
                    preferred_width = child.widget.preferred_width

            self.preferred_width = preferred_width
            self.preferred_height = preferred_height
