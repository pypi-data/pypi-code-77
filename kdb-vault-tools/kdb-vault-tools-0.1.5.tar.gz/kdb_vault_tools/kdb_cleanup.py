import json

from pykeepass import PyKeePass
import random

from kdb_vault_tools.datatypes.basic import BaseEntry
from kdb_vault_tools.processors import KDBProcessor, VaultProcessor, Processor


def reset_passwords_all(kdb: PyKeePass, force: bool = True):

    if not force:
        return

    for entry in kdb.entries:
        # print(entry, dir(entry))
        entry.password = str(random.randint(10000, 9999999))
        e = BaseEntry.from_kdb_entry(entry)

        # print(json.dumps(e, cls=EnhancedJSONEncoder))
        print(e.dump_json())


def save_kdb_as_file(kdb: PyKeePass):
    kdb_map = {}
    for entry in kdb.entries:
        e = BaseEntry.from_kdb_entry(entry)
        kdb_map[e.path] = e.as_dict()

    with open("kdb_tmp/nc-tech-sl-20190422.json", "w") as fh:
        json.dump(kdb_map, fh)


def lad_kdb_from_file():
    with open("kdb_tmp/nc-tech-sl-20190422.json", "r") as fh:
        kdb_map = json.load(fh)

    entryes = []

    # kdb = create_database('kdb_tmp/db.kdbx', password='somePassw0rd')
    kdb = PyKeePass("blank_database.kdbx", "password")
    kdb.filename = "kdb_tmp/db.kdbx"
    kdb.password = "somePassw0rd"
    kdb.keyfile = None
    # kdb.version = KDB_VERSION
    # kdb.kdbx.header.value.minor_version = 1
    # kdb.kdbx.header.value.major_version = 3
    kdb.save()
    # print(kdb.kdbx.header)
    print(kdb.version, "VERSION")
    for k, v in kdb_map.items():
        e = BaseEntry(**v)
        entry_path = k.split("/")[:-1]
        print(entry_path)
        kdb_group = kdb.find_groups(path=entry_path, first=True)
        if kdb_group:
            print(f" OK GROUP EXIST {kdb_group}")
        else:
            base_grp = kdb.root_group
            base_grp_path = []
            for grp in entry_path:
                base_grp_path.append(grp)
                new_grp = kdb.find_groups(path=base_grp_path, first=True)

                if not new_grp:
                    print(f"CREATING FROUP {grp}")
                    base_grp = kdb.add_group(base_grp, grp)
                else:
                    base_grp = new_grp

                kdb_group = base_grp

        entry = kdb.find_entries(
            title=e.title, group=kdb_group, recursive=False, first=True
        )

        if entry:
            print("update")  # NOT POSSIBLE
        else:
            print("add entry")
            e_ = kdb.add_entry(
                kdb_group,
                title=e.title,
                username=e.username or "",
                notes=e.dump_notes(e.meta),
                icon=e.icon,
                password=e.password,
                url=e.url or "",
            )
            # e_.mtime = e.misc.ts.m_date_time
            # e_.ctime = e.misc.ts.c_date_time
            # e_.atime = e.misc.ts.a_date_time

    kdb.save()

    print(entryes)


def main(db: str, password: str):
    # kp = PyKeePass(db, password=password)
    # print(kp.version, "VERSION")
    kdb_pr = KDBProcessor()
    kdb_pr.load_from_kdb(db, password)
    # print(kdb_pr.kdb_groups)
    # print(kdb_pr.kdb_entries)
    #
    # kdb_pr.__kdb = PyKeePass("kdb_tmp/nc-tech-sl-test.kdbx", password=password)

    vault = VaultProcessor()
    vault.vault_connect(url="http://localhost:1234", token="myroot")

    base_path = "/sandbox/namecheap/TOST/sl_kdb"

    for k, v in kdb_pr.kdb_groups.items():
        vault.write_group(v, base_path=base_path)

    for k, v in kdb_pr.kdb_entries.items():
        for i in v:
            vault.write_secret(i, base_path=base_path)

    vault.read_secrets()
    kdb_pr.kdb_entries = vault.kdb_entries
    kdb_pr.kdb_groups = vault.kdb_groups

    filename = "kdb_tmp/db_vault.kdbx"
    password = "123"
    kdb_pr.build_kdb(filename, password)

    # reset_passwords_all(kp, True)
    # save_kdb_as_file(kp)
    # lad_kdb_from_file()
    # kp.password = "nhjkbtkbvskj"
    # kp.save()


def main2():

    vault_conf = {"url": "http://localhost:1234", "token": "myroot"}
    kdb_conf = {"filename": "kdb_tmp/db_vault.kdbx", "password": "123"}

    processor = Processor(vault_settings=vault_conf, kdb_settings=kdb_conf)
    processor.sync_from_vault()
    processor.write_kdb()


def main3():
    vault_conf = {"url": "http://localhost:1234", "token": "myroot"}
    kdb_conf = {
        "filename": "kdb_tmp/nc-tech-sl-20190422.kdbx",
        "password": "nhjkbtkbvskj",
    }

    processor = Processor(vault_settings=vault_conf, kdb_settings=kdb_conf)
    processor.sync_from_kdb()
    processor.write_vault(base_path="/sandbox/namecheap/TOST/sl_kdb/")


def reset():
    file = input("File Location")
    save_as = input("Save as")
    password = input("Password")
    kdb = PyKeePass(filename=file, password=password)
    reset_passwords_all(kdb, True)
    kdb.password = "123"
    kdb.save(save_as)


if __name__ == "__main__":
    # main3()
    main2()
    # main("kdb_tmp/nc-tech-sl-20190422.kdbx", "nhjkbtkbvskj")
    # reset()
