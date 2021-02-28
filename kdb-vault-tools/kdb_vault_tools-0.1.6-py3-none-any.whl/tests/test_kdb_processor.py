import io
import os
from unittest import TestCase

from pykeepass import PyKeePass
from pykeepass.group import Group

from kdb_vault_tools.datatypes.basic import BaseEntry, BaseGroup
from kdb_vault_tools.exceptions import EntryBuildError
from kdb_vault_tools.processors import KDBProcessor

from .utils import create_kdb, create_kdb_entry, create_kdb_group


class TestKDBFeature(TestCase):
    def setUp(self):
        self.password = "123456"
        kdb = create_kdb(password=self.password)
        entry_data = {
            "icon": "1",
            "password": "root",
            "url": "https://127.0.0.1/",
            "username": "tester",
            "notes": "",
        }
        create_kdb_entry(kdb, title="root_entry", **entry_data)
        kdb_sub_grp = create_kdb_group(kdb, group_name="sub")
        create_kdb_entry(
            kdb, title="sub_entry", **entry_data, parent_group=kdb_sub_grp
        )
        kdb_sub_sub_grp = create_kdb_group(
            kdb, group_name="subsub", parent_group=kdb_sub_grp
        )
        create_kdb_entry(
            kdb,
            title="sub_sub_entry",
            **entry_data,
            parent_group=kdb_sub_sub_grp,
        )
        self.raw_kdb_full_path = "/tmp/__test_kdb.kdbx"
        kdb.save(filename=self.raw_kdb_full_path)
        self.kdb = kdb
        self.processor = KDBProcessor()

    def tearDown(self):
        os.remove(self.raw_kdb_full_path)

    def test_creation(self):
        self.processor.load_from_kdb(self.raw_kdb_full_path, self.password)
        self.assertEqual(
            list(self.processor.kdb_entries.keys()), ["", "sub", "sub/subsub"]
        )
        self.assertEqual(
            list(self.processor.kdb_groups.keys()), ["", "sub", "sub/subsub"]
        )

    def test_build_kdb(self):
        file = self.raw_kdb_full_path
        self.processor.build_kdb(filename=file, password="123")

        kdb = PyKeePass(filename=file, password="123")
        entries = kdb.entries
        groups = kdb.groups
        self.assertEqual(len(entries), 0)
        self.assertEqual(len(groups), 1)

        kdb_io = io.BytesIO()
        self.kdb.save(kdb_io)
        kdb_io.seek(0)
        self.processor.load_from_kdb(kdb_io, self.password)
        self.processor.build_kdb(filename=file, password="123")

        kdb = PyKeePass(filename=file, password="123")
        entries = kdb.entries
        groups = kdb.groups
        self.assertEqual(3, len(entries))
        self.assertEqual(3, len(groups))

        # TODO DRY
        self.processor.build_kdb(filename=kdb_io, password="123")

        kdb = PyKeePass(filename=file, password="123")
        entries = kdb.entries
        groups = kdb.groups
        self.assertEqual(3, len(entries))
        self.assertEqual(3, len(groups))

    def test_load_entry(self):
        kdb_entry = self.kdb.entries[0]
        self.processor._load_entry_from_kdb(kdb_entry)
        self.assertTrue("" in self.processor.kdb_entries)
        self.assertEqual(len(self.processor.kdb_entries[""]), 1)
        entry = self.processor.kdb_entries[""][0]
        self.assertIsInstance(entry, BaseEntry)
        self.assertEqual(
            entry,
            BaseEntry(
                title="root_entry",
                username="tester",
                meta={},
                icon="1",
                password="root",
                url="https://127.0.0.1/",
                path="root_entry",
            ),
        )

    def test_load_group_from_kdb(self):
        kdb_entry = self.kdb.groups[0]
        self.processor._load_group_from_kdb(kdb_entry, load_entries=False)
        self.assertTrue("" in self.processor.kdb_groups)
        group = self.processor.kdb_groups[""]
        self.assertIsInstance(group, BaseGroup)
        self.assertEqual(group, BaseGroup(title="Root", icon="48", path=""))
        self.assertEqual(0, len(self.processor.kdb_entries.keys()))
        self.processor._load_group_from_kdb(kdb_entry, load_entries=True)
        self.assertEqual(group, BaseGroup(title="Root", icon="48", path=""))
        self.assertEqual(1, len(self.processor.kdb_entries.keys()))

    def test_exception_handler(self):
        exc = Exception("TEST")
        res = self.processor.exception_handler(exception=exc)
        self.assertIsNone(res)

    def test_init_kdb_connection(self):
        res = self.processor.init_kdb_connection()
        self.assertIsNone(res)

    def test_build_from_blank(self):

        processor = KDBProcessor()
        processor._blank_kdb_file = self.raw_kdb_full_path
        processor._blank_kdb_file_password = self.password
        processor._build_from_blank("Foo", "test123")

        entries = processor.kdb.entries
        groups = processor.kdb.groups
        self.assertEqual(3, len(entries))
        self.assertEqual(3, len(groups))

    def test_kdb_group_get_or_create(self):
        self.processor.load_from_kdb(self.raw_kdb_full_path, self.password)

        kdb_group = self.processor._kdb_group_get_or_create("sub/subsub")
        self.assertIsInstance(kdb_group, Group)
        self.assertEqual(kdb_group.path, ["sub", "subsub"])
        self.assertEqual(kdb_group.name, "subsub")
        self.assertEqual(kdb_group.icon, "1")

        self.processor.kdb_groups["sub/subsub/created"] = BaseGroup(
            path="sub/subsub/created",
            title="created",
            icon="42",
        )

        kdb_group = self.processor._kdb_group_get_or_create(
            "sub/subsub/created"
        )
        self.assertIsInstance(kdb_group, Group)
        self.assertEqual(kdb_group.path, ["sub", "subsub", "created"])
        self.assertEqual(kdb_group.name, "created")
        self.assertEqual(kdb_group.icon, "42")

    def test_save_groups_to_kdb(self):
        self.processor.load_from_kdb(self.raw_kdb_full_path, self.password)
        self.processor.kdb_groups[
            "sub/Foo][ \ 1 *8!@#$%^&*()/ [ subsub/created"
        ] = BaseGroup(
            path="sub/su/created",
            title="crea[ ']ted",
            icon="42",
        )
        self.processor._save_groups_to_kdb()

        self.assertFalse("crea[ ']ted" in self.kdb.groups)
        self.assertFalse("created" in self.kdb.groups)

    def test_exceptions_group_get_or_create(self):
        self.processor.load_from_kdb(self.raw_kdb_full_path, self.password)

        def _kdb_group_get_or_create(path):
            raise EntryBuildError(
                f"Fail while processing group {path} result: {None}"
            )

        self.processor._kdb_group_get_or_create = _kdb_group_get_or_create
        kdb_io = io.BytesIO()
        self.processor.build_kdb(kdb_io, password="123")
        kdb_io.seek(0)
        kdb = PyKeePass(kdb_io, password="123")

        self.assertEqual(len(kdb.entries), 0)
        self.assertEqual(len(kdb.groups), 1)
