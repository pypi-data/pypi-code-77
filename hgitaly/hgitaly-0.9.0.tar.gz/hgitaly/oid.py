# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from base64 import (
    b64encode,
    b64decode,
)


def concat_chgsid_path(changeset_id, path):
    return changeset_id + b64encode(path).decode('ascii')


def split_chgsid_path(oid):
    return oid[:40], b64decode(oid[40:])


def tree_oid(repo, changeset_id: str, path: bytes):
    return concat_chgsid_path(changeset_id, path)


def blob_oid(repo, changeset_id, path):
    return concat_chgsid_path(changeset_id, path)


def extract_tree_oid(repo, oid: str) -> (str, bytes):
    """"Return changeset id and path for a tree OID.

    Changeset ID is given in hexadecimal form.
    """
    return split_chgsid_path(oid)


def extract_blob_oid(repo, oid: str) -> (str, bytes):
    """Return changeset ID and path for a blob OID.

    Changeset ID is given in hexadecimal form.

    Examples:

    """
    return split_chgsid_path(oid)
