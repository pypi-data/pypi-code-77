import GLXCurses


class MenuShell(GLXCurses.Container):
    def __init__(self):
        GLXCurses.Container.__init__(self)

        self.__take_focus = None

        self.take_focus = None

    @property
    def take_focus(self):
        return self.__take_focus

    @take_focus.setter
    def take_focus(self, take_focus=True):
        if take_focus is None:
            take_focus = True
        if type(take_focus) != bool:
            raise TypeError("'take_focus' property value must be a bool type or None")
        if self.take_focus != take_focus:
            self.__take_focus = take_focus

    def append(self, child=None):
        """
        Adds a new ``GLXCurses.MenuItem`` to the end of the menu shell's item list.

        :return: A new ``GLXCurses.MenuItem`` to add
        :type menu_shell: GLXCurses.MenuItem
        """
        if not isinstance(child, GLXCurses.Widget):
            raise TypeError("'widget' must be an instance of GLXCurses.Widget")

        # If we are here everything look ok
        if bool(self.child):
            if callable(getattr(self.child.widget, "unparent")):
                self.child.widget.unparent()

        # The added widget receive a parent
        child.parent = self
        child.stdscr = GLXCurses.Application().stdscr

        self.child = GLXCurses.ChildElement(
            widget=child,
            widget_name=child.name,
            widget_type=child.glxc_type,
            widget_id=child.id,
            widget_properties=GLXCurses.ChildProperty(position=0),
        )

        self.emit("add", {"widget": self.child.widget, "id": self.child.id})
