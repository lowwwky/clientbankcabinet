import uuid
from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, computed_field


class ClientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    client_id: uuid.UUID
    last_name: str
    first_name: str
    middle_name: str | None = None
    birth_date: date
    phone: str
    email: str | None = None
    avatar_url: str | None = None

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        had_birthday = (today.month, today.day) >= (self.birth_date.month, self.birth_date.day)
        return today.year - self.birth_date.year - (0 if had_birthday else 1)


class ContactsUpdate(BaseModel):
    phone: str | None = Field(None, pattern=r"^\+?\d{10,15}$")
    email: EmailStr | None = None


class UpdateAvatar(BaseModel):
    avatar_url: str = Field(min_length=1, max_length=500)

class DocumentIn(BaseModel):
    document_type: str = Field(max_length=200)
    series: str = Field(max_length=20)
    number: str = Field(max_length=20)
    issue_date: date
    issued_by: str = Field(max_length=300)


class DocumentOut(DocumentIn):
    model_config = ConfigDict(from_attributes=True)

    document_id: uuid.UUID
    client_id: uuid.UUID


class DocumentUpdate(BaseModel):
    document_type: str | None = Field(default=None, min_length=1, max_length=200)
    series: str | None = Field(default=None, min_length=1, max_length=20)
    number: str | None = Field(default=None, min_length=1, max_length=20)
    issue_date: date | None = None
    issued_by: str | None = Field(default=None, min_length=1, max_length=300)


class RelationIn(BaseModel):
    related_client_id: UUID
    related_type: Literal["Родитель", "Ребёнок"]


class RelationOut(RelationIn):
    model_config = ConfigDict(from_attributes=True)

    relation_id: UUID
    client_id: UUID