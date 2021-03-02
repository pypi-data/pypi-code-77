from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class EditPeerFolders(TL):
    ID = 0x6847d0ab

    def __init__(cls, folder_peers: List[TL]):
        cls.folder_peers = folder_peers

    @staticmethod
    def read(data) -> "EditPeerFolders":
        folder_peers = data.getobj()
        return EditPeerFolders(folder_peers=folder_peers)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Vector().getvalue(cls.folder_peers))
        return data.getvalue()


class DeleteFolder(TL):
    ID = 0x1c295881

    def __init__(cls, folder_id: int):
        cls.folder_id = folder_id

    @staticmethod
    def read(data) -> "DeleteFolder":
        folder_id = Int.read(data)
        return DeleteFolder(folder_id=folder_id)

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        data.write(Int.getvalue(cls.folder_id))
        return data.getvalue()
