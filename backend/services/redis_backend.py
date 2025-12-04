from typing import Generic, Type, Optional
from redis.asyncio import Redis
from uuid import UUID

from fastapi_sessions.backends.session_backend import (
    BackendError,
    SessionBackend,
    SessionModel,
)
from fastapi_sessions.frontends.session_frontend import ID

from core.config import settings

class RedisBackend(Generic[ID, SessionModel], SessionBackend[ID, SessionModel]):
    def __init__(self, *, session_model: Type[SessionModel], redis: Redis, prefix: str = "session"):
        self._session_model = session_model
        self._redis = redis
        self._prefix = prefix

    @property
    def session_model(self) -> Type[SessionModel]:
        return self._session_model

    async def create(self, session_id: ID, session_data: SessionModel) -> None:
        key_id = str(session_id) if isinstance(session_id, UUID) else session_id
        key = f"{self._prefix}:{key_id}"
        await self._redis.set(key, session_data.model_dump_json())
        await self._redis.expire(key, settings.SESSION_EXPIRATION_SECONDS)

    async def read(self, session_id: ID) -> Optional[SessionModel]:
        key_id = str(session_id) if isinstance(session_id, UUID) else session_id
        key = f"{self._prefix}:{key_id}"
        data = await self._redis.get(key)
        if data is None:
            return None
        return self._session_model.model_validate_json(data)

    async def update(self, session_id: ID, session_data: SessionModel) -> None:
        key_id = str(session_id) if isinstance(session_id, UUID) else session_id
        key = f"{self._prefix}:{key_id}"
        exists = await self._redis.exists(key)
        if not exists:
            raise BackendError("Session does not exist")
        await self._redis.set(key, session_data.model_dump_json())
        await self._redis.expire(key, settings.SESSION_EXPIRATION_SECONDS)

    async def delete(self, session_id: ID) -> None:
        key_id = str(session_id) if isinstance(session_id, UUID) else session_id
        key = f"{self._prefix}:{key_id}"
        await self._redis.delete(key)