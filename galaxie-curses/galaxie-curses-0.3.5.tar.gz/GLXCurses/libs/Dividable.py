#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

from array import array

import GLXCurses


class Dividable(object):

    @staticmethod
    def get_child_x_coordinates(children=None, length=None):
        """
        The function parse children list and calculate coordinates for each ChildElement by regarding ChildProperty
        information's and return a

        :param length: the max length in char
        :type length: int
        :param children: The list of children where we need coordinates
        :type children: list of ChildElement
        :return: a dict with child coordinates
        :rtype: dict of dict
        """
        if length is None:
            length = 0
        if children is None:
            children = []

        coordinates = {}

        if children:

            number_of_not_expand = 0
            unexpanded_width = 0

            for child in children:
                if not child.properties.expand:
                    number_of_not_expand += 1
                    unexpanded_width += child.widget.preferred_width

            try:
                size_by_expanded = int((length - unexpanded_width) / (len(children) - number_of_not_expand) - 1)
            except ZeroDivisionError:
                size_by_expanded = length - unexpanded_width

            count = 0
            for child in children:
                coordinates[child.properties.position] = {"start": count}

                if child.properties.expand:
                    coordinates[child.properties.position]['stop'] = coordinates[child.properties.position][
                                                                         'start'] + size_by_expanded
                else:
                    coordinates[child.properties.position]['stop'] = coordinates[child.properties.position][
                                                                         'start'] + child.widget.preferred_width

                count += coordinates[child.properties.position]['stop'] - coordinates[child.properties.position][
                    'start'] + 1

            # Fit the thing
            if coordinates[len(children) - 1]['stop'] != length:
                coordinates[len(children) - 1]['stop'] = length

        return coordinates

    @staticmethod
    def get_child_y_coordinates(children=None, length=None):
        """
        The function parse children list and calculate coordinates for each ChildElement by regarding ChildProperty
        information's and return a

        :param length: the max length in char
        :type length: int
        :param children: The list of children where we need coordinates
        :type children: list of ChildElement
        :return: a dict with child coordinates
        :rtype: dict of dict
        """
        if length is None:
            length = 0
        if children is None:
            children = []

        coordinates = {}

        if children:
            number_of_not_expand = 0
            unexpanded_height = 0

            for child in children:
                if not child.properties.expand:
                    number_of_not_expand += 1
                    unexpanded_height += child.widget.preferred_height

            try:
                size_by_expanded = int((length - unexpanded_height) / (len(children) - number_of_not_expand) - 1)
            except ZeroDivisionError:
                size_by_expanded = length - unexpanded_height

            count = 0
            for child in children:
                coordinates[child.properties.position] = {"start": count}

                if child.properties.expand:
                    coordinates[child.properties.position]['stop'] = coordinates[child.properties.position][
                                                                         'start'] + size_by_expanded
                else:
                    coordinates[child.properties.position]['stop'] = coordinates[child.properties.position][
                                                                         'start'] + child.widget.preferred_height

                count += coordinates[child.properties.position]['stop'] - coordinates[child.properties.position][
                    'start'] + 1

            # Fit the thing
            if coordinates[len(children) - 1]['stop'] != length:
                coordinates[len(children) - 1]['stop'] = length

        return coordinates
