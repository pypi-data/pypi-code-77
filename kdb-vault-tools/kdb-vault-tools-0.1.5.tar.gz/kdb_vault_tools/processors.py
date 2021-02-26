import logging
import os
import sys
from copy import copy
from typing import Type, List

import hvac
from hvac import exceptions as vault_errors
from pykeepass import PyKeePass, create_database
from pykeepass.entry import Entry
from pykeepass.group import Group


from kdb_vault_tools.datatypes.basic import BaseEntry, BaseGroup
from kdb_vault_tools.exceptions import EntryBuildError, VaultConnectionError

logger = logging.getLogger(__package__)
logger.level = logging.DEBUG

# TODO Configure logger
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class KDBProcessor:

    kdb_entries: dict
    kdb_groups: dict

    __blank_kdb_file = "blank_database.kdbx"
    __blank_kdb_file_password = "password"
    __tmd_kdb: PyKeePass

    def exception_handler(self, exception: Exception):
        pass

    def __init__(self, *args, **kwargs):
        self.kdb_entries = {}
        self.kdb_groups = {}

    def init_kdb_connection(self):
        pass

    def load_from_kdb(self, filename: str, password: str):
        self.__tmd_kdb = PyKeePass(filename=filename, password=password)
        self._load_groups_from_kdb()

    def _load_group_from_kdb(self, group: Group, load_entries=True):
        g = BaseGroup.from_kdb_entry(group)
        self.kdb_groups[g.path] = g

        if group.entries and load_entries:
            self._load_entries_from_kdb(group.entries)

    def _load_groups_from_kdb(self):
        for entry in self.kdb.groups:
            self._load_group_from_kdb(entry)

    def _load_entry_from_kdb(self, entry: Entry):
        e = BaseEntry.from_kdb_entry(entry)
        self.kdb_entries.setdefault(e.group_path, []).append(e)

    def _load_entries_from_kdb(self, entries: Type[List[Entry]] = None):
        entries = entries or self.kdb.entries
        for entry in entries:
            self._load_entry_from_kdb(entry)

    def build_kdb(self, filename: str, password: str):
        self._build_from_blank(filename, password)
        self._save_groups_to_kdb()
        self._save_entries_to_kdb()
        if hasattr(self.kdb.filename, "seek"):
            self.kdb.filename.seek(0)
        self.kdb.save()

    def _build_from_blank(self, filename, password):
        if self.__blank_kdb_file and os.path.isfile(self.__blank_kdb_file):
            kdb = PyKeePass(self.__blank_kdb_file, self.__blank_kdb_file_password)
            kdb.filename = filename
            kdb.password = password
            kdb.keyfile = None
        else:
            kdb = create_database(filename, password)

        self.__tmd_kdb = kdb

    def _save_groups_to_kdb(self):
        for g in self.kdb_groups.keys():
            try:
                self._kdb_group_get_or_create(g)
            except EntryBuildError as err:
                logger.exception(f"Group was not created {err}")
                continue

    def _save_entries_to_kdb(self):
        for p, entry_list in self.kdb_entries.items():
            try:
                kdb_group = self._kdb_group_get_or_create(p)
            except EntryBuildError as err:
                logger.exception("Group was not created")
                continue

            for e in entry_list:
                logger.debug(f"Adding entry {e.title} to group {p}")
                try:
                    self.kdb.add_entry(
                        kdb_group,
                        title=e.title,
                        username=e.username or "",
                        notes=e.dump_notes(e.meta),
                        icon=e.icon,
                        password=e.password,
                        url=e.url or "",
                    )
                except Exception as err:
                    logger.error(f"Error while adding entry {e} {err}")
                    self.exception_handler(exception=err)

    def _kdb_group_get_or_create(self, path: str) -> Group:
        parent_group = self.kdb.root_group

        if path != "":
            _path = path.split("/")
            for i in range(len(_path)):
                c_path = _path[: i + 1]
                try:
                    group = self.kdb.find_groups(path=c_path, first=True)
                except Exception as err:
                    raise EntryBuildError(
                        f"Fail while processing group {c_path} result: {group}"
                    ) from err

                logger.debug(f"Find group {c_path} result: {group}")
                if not group:
                    j_c_path = "/".join(c_path)
                    l_group = self.kdb_groups.get(j_c_path)
                    icon = l_group.icon if l_group else None
                    group = self.kdb.add_group(
                        parent_group, group_name=_path[i], icon=icon
                    )
                parent_group = group
        return parent_group

    @property
    def kdb(self) -> PyKeePass:
        return self.__tmd_kdb


