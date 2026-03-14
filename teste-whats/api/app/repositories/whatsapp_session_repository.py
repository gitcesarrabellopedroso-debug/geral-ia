from datetime import datetime, timezone

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from app.schemas.common import serialize_mongo_document
from app.schemas.whatsapp_session import WhatsAppSessionCreate, WhatsAppSessionUpdate


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class WhatsAppSessionRepository:
    def __init__(self, database) -> None:
        self.collection = database["whatsapp_sessions"]

    async def create(self, payload: WhatsAppSessionCreate) -> dict:
        now = utc_now()
        document = {
            **payload.model_dump(),
            "created_at": now,
            "updated_at": now,
        }

        try:
            result = await self.collection.insert_one(document)
        except DuplicateKeyError as exc:
            raise ValueError("A session with this key already exists.") from exc

        created = await self.collection.find_one({"_id": result.inserted_id})
        return serialize_mongo_document(created)

    async def list(self, skip: int = 0, limit: int = 20) -> tuple[list[dict], int]:
        cursor = (
            self.collection.find({})
            .sort("updated_at", -1)
            .skip(skip)
            .limit(limit)
        )
        items = [serialize_mongo_document(item) async for item in cursor]
        total = await self.collection.count_documents({})
        return items, total

    async def get_by_session_key(self, session_key: str) -> dict | None:
        document = await self.collection.find_one({"session_key": session_key})
        if not document:
            return None
        return serialize_mongo_document(document)

    async def get(self, session_id: str) -> dict | None:
        document = await self.collection.find_one({"_id": ObjectId(session_id)})
        if not document:
            return None
        return serialize_mongo_document(document)

    async def upsert_by_session_key(self, session_key: str, payload: dict) -> dict:
        payload = {
            **payload,
            "session_key": session_key,
            "updated_at": utc_now(),
        }

        result = await self.collection.find_one_and_update(
            {"session_key": session_key},
            {
                "$set": payload,
                "$setOnInsert": {"created_at": utc_now()},
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        return serialize_mongo_document(result)

    async def update(self, session_id: str, payload: WhatsAppSessionUpdate) -> dict | None:
        update_fields = payload.model_dump(exclude_none=True)

        if not update_fields:
            return await self.get(session_id)

        update_fields["updated_at"] = utc_now()
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(session_id)},
            {"$set": update_fields},
            return_document=ReturnDocument.AFTER,
        )

        if not result:
            return None

        return serialize_mongo_document(result)

    async def delete(self, session_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(session_id)})
        return result.deleted_count > 0
