import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class ChatOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chat_id: uuid.UUID
    chat_type: str
    created_at: datetime
    status: str

class MessageIn(BaseModel):
    chat_id: uuid.UUID
    text: str = Field(min_length=1, max_length=4000)

class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message_id: uuid.UUID
    chat_id: uuid.UUID
    sender: uuid.UUID
    text: str
    sent_at: datetime

class RequestIn(BaseModel):
    reason: str = Field(min_length=1)
    description: str = Field(min_length=1)
    operation_id: uuid.UUID | None = Field(None, description="Если оспаривается операция")

class RequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    request_id: uuid.UUID
    operation_id: uuid.UUID | None = None
    reason: str
    description: str
    status: str
    created_at: datetime
    closed_at: datetime | None = None

class FaqOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    faq_id: uuid.UUID
    question: str
    answer: str
    category: str
