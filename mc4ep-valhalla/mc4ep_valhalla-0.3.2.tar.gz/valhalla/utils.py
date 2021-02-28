from enum import Enum
from io import BytesIO
from typing import Union, TypeVar, Any, Dict, Type

from PIL import Image
from nidhoggr.core.response import ErrorResponse, TextureStatusResponse
from pydantic import BaseModel, ValidationError
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from werkzeug.exceptions import InternalServerError, BadRequest

from valhalla.decorators import as_json_error
from sps_parser import parse_metadata, SkinMetadata

T = TypeVar("T")
U = TypeVar("U", bound=BaseModel)

ALLOWED_SIZES = {64, 128, 256, 512, 1024, 2048}


def handle_status(repository_response: Union[ErrorResponse, T]) -> T:
    if isinstance(repository_response, ErrorResponse):
        raise InternalServerError(description=repository_response.reason)
    return repository_response


@as_json_error
def error_handler(error: InternalServerError):
    return TextureStatusResponse(message=error.description)


def validate_image(*, data: bytes):
    with Image.open(BytesIO(data)) as image:
        if image.format != "PNG":
            raise BadRequest(description=f"Format not allowed: {image.format}")

        (width, height) = image.size
        valid = width / 2 == height or width == height

        if not valid or width not in ALLOWED_SIZES:
            raise BadRequest(description=f"Unsupported image size: {image.size}")


def extract_skin_metadata(*, data: bytes) -> Dict[str, str]:
    with Image.open(BytesIO(data)) as image:
        metadata: SkinMetadata = parse_metadata(image)

    # TODO: use custom serializer here
    return {
        key: value.name
        if isinstance(value, Enum) else value
        for key, value
        in metadata.__dict__.items()
    }


def cleanup_metadata(*, raw_metadata: Dict[Any, Any]) -> Dict[str, str]:
    return {
        key: value
        for key, value
        in raw_metadata.items()
        if isinstance(key, str) and isinstance(value, str)
    }


def validate_form(*, form: ImmutableMultiDict, clazz: Type[U]) -> Union[ErrorResponse, U]:
    try:
        return clazz.parse_obj(form.to_dict())
    except ValidationError as e:
        raise BadRequest(description=str(e))

