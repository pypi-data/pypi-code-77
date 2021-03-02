#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import GLXCurses
import curses
from curses import (
    A_BOLD,
    A_REVERSE,
    KEY_ENTER,
    BUTTON1_RELEASED,
    BUTTON1_CLICKED,
    BUTTON1_PRESSED,
)


class MenuItem(GLXCurses.Widget):
    def __init__(self):
        GLXCurses.Widget.__init__(self)
        self.__accel_path = None
        self.__label = None
        self.__right_justified = None
        self.__spacing = None
        self.__text_short_cut = None
        self.__is_accel = None
        self.__have_cross_a_accel = None

        self.accel_path = None
        self.label = None
        self.right_justified = None
        self.spacing = 1
        self.can_focus = True
        self.can_prelight = True
        self.can_default = True
        self.debug = False

        # Subscription
        # Mouse
        self.connect("MOUSE_EVENT", MenuItem._handle_mouse_event)
        # Keyboard
        self.connect("CURSES", MenuItem._handle_key_event)

        self.curses_mouse_states = {
            GLXCurses.GLXC.BUTTON1_PRESSED: "BUTTON1_PRESS",
            GLXCurses.GLXC.BUTTON1_RELEASED: "BUTTON1_RELEASED",
            GLXCurses.GLXC.BUTTON1_CLICKED: "BUTTON1_CLICKED",
            GLXCurses.GLXC.BUTTON1_DOUBLE_CLICKED: "BUTTON1_DOUBLE_CLICKED",
            GLXCurses.GLXC.BUTTON1_TRIPLE_CLICKED: "BUTTON1_TRIPLE_CLICKED",
            GLXCurses.GLXC.BUTTON2_PRESSED: "BUTTON2_PRESSED",
            GLXCurses.GLXC.BUTTON2_RELEASED: "BUTTON2_RELEASED",
            GLXCurses.GLXC.BUTTON2_CLICKED: "BUTTON2_CLICKED",
            GLXCurses.GLXC.BUTTON2_DOUBLE_CLICKED: "BUTTON2_DOUBLE_CLICKED",
            GLXCurses.GLXC.BUTTON2_TRIPLE_CLICKED: "BUTTON2_TRIPLE_CLICKED",
            GLXCurses.GLXC.BUTTON3_PRESSED: "BUTTON3_PRESSED",
            GLXCurses.GLXC.BUTTON3_RELEASED: "BUTTON3_RELEASED",
            GLXCurses.GLXC.BUTTON3_CLICKED: "BUTTON3_CLICKED",
            GLXCurses.GLXC.BUTTON3_DOUBLE_CLICKED: "BUTTON3_DOUBLE_CLICKED",
            GLXCurses.GLXC.BUTTON3_TRIPLE_CLICKED: "BUTTON3_TRIPLE_CLICKED",
            GLXCurses.GLXC.BUTTON4_PRESSED: "BUTTON4_PRESSED",
            GLXCurses.GLXC.BUTTON4_RELEASED: "BUTTON4_RELEASED",
            GLXCurses.GLXC.BUTTON4_CLICKED: "BUTTON4_CLICKED",
            GLXCurses.GLXC.BUTTON4_DOUBLE_CLICKED: "BUTTON4_DOUBLE_CLICKED",
            GLXCurses.GLXC.BUTTON4_TRIPLE_CLICKED: "BUTTON4_TRIPLE_CLICKED",
            GLXCurses.GLXC.BUTTON_SHIFT: "BUTTON_SHIFT",
            GLXCurses.GLXC.BUTTON_CTRL: "BUTTON_CTRL",
            GLXCurses.GLXC.BUTTON_ALT: "BUTTON_ALT",
        }

    @property
    def accel_path(self):
        """
        Sets the accelerator path of the menu item, through which runtime changes of the menu
        item's accelerator caused by the user can be identified and saved to persistant storage.

        Default value: NULL

        :return: The accelerator path of the menu item
        :rtype: str
        """
        return self.__accel_path

    @accel_path.setter
    def accel_path(self, accel_path=None):
        """
        Set the ``label`` property value

        :param accel_path:
        :type: str or None
        """
        if accel_path is not None and type(accel_path) != str:
            raise TypeError('"accel_path" property value must be a str type or None')
        if self.accel_path != accel_path:
            self.__accel_path = accel_path

    @property
    def label(self):
        """
        The text for the child label.

        Default value: ""

        :return: child label
        :rtype: str
        :raise TypeError: When ``label`` property value is not str type or None
        """
        return self.__label

    @label.setter
    def label(self, label=None):
        """
        Set the ``label`` property value

        :param label:
        :type: str or None
        """
        if label is not None and type(label) != str:
            raise TypeError('"label" property value must be a str type or None')
        if self.label != label:
            self.__label = label
            self._update_sizes()

    @property
    def right_justified(self):
        """
        Sets whether the menu item appears justified at the right side of a menu bar.

        Default value: ``False``

        :return: ``True`` if the widget appears justified at the right side of a menu bar
        :rtype: bool
        """
        return self.__right_justified

    @right_justified.setter
    def right_justified(self, right_justified=False):
        """
        Sets whether the menu item appears justified at the right side of a menu bar.

        :param right_justified: The value to set to ``right_justified`` property
        :type right_justified: bool
        :raise TypeError: if ``right_justified`` is not a bool type or None
        """
        if right_justified is None:
            right_justified = False
        if type(right_justified) != bool:
            raise TypeError("'right_justified' property value must be a bool type")

        if self.right_justified != right_justified:
            self.__right_justified = right_justified

    @property
    def text_short_cut(self):
        return self.__text_short_cut

    @text_short_cut.setter
    def text_short_cut(self, text=None):
        if text is not None and type(text) != str:
            raise TypeError('"text" must be a str type or None')
        if self.text_short_cut != text:
            self.__text_short_cut = text
            self._update_sizes()

    @property
    def spacing(self):
        return self.__spacing

    @spacing.setter
    def spacing(self, spacing=None):
        if spacing is not None and type(spacing) != int:
            raise TypeError('"spacing" must be a int type or None')
        if self.spacing != GLXCurses.clamp_to_zero(spacing):
            self.__spacing = GLXCurses.clamp_to_zero(spacing)
            self._update_sizes()

    @property
    def resized_text(self):
        return GLXCurses.resize_text(self.label, self.width - (self.spacing * 2), "~")

    @property
    def resized_text_short_cut(self):
        return GLXCurses.resize_text(
            self.text_short_cut,
            self.width
            - 1
            - len(self.resized_text)
            + self.accelerator_size
            - (self.spacing * 2),
            "~",
        )

    @property
    def is_accel(self):
        return self.__is_accel

    @is_accel.setter
    def is_accel(self, value=None):
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"value" must be a bool type or None')
        if self.is_accel != value:
            self.__is_accel = value

    @property
    def accelerator_size(self):
        return self.__have_cross_a_accel

    @accelerator_size.setter
    def accelerator_size(self, value=None):
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError('"value" must be a int type or None')
        if self.accelerator_size != value:
            self.__have_cross_a_accel = value

    @property
    def color(self):
        if self.is_accel:
            self.__is_accel = False
            if self.has_default:
                return self.style.color(fg=(255, 255, 0), bg=(0, 0, 0), attributes=False)
            return self.style.color(fg=(255, 255, 0), bg=(0, 255, 255), attributes=False)
        else:
            if self.has_default:
                return self.style.color(bg=(0, 0, 0), fg=(180, 180, 180))
            return self.style.color(bg=(255, 255, 255), fg=(0, 255, 255), attributes=False) | A_REVERSE

    def draw(self):
        self._update_sizes()
        self.draw_background(color=self.color)

        pos = 0
        if self.spacing:
            self.add_character(y=0, x=pos, character=" ", color=self.color)
            pos += 1

        if self.label:
            self.accelerator_size = 0
            for x_inc in range(0, len(self.resized_text)):
                if self.resized_text[x_inc] == "_":
                    self.is_accel = True
                    self.accelerator_size += 1
                    continue

                self.add_character(
                    y=0,
                    x=pos + x_inc - self.accelerator_size,
                    character=self.resized_text[x_inc],
                    color=self.color,
                )

        if self.text_short_cut:
            self.add_string(
                y=0,
                x=self.width - self.spacing - len(self.resized_text_short_cut),
                text=self.resized_text_short_cut,
                color=self.color,
            )

    def _update_sizes(self):
        self.height = 1
        self.preferred_height = 1

        self.preferred_width = 0
        if self.spacing and self.text_short_cut:
            self.preferred_width += self.spacing
        if self.label:
            self.preferred_width += len(self.label)
        if self.text_short_cut:
            if self.spacing:
                self.preferred_width += self.spacing * 3
            self.preferred_width += len(self.text_short_cut)
        if self.spacing and self.text_short_cut:
            self.preferred_width += self.spacing

    def _handle_mouse_event(self, event_signal, event_args):
        if self.sensitive and self.can_focus:
            (mouse_event_id, x, y, z, event) = event_args
            # Be sure we select really the Button
            y -= self.y
            x -= self.x
            if 0 <= y <= self.height - 1:
                if 0 <= x <= self.x + self.width - 1:
                    # We are sure about the ToolBar have been clicked

                    if event == curses.BUTTON1_PRESSED:
                        if self.can_prelight:
                            self.emit("CLAIM_PRELIGHT", {"class": self.__class__.__name__, "id": self.id})
                        if self.can_default:
                            self.emit("CLAIM_DEFAULT", {"class": self.__class__.__name__, "id": self.id})
                        self.emit("button-pressed-event", {"class": self.__class__.__name__, "id": self.id})
                    elif event == curses.BUTTON1_RELEASED:
                        self.emit("button-release-event", {"class": self.__class__.__name__, "id": self.id})
                        if self.can_prelight:
                            self.emit("RELEASE_PRELIGHT", {"class": self.__class__.__name__, "id": self.id})
                        if self.can_default:
                            self.emit("RELEASE_DEFAULT", {"class": self.__class__.__name__, "id": self.id})
                        if GLXCurses.application.toolbar:
                            self.emit(
                                "grab-focus", {"class": self.__class__.__name__, "id": GLXCurses.application.toolbar.id}
                            )
                    if event == curses.BUTTON1_CLICKED:
                        self.emit("button-clicked-event", {"class": self.__class__.__name__, "id": self.id})

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
        import curses

        if self.sensitive and self.can_default and self.can_prelight:
            # setting
            key = event_args[0]
            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:
                self.selected_menu = 0
                self.selected_menu_item = 0
                self.emit("RELEASE_PRELIGHT", {"class": self.__class__.__name__, "id": self.id})
                self.emit("RELEASE_FOCUS", {"class": self.__class__.__name__, "id": self.id})
                self.emit("RELEASE_DEFAULT", {"class": self.__class__.__name__, "id": self.id})

            if key == KEY_ENTER or key == ord("\n"):
                self.selected_menu = 0
                self.selected_menu_item = 0

                self.emit("button-pressed-event", {"class": self.__class__.__name__, "id": self.id})
                self.emit("button-release-event", {"class": self.__class__.__name__, "id": self.id})
                self.emit("RELEASE_PRELIGHT", {"class": self.__class__.__name__, "id": self.id})

                self.emit("RELEASE_DEFAULT", {"class": self.__class__.__name__, "id": self.id})

                if GLXCurses.application.toolbar:
                    self.emit(
                        "grab-focus", {"class": self.__class__.__name__, "id": GLXCurses.application.toolbar.id}
                    )