class VaultProcessor:

    kdb_entries: dict
    kdb_groups: dict

    __tmd_vault: hvac.Client
    __g_meta_label: str = "__META"

    def __init__(self, *args, **kwargs):
        self.kdb_entries = {}
        self.kdb_groups = {}

    def vault_connect(self, **kwargs):

        self._setup_connection(**kwargs)

        if not self.vault.is_authenticated():
            raise VaultConnectionError("Vault not Configured")

    def _setup_connection(self, **kwargs):
        ldap_config = kwargs.pop("ldap_config", None)

        self.__tmd_vault = hvac.Client(**kwargs)

        if ldap_config:
            self.__tmd_vault.ldap.login(
                **ldap_config
            )

    def read_secret(self, path: str):
        try:
            resp_ = self.vault.secrets.kv.v2.read_secret_version(path=path)
        except vault_errors.Forbidden as err:
            logger.debug(f"Failed to read secret {path} - {err}")
            return
        data = resp_.get("data", {}).get("data")
        path_ = copy(path).lstrip("/")
        g_path, title = path_.rsplit("/", 1) if "/" in path_ else ["", path_]

        if title == self.__g_meta_label:
            group = BaseGroup(title=title, path=g_path, **data)
            self.kdb_groups[g_path] = group
        else:
            try:
                entry = BaseEntry(**data, path=path_, title=title)
                self.kdb_entries.setdefault(g_path, []).append(
                    entry
                )  # TOdO make method move to mixin
            except TypeError as err:
                logger.info(
                    f"Secret configured improperly {err} {data} {path_} {title}"
                )

    def write_secret(self, entry: BaseEntry, base_path="/"):
        data = entry.as_dict()
        data.pop("title", None)
        path = base_path + data.pop("path")
        path = path.encode("utf-8").decode("utf-8", "ignore").strip()
        try:
            self.vault.secrets.kv.create_or_update_secret(
                path=path,
                secret=data,
            )
        except vault_errors.InvalidRequest as err:
            log_data = copy(data)
            log_data["password"] = "******"
            logger.exception(
                f"Cant write secret '{err}', path: '{path}' data: '{log_data}''"
            )

    def write_group(self, group: BaseGroup, base_path="/"):
        data = group.as_dict()
        data.pop("title")
        path = base_path + data.pop("path") + "/" + self.__g_meta_label

        self.vault.secrets.kv.create_or_update_secret(
            path=path,
            secret=data,
        )

    def read_secrets(self, path="/", recursive=True):

        if not path.endswith("/"):
            return self.read_secret(path)

        resp_ = self.vault.secrets.kv.v2.list_secrets(path=path)

        data = resp_.get("data")
        keys = data.get("keys")
        if recursive and keys:
            for k in keys:
                self.read_secrets(path=path + k)

    def build_vault(self, base_path="/"):
        for k, v in self.kdb_groups.items():
            self.write_group(v, base_path=base_path)

        for k, v in self.kdb_entries.items():
            for i in v:
                self.write_secret(i, base_path=base_path)

    @property
    def vault(self) -> hvac.Client:
        return self.__tmd_vault


class Processor:

    kdb_entries: dict
    kdb_groups: dict

    _kdb_processor = KDBProcessor()
    _vault_processor = VaultProcessor()

    _kdb_settings: dict
    _vault_settings: dict

    def __init__(self, vault_settings: dict, kdb_settings: dict):
        self.kdb_entries = {}
        self.kdb_groups = {}
        self._vault_processor.kdb_entries = (
            self._kdb_processor.kdb_entries
        ) = self.kdb_entries
        self._vault_processor.kdb_groups = (
            self._kdb_processor.kdb_groups
        ) = self.kdb_groups
        self._vault_settings = vault_settings
        self._kdb_settings = kdb_settings

    def sync_from_vault(self):
        self._vault_processor.vault_connect(**self._vault_settings)
        self._vault_processor.read_secrets("/")

    def write_vault(self, base_path="/"):
        self._vault_processor.vault_connect(**self._vault_settings)
        self._vault_processor.build_vault(base_path=base_path)

    def write_kdb(self):
        self._kdb_processor.build_kdb(**self._kdb_settings)

    def sync_from_kdb(self):
        self._kdb_processor.load_from_kdb(**self._kdb_settings)
