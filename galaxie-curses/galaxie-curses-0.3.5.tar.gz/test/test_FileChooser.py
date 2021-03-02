import unittest
import os
import GLXCurses


class MyTestCase(unittest.TestCase):
    def tearDown(self):
        GLXCurses.Application().refresh()

    def setUp(self):
        self.win = GLXCurses.Window()
        self.filechooser = GLXCurses.FileSelect()
        GLXCurses.Application().add_window(self.win)
        self.win.add(self.filechooser)

    def test_FileChooser_draw_widget_in_area(self):
        # Main loop
        # filechooser.draw_widget_in_area()
        GLXCurses.Application().refresh()

    def test_sort_by_name(self):
        """Test FileChooser.set_sort_by_name()"""

        self.assertTrue(self.filechooser.sort_by_name)

        self.filechooser.sort_by_name = False
        self.assertFalse(self.filechooser.sort_by_name)

        self.filechooser.sort_by_name = True
        self.assertTrue(self.filechooser.sort_by_name)

        self.filechooser.sort_by_name = None
        self.assertFalse(self.filechooser.sort_by_name)

        self.assertRaises(
            TypeError, setattr, self.filechooser, "sort_by_name", "Hello.42"
        )

    def test_sort_name_order(self):
        self.assertTrue(self.filechooser.sort_name_order)

        self.filechooser.sort_name_order = False
        self.assertFalse(self.filechooser.sort_name_order)

        self.filechooser.sort_name_order = True
        self.assertTrue(self.filechooser.sort_name_order)

        self.filechooser.sort_name_order = None
        self.assertFalse(self.filechooser.sort_name_order)

        self.assertRaises(TypeError, setattr, self.filechooser, "sort_name_order", 42)

    def test_FileChooser_sort_by_size(self):
        self.assertFalse(self.filechooser.sort_by_size)

        self.filechooser.sort_by_size = True
        self.assertTrue(self.filechooser.sort_by_size)

        self.filechooser.sort_by_size = None
        self.assertFalse(self.filechooser.sort_by_size)

        self.assertRaises(TypeError, setattr, self.filechooser, "sort_by_size", 42)

    def test_FileChooser_sort_size_order(self):
        self.assertTrue(self.filechooser.sort_size_order)

        self.filechooser.sort_size_order = False
        self.assertFalse(self.filechooser.sort_size_order)

        self.filechooser.sort_size_order = True
        self.assertTrue(self.filechooser.sort_size_order)

        self.filechooser.sort_size_order = None
        self.assertFalse(self.filechooser.sort_size_order)

        self.assertRaises(TypeError, setattr, self.filechooser, "sort_size_order", 42)

    def test_FileChooser_sort_by_mtime(self):
        self.assertFalse(self.filechooser.sort_by_mtime)

        self.filechooser.sort_by_mtime = True
        self.assertTrue(self.filechooser.sort_by_mtime)

        self.filechooser.sort_by_mtime = None
        self.assertFalse(self.filechooser.sort_by_mtime)

        self.assertRaises(TypeError, setattr, self.filechooser, "sort_by_mtime", 42)

    def test_FileChooser_set_sort_mtime_order(self):
        self.assertTrue(self.filechooser.sort_mtime_order)

        self.filechooser.sort_mtime_order = False
        self.assertFalse(self.filechooser.sort_mtime_order)

        self.filechooser.sort_mtime_order = True
        self.assertTrue(self.filechooser.sort_mtime_order)

        self.filechooser.sort_mtime_order = None
        self.assertFalse(self.filechooser.sort_mtime_order)

        self.assertRaises(TypeError, setattr, self.filechooser, "sort_mtime_order", 42)

    def test_item_it_can_be_display(self):
        self.assertEqual(0, self.filechooser.item_it_can_be_display)
        self.filechooser.item_it_can_be_display = None
        self.assertEqual(0, self.filechooser.item_it_can_be_display)

        self.filechooser.item_it_can_be_display = 42
        self.assertEqual(42, self.filechooser.item_it_can_be_display)

        self.assertRaises(
            TypeError, setattr, self.filechooser, "item_it_can_be_display", "42"
        )

    def test_FileChooser__set_item_list_scroll(self):
        self.assertEqual(0, self.filechooser.item_scroll_pos)
        self.filechooser.item_scroll_pos = 42
        self.assertEqual(42, self.filechooser.item_scroll_pos)
        self.filechooser.item_scroll_pos = 0
        self.assertEqual(0, self.filechooser.item_scroll_pos)

        self.assertRaises(TypeError, setattr, self.filechooser, "item_scroll_pos", "42")

    def test_selected_item_pos(self):
        self.assertEqual(0, self.filechooser.selected_item_pos)
        self.filechooser.selected_item_pos = 42
        self.assertEqual(42, self.filechooser.selected_item_pos)
        self.filechooser.selected_item_pos = None
        self.assertEqual(0, self.filechooser.selected_item_pos)
        self.assertRaises(
            TypeError, setattr, self.filechooser, "selected_item_pos", "42"
        )


if __name__ == "__main__":
    unittest.main()
