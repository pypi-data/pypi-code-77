from chameleongram.raw.tl_base import TL
from chameleongram.raw.primitives import *
from typing import Any, List
from io import BytesIO


class FileUnknown(TL):
    ID = 0xaa963b05

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FileUnknown":
        
        return FileUnknown()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FilePartial(TL):
    ID = 0x40bc6f52

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FilePartial":
        
        return FilePartial()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FileJpeg(TL):
    ID = 0x7efe0e

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FileJpeg":
        
        return FileJpeg()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FileGif(TL):
    ID = 0xcae1aadf

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FileGif":
        
        return FileGif()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FilePng(TL):
    ID = 0xa4f63c0

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FilePng":
        
        return FilePng()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FilePdf(TL):
    ID = 0xae1e508d

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FilePdf":
        
        return FilePdf()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FileMp3(TL):
    ID = 0x528a0677

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FileMp3":
        
        return FileMp3()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FileMov(TL):
    ID = 0x4b09ebbc

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FileMov":
        
        return FileMov()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FileMp4(TL):
    ID = 0xb3cea0e4

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FileMp4":
        
        return FileMp4()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()


class FileWebp(TL):
    ID = 0x1081464c

    def __init__(cls, ):
        ...

    @staticmethod
    def read(data) -> "FileWebp":
        
        return FileWebp()

    def getvalue(cls) -> bytes:
        data = BytesIO()
        data.write(Int.getvalue(cls.ID, False))
        
        return data.getvalue()
