import unittest
import os
from GLXCurses.libs.FileChooserFunctions import FileChooserUtils
from random import randint
from uuid import uuid4
from time import sleep


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.filechooser_utils = FileChooserUtils()
        self.cwd = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "libs/filechooser"
        )
        for file in ["file_1", "file_2", "file_3", "file_4", "file_5", "file_6"]:
            try:
                os.remove(os.path.join(self.cwd, file))
            except FileNotFoundError:
                pass
        for directory in ["directory_1", "directory_2"]:
            try:
                os.rmdir(os.path.join(self.cwd, directory))
            except FileNotFoundError:
                pass
        try:
            os.rmdir(self.cwd)
        except FileNotFoundError:
            pass

    def doCleanups(self) -> None:
        for file in ["file_1", "file_2", "file_3", "file_4", "file_5", "file_6"]:
            try:
                os.remove(os.path.join(self.cwd, file))
            except FileNotFoundError:
                pass
        for directory in ["directory_1", "directory_2"]:
            try:
                os.rmdir(os.path.join(self.cwd, directory))
            except FileNotFoundError:
                pass
        try:
            os.rmdir(self.cwd)
        except FileNotFoundError:
            pass

    def test_directory_view(self):
        self.assertEqual([], self.filechooser_utils.directory_view)
        self.filechooser_utils.directory_view = ['Hello', '42']
        self.assertEqual(['Hello', '42'], self.filechooser_utils.directory_view)

        self.assertRaises(TypeError, setattr, self.filechooser_utils, 'directory_view', 42)

    def test_cwd(self):
        self.assertTrue(type(self.filechooser_utils.cwd) == str)
        self.assertTrue(os.path.isdir(self.filechooser_utils.cwd))
        self.filechooser_utils.cwd = os.getcwd()
        self.assertEqual(os.getcwd(), self.filechooser_utils.cwd)

        self.assertRaises(TypeError, setattr, self.filechooser_utils, 'cwd', 42)
        self.assertRaises(ValueError, setattr, self.filechooser_utils, 'cwd', os.path.join(os.getcwd(), 'Hello.42'))

    def test_sort_by_name(self):
        self.filechooser_utils.sort_by_name = True
        self.assertTrue(self.filechooser_utils.sort_by_name)
        self.filechooser_utils.sort_by_name = False
        self.assertFalse(self.filechooser_utils.sort_by_name)
        self.filechooser_utils.sort_by_name = None
        self.assertFalse(self.filechooser_utils.sort_by_name)
        self.assertRaises(TypeError, setattr, self.filechooser_utils, 'sort_by_name', 42)

    def test_sort_name_order(self):
        self.filechooser_utils.sort_by_name = True
        self.assertTrue(self.filechooser_utils.sort_name_order)
        self.filechooser_utils.sort_name_order = False
        self.assertFalse(self.filechooser_utils.sort_name_order)
        self.filechooser_utils.sort_name_order = None
        self.assertFalse(self.filechooser_utils.sort_name_order)
        self.assertRaises(TypeError, setattr, self.filechooser_utils, 'sort_name_order', 42)

    def test_sort_by_size(self):
        self.filechooser_utils.sort_by_size = True
        self.assertTrue(self.filechooser_utils.sort_by_size)
        self.filechooser_utils.sort_by_size = False
        self.assertFalse(self.filechooser_utils.sort_by_size)
        self.filechooser_utils.sort_by_size = None
        self.assertFalse(self.filechooser_utils.sort_by_size)
        self.assertRaises(TypeError, setattr, self.filechooser_utils, 'sort_by_size', 42)

    def test_sort_size_order(self):
        self.filechooser_utils.sort_size_order = True
        self.assertTrue(self.filechooser_utils.sort_size_order)
        self.filechooser_utils.sort_size_order = False
        self.assertFalse(self.filechooser_utils.sort_size_order)
        self.filechooser_utils.sort_size_order = None
        self.assertFalse(self.filechooser_utils.sort_size_order)
        self.assertRaises(TypeError, setattr, self.filechooser_utils, 'sort_size_order', 42)

    def test_sort_by_mtime(self):
        self.filechooser_utils.sort_by_mtime = True
        self.assertTrue(self.filechooser_utils.sort_by_mtime)
        self.filechooser_utils.sort_by_mtime = False
        self.assertFalse(self.filechooser_utils.sort_by_mtime)
        self.filechooser_utils.sort_by_mtime = None
        self.assertFalse(self.filechooser_utils.sort_by_mtime)
        self.assertRaises(TypeError, setattr, self.filechooser_utils, 'sort_by_mtime', 42)

    def test_sort_mtime_order(self):
        self.filechooser_utils.sort_mtime_order = True
        self.assertTrue(self.filechooser_utils.sort_mtime_order)
        self.filechooser_utils.sort_mtime_order = False
        self.assertFalse(self.filechooser_utils.sort_mtime_order)
        self.filechooser_utils.sort_mtime_order = None
        self.assertFalse(self.filechooser_utils.sort_mtime_order)
        self.assertRaises(TypeError, setattr, self.filechooser_utils, 'sort_mtime_order', 42)

    def test_convert_truck(self):
        self.filechooser_utils.convert_file_attribute()
        # print(self.filechooser_utils.convert_file_attribute())
        # self.assertEqual("", self.filechooser_utils.convert_file_attribute())

    def test_update_directory_list(self):
        os.mkdir(self.cwd)
        for directory in ["directory_1", "directory_2"]:
            os.mkdir(os.path.join(self.cwd, directory))
        for file in ["file_1", "file_2", "file_3", "file_4", "file_tmp"]:
            sleep(randint(1, 3))
            with open(os.path.join(self.cwd, file), "w") as file_object:

                if file == "file_1":
                    min = 1
                    max = 10
                if file == "file_2":
                    min = 111
                    max = 120
                if file == "file_3":
                    min = 1121
                    max = 1130
                if file == "file_4":
                    min = 11131
                    max = 11140
                if file == "file_tmp":
                    min = 111131
                    max = 111140
                for _ in range(0, randint(min, max)):
                    file_object.write("{0}\n".format(uuid4()))

        os.link(os.path.join(self.cwd, 'file_4'), os.path.join(self.cwd, 'file_5'))
        os.link(os.path.join(self.cwd, 'file_tmp'), os.path.join(self.cwd, 'file_6'))

        try:
            os.remove(os.path.join(self.cwd, 'file_tmp'))
        except FileNotFoundError:
            pass

        filechooser_utils = FileChooserUtils()
        filechooser_utils.cwd = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "libs/filechooser"
        )

        filechooser_utils.sort_by_name = True
        filechooser_utils.sort_name_order = True
        filechooser_utils.sort_by_size = False
        filechooser_utils.sort_size_order = False
        filechooser_utils.sort_by_mtime = False
        filechooser_utils.sort_mtime_order = False
        filechooser_utils.update_directory_list()

        # print("Short by name")
        # for item in filechooser_utils.directory_view:
        #     print("|{3}{0:<30} | {1:<8} | {2:<10}|".format(item['to_display_name'],
        #                                                    item['to_display_size'],
        #                                                    item['to_display_mtime'],
        #                                                    item['to_display_symbol'],
        #                                                    ))

        self.assertEqual("..", filechooser_utils.directory_view[0]["name"])
        self.assertEqual("directory_1", filechooser_utils.directory_view[1]["name"])
        self.assertEqual("directory_2", filechooser_utils.directory_view[2]["name"])
        self.assertEqual("file_1", filechooser_utils.directory_view[3]["name"])
        self.assertEqual("file_2", filechooser_utils.directory_view[4]["name"])
        self.assertEqual("file_3", filechooser_utils.directory_view[5]["name"])
        self.assertEqual("file_4", filechooser_utils.directory_view[6]["name"])

        filechooser_utils.sort_by_name = True
        filechooser_utils.sort_name_order = False
        filechooser_utils.sort_by_size = False
        filechooser_utils.sort_size_order = False
        filechooser_utils.sort_by_mtime = False
        filechooser_utils.sort_mtime_order = False
        filechooser_utils.update_directory_list()

        # print("Short by name reverted")
        # for item in filechooser_utils.directory_view:
        #     print("|{3}{0:<30} | {1:<8} | {2:<10}|".format(item['to_display_name'],
        #                                                    item['to_display_size'],
        #                                                    item['to_display_mtime'],
        #                                                    item['to_display_symbol'],
        #                                                    ))

        self.assertEqual("..", filechooser_utils.directory_view[0]["name"])
        self.assertEqual("directory_2", filechooser_utils.directory_view[1]["name"])
        self.assertEqual("directory_1", filechooser_utils.directory_view[2]["name"])
        self.assertEqual("file_6", filechooser_utils.directory_view[3]["name"])
        self.assertEqual("file_5", filechooser_utils.directory_view[4]["name"])
        self.assertEqual("file_4", filechooser_utils.directory_view[5]["name"])
        self.assertEqual("file_3", filechooser_utils.directory_view[6]["name"])

        filechooser_utils.sort_by_name = False
        filechooser_utils.sort_name_order = False
        filechooser_utils.sort_by_size = True
        filechooser_utils.sort_size_order = True
        filechooser_utils.sort_by_mtime = False
        filechooser_utils.sort_mtime_order = False
        filechooser_utils.update_directory_list()

        # print("Short by size")
        # for item in filechooser_utils.directory_view:
        #     print("|{3}{0:<30} | {1:<8} | {2:<10}|".format(item['to_display_name'],
        #                                                    item['to_display_size'],
        #                                                    item['to_display_mtime'],
        #                                                    item['to_display_symbol'],
        #                                                    ))

        self.assertEqual("..", filechooser_utils.directory_view[0]["name"])
        self.assertEqual("directory_2", filechooser_utils.directory_view[1]["name"])
        self.assertEqual("directory_1", filechooser_utils.directory_view[2]["name"])
        self.assertEqual("file_1", filechooser_utils.directory_view[3]["name"])
        self.assertEqual("file_2", filechooser_utils.directory_view[4]["name"])
        self.assertEqual("file_3", filechooser_utils.directory_view[5]["name"])
        # self.assertEqual("file_6", filechooser_utils.directory_view[6]["name"])

        filechooser_utils.sort_by_name = False
        filechooser_utils.sort_name_order = False
        filechooser_utils.sort_by_size = True
        filechooser_utils.sort_size_order = False
        filechooser_utils.sort_by_mtime = False
        filechooser_utils.sort_mtime_order = False
        filechooser_utils.update_directory_list()

        # print("Short by size reverted")
        # for item in filechooser_utils.directory_view:
        #     print("|{3}{0:<30} | {1:<8} | {2:<10}|".format(item['to_display_name'],
        #                                                    item['to_display_size'],
        #                                                    item['to_display_mtime'],
        #                                                    item['to_display_symbol'],
        #                                                    ))

        self.assertEqual("..", filechooser_utils.directory_view[0]["name"])
        self.assertEqual("directory_1", filechooser_utils.directory_view[1]["name"])
        self.assertEqual("directory_2", filechooser_utils.directory_view[2]["name"])
        self.assertEqual("file_6", filechooser_utils.directory_view[3]["name"])
        # self.assertEqual("file_5", filechooser_utils.directory_view[4]["name"])
        # self.assertEqual("file_4", filechooser_utils.directory_view[5]["name"])
        self.assertEqual("file_3", filechooser_utils.directory_view[6]["name"])

        filechooser_utils.sort_by_name = False
        filechooser_utils.sort_name_order = False
        filechooser_utils.sort_by_size = False
        filechooser_utils.sort_size_order = False
        filechooser_utils.sort_by_mtime = True
        filechooser_utils.sort_mtime_order = True
        filechooser_utils.update_directory_list()

        # print("Short by time ")
        # for item in filechooser_utils.directory_view:
        #     print("|{3}{0:<30} | {1:<8} | {2:<10}|".format(item['to_display_name'],
        #                                                    item['to_display_size'],
        #                                                    item['to_display_mtime'],
        #                                                    item['to_display_symbol'],
        #                                                    ))

        self.assertEqual("..", filechooser_utils.directory_view[0]["name"])
        self.assertEqual("directory_2", filechooser_utils.directory_view[1]["name"])
        self.assertEqual("directory_1", filechooser_utils.directory_view[2]["name"])
        self.assertEqual("file_1", filechooser_utils.directory_view[3]["name"])
        self.assertEqual("file_2", filechooser_utils.directory_view[4]["name"])
        self.assertEqual("file_3", filechooser_utils.directory_view[5]["name"])
        # self.assertEqual("file_4", filechooser_utils.directory_view[6]["name"])

        filechooser_utils.sort_by_name = False
        filechooser_utils.sort_name_order = False
        filechooser_utils.sort_by_size = False
        filechooser_utils.sort_size_order = False
        filechooser_utils.sort_by_mtime = True
        filechooser_utils.sort_mtime_order = False
        filechooser_utils.update_directory_list()

        # print("Short by time reverted")
        # for item in filechooser_utils.directory_view:
        #     print("|{3}{0:<30} | {1:<8} | {2:<10}|".format(item['to_display_name'],
        #                                                    item['to_display_size'],
        #                                                    item['to_display_mtime'],
        #                                                    item['to_display_symbol'],
        #                                                    ))

        self.assertEqual("..", filechooser_utils.directory_view[0]["name"])
        self.assertEqual("directory_1", filechooser_utils.directory_view[1]["name"])
        self.assertEqual("directory_2", filechooser_utils.directory_view[2]["name"])
        self.assertEqual("file_6", filechooser_utils.directory_view[3]["name"])
        # self.assertEqual("file_5", filechooser_utils.directory_view[4]["name"])
        # self.assertEqual("file_4", filechooser_utils.directory_view[5]["name"])
        # self.assertEqual("file_3", filechooser_utils.directory_view[6]["name"])

        # self.assertEqual(0, filechooser_utils.update_directory_list())

    # def test_utils_get_file_info_list(self):
    #     """Test Utils get_file_info_list"""
    # filechooser = GLXCurses.FileSelect()
    # # ['.', '.', 4096, '29/01/2019  01:52', 4096, 1548723122.4803152]
    # self.assertEqual(list, type(filechooser.get_file_info_list('.')))
    # self.assertEqual(9, len(filechooser.get_file_info_list('.')))
    # self.assertEqual(str, type(filechooser.get_file_info_list('.')[0]))
    # self.assertEqual(str, type(filechooser.get_file_info_list('.')[1]))
    # self.assertEqual(int, type(filechooser.get_file_info_list('.')[2]))
    # self.assertEqual(str, type(filechooser.get_file_info_list('.')[3]))
    # self.assertEqual(int, type(filechooser.get_file_info_list('.')[4]))
    # self.assertEqual(float, type(filechooser.get_file_info_list('.')[5]))
    #
    # self.assertEqual("UP--DIR", filechooser.get_file_info_list('..')[2])
    #
    # #self.assertRaises(FileNotFoundError, filechooser.get_file_info_list, '42')
    # self.assertRaises(TypeError, filechooser.get_file_info_list, None)


if __name__ == "__main__":
    unittest.main()
