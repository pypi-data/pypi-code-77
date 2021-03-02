import unittest
import GLXCurses


class TestMenuBar(unittest.TestCase):
    def setUp(self) -> None:
        self.menu_shell = GLXCurses.MenuShell()

    def test_take_focus(self):
        self.menu_shell.take_focus = False
        self.assertFalse(self.menu_shell.take_focus)
        self.menu_shell.take_focus = True
        self.assertTrue(self.menu_shell.take_focus)
        self.menu_shell.take_focus = None
        self.menu_shell.take_focus = False
        self.assertRaises(TypeError, setattr, self.menu_shell, 'take_focus', 42)


if __name__ == "__main__":
    unittest.main()
