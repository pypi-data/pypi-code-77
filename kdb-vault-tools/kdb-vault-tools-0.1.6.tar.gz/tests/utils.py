import io

from pykeepass import PyKeePass, create_database
from pykeepass.entry import Entry
from pykeepass.group import Group


def create_kdb(password: str = "test123") -> PyKeePass:
    file = io.BytesIO()
    return create_database(filename=file, password=password)


def create_kdb_group(
    kdb: PyKeePass,
    group_name: str,
    parent_group: Group = None,
    icon: str = "1",
) -> Group:
    if not parent_group:
        parent_group = kdb.root_group
    return kdb.add_group(
        destination_group=parent_group, group_name=group_name, icon=icon
    )


def create_kdb_entry(
    kdb: PyKeePass, parent_group: Group = None, **kwargs
) -> Entry:
    if not parent_group:
        parent_group = kdb.root_group
    return kdb.add_entry(destination_group=parent_group, **kwargs)
