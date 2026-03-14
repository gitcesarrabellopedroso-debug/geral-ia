from typing import Any

from bson import ObjectId
from pydantic import BaseModel, ConfigDict


class APIModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        json_encoders={ObjectId: str},
    )


def serialize_mongo_document(document: dict[str, Any]) -> dict[str, Any]:
    if not document:
        return {}

    payload = dict(document)
    payload["id"] = str(payload.pop("_id"))
    return payload
