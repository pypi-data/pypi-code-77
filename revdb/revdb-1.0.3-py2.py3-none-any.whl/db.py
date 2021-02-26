from typing import Any, Dict, Type, TypeVar

import requests
from mongoengine import Document, DynamicDocument
from mongoengine import connect as mongo_connect  # ignore: type
from mongoengine.base import BaseDocument

URLS_V1 = {
    "stg": "https://jstorage-stg.revtel-api.com/v1/settings",
    "prod": "https://jstorage.revtel-api.com/v1/settings",
}

URLS_V2 = {
    "stg": "https://jstorage-stg.revtel-api.com/v2/settings",
    "prod": "https://jstorage.revtel-api.com/v2/settings",
}


def connect(api_key: str, stage: str = "stg", alias: str = "default") -> None:
    try:
        url = URLS_V1[stage]
    except KeyError as e:
        raise ValueError("stage should be in [stg, prod]") from e

    resp = requests.get(
        url, headers={"Content-Type": "application/json", "x-api-key": api_key}
    )
    resp.raise_for_status()

    resp_json = resp.json()
    mongo_connect(resp_json["id"], host=resp_json["db_host"], alias=alias)


def connect_v2(client_secret: str, stage: str = "stg", alias: str = "default") -> None:
    try:
        url = URLS_V2[stage]
    except KeyError as e:
        raise ValueError("stage should be in [stg, prod]") from e

    full_url = f"{url}?client_secret={client_secret}"
    resp = requests.get(full_url)
    resp.raise_for_status()

    resp_json = resp.json()

    mongo_connect(resp_json["id"], host=resp_json["db_host"], alias=alias)


DOC = TypeVar("DOC", bound=BaseDocument)


def make_model_class(base: Type[DOC], **meta: Any) -> Type[DOC]:
    return type(base.__name__, (base,), {"meta": meta})


def create_connected_model(
    doc_class: BaseDocument, client_id: str, host: str, **kwargs: Any
) -> BaseDocument:
    db = client_id
    alias = f"{db}_alias"
    mongo_connect(db, host=host, alias=alias)
    return make_model_class(doc_class, db_alias=alias, **kwargs)


class ModelMixin:
    _meta: Dict[str, Any]

    @classmethod
    def from_client(cls, client_id: str) -> BaseDocument:
        db_host = cls._meta.get("db_host")
        if not db_host:
            raise ValueError("should define db_host in meta")

        return create_connected_model(
            cls,
            host=db_host,
            client_id=client_id,
        )


class Model(ModelMixin, DynamicDocument):  # type: ignore
    meta: Dict[str, Any] = {"abstract": True}


class StrictModel(ModelMixin, Document):  # type: ignore
    meta: Dict[str, Any] = {"abstract": True}
