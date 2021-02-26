from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

AtomicType = str
Type = Union[AtomicType, 'ListType', 'SetType', 'MapType', 'ReferenceType']


@dataclass()
class ListType:
    valueType: Type


@dataclass()
class SetType:
    valueType: Type


@dataclass()
class MapType:
    keyType: Type
    valueType: Type


@dataclass()
class ReferenceType:
    module: str
    name: str


@dataclass()
class Namespace:
    name: str
    language: str


@dataclass()
class EnumMember:
    name: str
    value: int
    doc: str = ''


@dataclass()
class Enum:
    name: str
    members: List[EnumMember]
    doc: str = ''


@dataclass()
class Typedef:
    name: str
    type_: Type
    doc: str = ''


@dataclass()
class Field:
    key: int
    name: str
    type_: Type
    required: str = 'required'
    doc: str = ''
    default: Optional[Any] = None
    type: Optional[Any] = None


@dataclass()
class Struct:
    name: str
    isException: bool
    isUnion: bool
    fields: List[Field]
    doc: str = ''


@dataclass()
class Constant:
    name: str
    type_: Type
    value: Any
    doc: str = ''


@dataclass()
class Function:
    name: str
    oneway: bool
    returnType: Type
    arguments: List[Field]
    exceptions: List[Field]
    doc: str = ''


@dataclass()
class Service:
    name: str
    functions: List[Function]
    doc: str = ''


@dataclass()
class Module:
    name: str
    namespaces: List[Namespace]
    enums: List[Enum]
    typedefs: List[Typedef]
    structs: List[Struct]
    constants: List[Constant]
    services: List[Service]
    doc: str = ''
