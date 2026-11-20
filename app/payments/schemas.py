import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TransferType = Literal[
    "по номеру телефона", "по номеру карты", "между своими счетами", "по реквизитам", "по номеру договора"
]

class TransferIn(BaseModel):
    transfer_type: TransferType
    source_account_id: uuid.UUID
    recipient: str = Field(min_length=1, max_length=500,
                           description="Телефон / номер карты / реквизиты / договор; для перевода между своими счетами — account_id счёта-получателя")
    recipient_bank: str | None = Field(None, max_length=1000, description="Обязателен, кроме перевода между своими счетами")
    recipient_name: str | None = Field(None, max_length=200)
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    message: str | None = None

class TransferOut(BaseModel):
    operation_id: uuid.UUID
    transfer_id: uuid.UUID
    status: str
    amount: Decimal
    source_account_id: uuid.UUID
    recipient: str
    recipient_bank: str
    transfer_type: str
    date: datetime
    message: str | None = None

class OperationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    operation_id: uuid.UUID
    source_account_id: uuid.UUID
    operation_type: str
    amount: Decimal
    date: datetime
    status: str
    description: str | None = None

class SummaryOut(BaseModel):
    year: int
    month: int
    income: Decimal
    expenses: Decimal

class FavoriteIn(BaseModel):
    name: str = Field(min_length=1)
    payment_type: TransferType | None = None
    recipient_data: dict

class FavoriteOut(FavoriteIn):
    model_config = ConfigDict(from_attributes=True)

    favorite_id: uuid.UUID
    client_id: uuid.UUID

class RecentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recipient_id: uuid.UUID
    phone: str
    name: str
    last_used_at: datetime
