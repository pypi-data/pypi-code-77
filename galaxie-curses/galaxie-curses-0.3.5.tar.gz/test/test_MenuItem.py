import unittest
import GLXCurses


class TestMenuItem(unittest.TestCase):
    def setUp(self) -> None:
        self.menu_item = GLXCurses.MenuItem()

    def test_label(self):
        self.assertIsNone(self.menu_item.label)
        self.menu_item.label = "Hello.42"
        self.assertEqual("Hello.42", self.menu_item.label)
        self.menu_item.label = None
        self.assertIsNone(self.menu_item.label)

        self.assertRaises(TypeError, setattr, self.menu_item, "label", 42)

    def test_right_justified(self):
        self.menu_item.right_justified = None
        self.assertFalse(self.menu_item.right_justified)
        self.menu_item.right_justified = True
        self.assertTrue(self.menu_item.right_justified)
        self.menu_item.right_justified = False
        self.assertFalse(self.menu_item.right_justified)

        self.assertRaises(TypeError, setattr, self.menu_item, "right_justified", 42)

    def test_text_short_cut(self):
        self.assertIsNone(self.menu_item.text_short_cut)
        self.menu_item.text_short_cut = "Hello.42"
        self.assertEqual("Hello.42", self.menu_item.text_short_cut)
        self.menu_item.text_short_cut = None
        self.assertIsNone(self.menu_item.text_short_cut)

        self.assertRaises(TypeError, setattr, self.menu_item, "text_short_cut", 42)

    def test_spacing(self):
        self.assertEqual(1, self.menu_item.spacing)

        self.menu_item.text = None
        self.assertEqual(1, self.menu_item.spacing)

        self.menu_item.spacing = 42
        self.assertEqual(42, self.menu_item.spacing)

        self.menu_item.spacing = -42
        self.assertEqual(0, self.menu_item.spacing)

        self.assertRaises(TypeError, setattr, self.menu_item, "spacing", "Hello.42")

    def test__update_preferred_sizes(self):
        self.assertEqual(0, self.menu_item.preferred_width)
        self.assertEqual(1, self.menu_item.preferred_height)

        self.menu_item._update_sizes()
        self.assertEqual(0, self.menu_item.preferred_width)
        self.assertEqual(1, self.menu_item.preferred_height)

        self.menu_item.label = "Hello"
        self.menu_item._update_sizes()
        self.assertEqual(5, self.menu_item.preferred_width)

        self.menu_item.spacing = 1
        self.menu_item._update_sizes()
        self.assertEqual(5, self.menu_item.preferred_width)

        self.menu_item.text_short_cut = "42"
        self.menu_item._update_sizes()
        self.assertEqual(12, self.menu_item.preferred_width)

    def test_draw(self):
        app = GLXCurses.Application()
        win = GLXCurses.Window()

        win.add(self.menu_item)
        app.add_window(win)
        app.refresh()


if __name__ == "__main__":
    unittest.main()
