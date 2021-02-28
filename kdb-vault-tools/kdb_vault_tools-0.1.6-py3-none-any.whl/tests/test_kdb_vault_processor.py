import io
from unittest import TestCase

from pykeepass import PyKeePass

from kdb_vault_tools import Processor
from kdb_vault_tools.processors import KDBProcessor, VaultProcessor

from .utils import create_kdb, create_kdb_entry, create_kdb_group


class TestKDBVaultFeature(TestCase):
    def setUp(self):
        self.kdb_password = "test123"
        self.vault_config = {"token": "myroot", "url": "http://127.0.0.1:1234"}
        file_like = io.BytesIO()

        self.kdb = create_kdb(self.kdb_password)
        entry_data = {
            "icon": "1",
            "password": "root",
            "url": "https://127.0.0.1/",
            "username": "tester",
            "notes": "",
        }
        group = create_kdb_group(self.kdb, "test")
        group = create_kdb_group(self.kdb, "sub", parent_group=group)
        create_kdb_entry(
            self.kdb, parent_group=group, title="test_entry", **entry_data
        )
        self.kdb.save(file_like)
        file_like.seek(0)
        self.kdb_config = {
            "filename": file_like,
            "password": self.kdb_password,
        }

    def test_create(self):
        processor = Processor({"conf": 1}, {"conf": 2})
        self.assertIsInstance(processor._vault_processor, VaultProcessor)
        self.assertIsInstance(processor._kdb_processor, KDBProcessor)
        self.assertEqual(processor._kdb_settings["conf"], 2)
        self.assertEqual(processor._vault_settings["conf"], 1)

        self.assertTrue(
            processor.kdb_groups
            == processor._vault_processor.kdb_groups
            == processor._kdb_processor.kdb_groups
        )
        self.assertTrue(
            processor.kdb_entries
            == processor._vault_processor.kdb_entries
            == processor._kdb_processor.kdb_entries
        )

    def test_processor(self):
        processor = Processor(
            vault_settings=self.vault_config, kdb_settings=self.kdb_config
        )
        processor.sync_from_kdb()
        processor.sync_from_vault()
        processor.write_vault()
        file_like = io.BytesIO()
        processor._kdb_settings["filename"] = file_like
        processor.write_kdb()
        file_like.seek(0)
        kdb = PyKeePass(filename=file_like, password=self.kdb_password)
        entry = kdb.find_entries_by_title(title="test_entry", first=True)
        self.assertEqual(entry.path, ["test", "sub", "test_entry"])
