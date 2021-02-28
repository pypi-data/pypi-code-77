from unittest import TestCase

from kdb_vault_tools.datatypes.basic import BaseEntry, BaseGroup

from .utils import create_kdb, create_kdb_entry, create_kdb_group


class TestBaseGroup(TestCase):
    def setUp(self):
        self.entry = BaseGroup(title="test", path="/", icon="1")
        self.kdb = create_kdb()

    def test_creation(self):

        group = self.entry
        self.assertEqual(group.path, "/")
        self.assertEqual(group.title, "test")
        self.assertEqual(group.icon, "1")

    def test_to_dict(self):
        dict_group = self.entry.as_dict()

        self.assertIsInstance(dict_group, dict)
        self.assertEqual(
            dict_group, {"path": "/", "title": "test", "icon": "1"}
        )

    def _test_entry(self, group_name, icon, expected_path, parent_group=None):
        kdb_group = create_kdb_group(
            self.kdb,
            group_name=group_name,
            icon=icon,
            parent_group=parent_group,
        )
        group = BaseGroup.from_kdb_entry(kdb_group)
        dict_group = group.as_dict()
        self.assertEqual(
            dict_group,
            {"path": expected_path, "title": group_name, "icon": icon},
        )
        return kdb_group

    def test_from_kdb_entry(self):
        group = self._test_entry("test", "1", "test")
        group2 = self._test_entry("1", "2", "test/1", parent_group=group)
        self._test_entry("sub_sub", "3", "test/1/sub_sub", parent_group=group2)


class TestBaseEntry(TestCase):
    def setUp(self):
        self.entry = BaseEntry(
            title="test",
            path="/",
            icon="1",
            password="test123",
            url="https://127.0.0.1/",
            meta={"key": "value"},
            username="tester",
        )
        self.kdb = create_kdb()

    def test_creation(self):

        entry = self.entry
        self.assertEqual(entry.path, "/")
        self.assertEqual(entry.title, "test")
        self.assertEqual(entry.icon, "1")
        self.assertEqual(entry.password, "test123")
        self.assertEqual(entry.url, "https://127.0.0.1/")
        self.assertEqual(entry.username, "tester")
        self.assertEqual(entry.meta, {"key": "value"})

    def test_to_dict(self):
        entry = self.entry.as_dict()

        self.assertIsInstance(entry, dict)
        self.assertEqual(
            entry,
            {
                "path": "/",
                "title": "test",
                "icon": "1",
                "password": "test123",
                "url": "https://127.0.0.1/",
                "username": "tester",
                "meta": {"key": "value"},
            },
        )

    def _test_entry(
        self,
        entry_name,
        icon,
        expected_path,
        parent_group=None,
        group_name=None,
    ):

        if group_name:
            kdb_group = create_kdb_group(
                self.kdb,
                group_name=group_name,
                icon=icon,
                parent_group=parent_group or self.kdb.root_group,
            )
        elif parent_group:
            kdb_group = parent_group
        else:
            kdb_group = self.kdb.root_group

        entry_data = {
            "title": entry_name,
            "icon": icon,
            "password": "test123",
            "url": "https://127.0.0.1/",
            "username": "tester",
            "notes": "FOO: bar\n Baz Fuz",
        }
        kdb_entry = create_kdb_entry(
            self.kdb, parent_group=kdb_group, **entry_data
        )
        base_entry = BaseEntry.from_kdb_entry(kdb_entry)
        dict_entry = base_entry.as_dict()
        self.assertEqual(
            dict_entry,
            {
                "path": expected_path,
                "title": entry_name,
                "icon": icon,
                "password": "test123",
                "url": "https://127.0.0.1/",
                "username": "tester",
                "meta": {"FOO": "bar", "": "BazFuz"},
            },
        )
        return kdb_group, kdb_entry

    def test_from_kdb_entry(self):
        self._test_entry("test1", "1", "test1")
        group, _ = self._test_entry(
            "test2", "1", "foo/test2", group_name="foo"
        )
        _, entry = self._test_entry(
            "test3", "1", "foo/bar/test3", parent_group=group, group_name="bar"
        )

        base_entry = BaseEntry.from_kdb_entry(entry)
        self.assertEqual(base_entry.group_path, "foo/bar")

    def test_json_dump(self):
        entry = BaseEntry(
            title="test",
            password="123",
            url="https://1.tld",
            username="",
            path="",
            icon=None,
            meta={},
        )
        json_payload = entry.dump_json(indent=3)
        self.assertEqual(
            json_payload,
            '{\n   "title": "test",\n   "path": "",\n   "password": "123",\n   '
            '"meta": {},\n   "icon": null,\n   "username": "",\n   "url": "https://1.tld"\n}',
        )

    def test_parse_notes(self):
        notes = "test: 123"
        parsed = BaseEntry.parse_notes(notes)

        self.assertEqual(parsed, {"test": "123"})

        notes = "test: 123\nSome data here\n"
        parsed = BaseEntry.parse_notes(notes)
        self.assertEqual(parsed, {"test": "123", "Some": "datahere", "": ""})

        notes = ""
        parsed = BaseEntry.parse_notes(notes)
        self.assertEqual(parsed, {})

    def test_dump_notes(self):
        meta = {"Foo": "Bar", "Baz": {"Nested": "Not Supported yet"}}
        notes = BaseEntry.dump_notes(meta)
        self.assertEqual(
            notes, "Foo: Bar\nBaz: {'Nested': 'Not Supported yet'}"
        )
