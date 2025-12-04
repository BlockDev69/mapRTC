from pydantic import BaseModel, field_serializer
from uuid import UUID

class Session(BaseModel):
    user_id: UUID
    is_anonymous: bool = True

    @field_serializer('user_id')
    def serialize_user_id(self, value: UUID) -> str:
        return str(value)
