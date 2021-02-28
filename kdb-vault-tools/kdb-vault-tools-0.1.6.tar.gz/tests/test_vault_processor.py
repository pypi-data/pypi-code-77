from unittest import TestCase

from hvac.exceptions import InvalidPath

from kdb_vault_tools.datatypes.basic import BaseEntry, BaseGroup
from kdb_vault_tools.exceptions import VaultConnectionError
from kdb_vault_tools.processors import VaultProcessor


class TestVaultFeature(TestCase):
    def setUp(self):
        self.vault_config = {"token": "myroot", "url": "http://127.0.0.1:1234"}
        self.processor = VaultProcessor()
        self.processor.vault_connect(**self.vault_config)

    def test_connection(self):
        try:
            self.processor.vault_connect()
            raise Exception("Failed")
        except VaultConnectionError as err:
            self.assertEqual(str(err), "Vault not Configured")

        self.processor.vault_connect(**self.vault_config)
        self.assertTrue(self.processor.vault.is_authenticated())

    def _test_write_secret(self, entry, base_path="/"):
        self.processor.write_secret(entry=entry, base_path=base_path)
        secret_full_path = f"{base_path}{entry.path}"
        resp = self.processor.vault.secrets.kv.v2.read_secret_version(
            path=secret_full_path
        )
        data = resp["data"]["data"]
        expected_data = entry.as_dict()
        expected_data.pop("path")
        expected_data.pop("title")
        self.assertEqual(
            data,
            expected_data,
        )

    def test_write_secret(self):
        entry = BaseEntry(
            title="root secret",
            password="root",
            icon="1",
            path="root_secret",
            url="",
            meta={"foo": "bar"},
            username="odin",
        )
        self._test_write_secret(entry)
        entry.title = "root2"
        self._test_write_secret(entry, "/foo/bar/baz/")
        entry.title = "root3"
        self._test_write_secret(entry, "/foo/bar/baz/")
        entry.title = "root4"
        self._test_write_secret(entry, "/foo/")
        try:
            self._test_write_secret(entry, "/foo/   ")
        except InvalidPath:
            pass

    def _test_write_group(self, group, base_path="/"):
        self.processor.write_group(group, base_path=base_path)
        group_meta_full_path = (
            f"{base_path}{group.path}/{self.processor.group_meta_label}"
        )
        resp = self.processor.vault.secrets.kv.v2.read_secret_version(
            path=group_meta_full_path
        )
        data = resp["data"]["data"]
        expected_data = group.as_dict()
        expected_data.pop("path")
        expected_data.pop("title")
        self.assertEqual(
            data,
            expected_data,
        )

    def test_write_group(self):
        entry = BaseGroup(
            title="root_group",
            icon="42",
            path="root_group",
        )
        self._test_write_group(entry)
        self._test_write_group(entry, "/main_group/")
        self._test_write_group(entry, "/main_group/sub/")
        self._test_write_group(entry, "/main_group/sub/sub/")

    def test_read_secret(self):
        entry = BaseEntry(
            title="test_read",
            password="root",
            icon="1",
            path="test_read",
            url="",
            meta={"foo": "bar"},
            username="odin",
        )
        self.processor.write_secret(entry)
        self.processor.read_secret(f"/{entry.path}")
        self.assertEqual(self.processor.kdb_entries[""][0], entry)

    def test_read_secrets(self):
        base_path = "test/recursive/read/"

        group_entry = BaseGroup(
            title="root_group",
            icon="42",
            path=f"{base_path}root_group",
        )

        secret_entry = BaseEntry(
            title="test_entry",
            password="root",
            icon="1",
            path=f"{base_path}root_group/test_entry",
            url="",
            meta={"foo": "bar"},
            username="odin",
        )

        self.processor.write_group(group=group_entry)
        self.processor.write_secret(entry=secret_entry)
        self.processor.read_secrets(path=f"/{base_path}", recursive=True)

        self.assertEqual(
            self.processor.kdb_groups[group_entry.path], group_entry
        )
        self.assertEqual(
            self.processor.kdb_entries[group_entry.path][0], secret_entry
        )

    def test_build_vault(self):
        base_path = "test/recursive/build/"

        group_entry = BaseGroup(
            title="root_group",
            icon="42",
            path=f"{base_path}root_group",
        )

        secret_entry = BaseEntry(
            title="test_entry",
            password="root",
            icon="1",
            path=f"{base_path}root_group/test_entry",
            url="",
            meta={"foo": "bar"},
            username="odin",
        )
        self.processor.kdb_entries[group_entry.path] = [
            secret_entry,
        ]
        self.processor.kdb_groups[group_entry.path] = group_entry

        self.processor.build_vault()

        # TODO DRY
        resp = self.processor.vault.secrets.kv.v2.read_secret_version(
            path=f"{group_entry.path}/{self.processor.group_meta_label}"
        )
        data = resp["data"]["data"]
        expected_data = group_entry.as_dict()
        expected_data.pop("path")
        expected_data.pop("title")
        self.assertEqual(
            data,
            expected_data,
        )

        resp = self.processor.vault.secrets.kv.v2.read_secret_version(
            path=f"{group_entry.path}/{secret_entry.title}"
        )
        data = resp["data"]["data"]
        expected_data = secret_entry.as_dict()
        expected_data.pop("path")
        expected_data.pop("title")
        self.assertEqual(
            data,
            expected_data,
        )
