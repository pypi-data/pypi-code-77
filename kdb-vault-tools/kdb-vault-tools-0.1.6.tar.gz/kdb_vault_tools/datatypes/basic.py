import dataclasses
import json
import os
from typing import Optional

from pykeepass.entry import Entry
from pykeepass.group import Group


@dataclasses.dataclass
class BaseGroup:
    title: str
    path: str
    icon: Optional[str]

    @classmethod
    def from_kdb_entry(cls, entry: Group):
        return cls(
            title=entry.name, path="/".join(entry.path), icon=entry.icon
        )

    def as_dict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class BaseEntry:
    title: str
    path: str
    password: str
    meta: Optional[dict]
    icon: Optional[str]
    username: str = ""
    url: str = ""

    @classmethod
    def from_kdb_entry(cls, entry: Entry):
        return cls(
            password=entry.password,
            url=entry.url,
            username=entry.username,
            # notes=entry.notes,
            path=os.path.join(*entry.path),
            title=entry.title,
            icon=entry.icon,
            meta=cls.parse_notes(entry.notes),
        )

    @staticmethod
    def parse_notes(notes: str) -> dict:
        # TODO use template lang
        meta = {}

        if not notes:
            return meta

        for line in notes.split("\n"):
            if ":" in line:
                key, *content = line.split(":", maxsplit=2)
            else:
                key, *content = line.split(" ", maxsplit=2)

            meta[key] = "".join(content).strip()

        return meta

    @staticmethod
    def dump_notes(meta: dict) -> str:
        notes = []

        for key, content in meta.items():
            notes.append(f"{key}: {content}")

        return "\n".join(notes)

    def dump_json(self, indent=None) -> str:
        return json.dumps(self.as_dict(), indent=indent)

    def as_dict(self) -> dict:
        return dataclasses.asdict(self)

    @property
    def group_path(self) -> str:
        return self.path.replace(self.title, "").rstrip("/")
