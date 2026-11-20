import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

class CardOut(BaseModel):
    card_id: uuid.UUID
    account_id: uuid.UUID
    masked_number: str
    card_type: str
    expiration_date: date
    status: str
    internet_payments_enabled: bool
    cash_withdrawal_enabled: bool
    limit: Decimal

class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_id: uuid.UUID
    client_id: uuid.UUID
    account_number: str
    name: str | None = None
    balance: Decimal
    currency: str
    tariff: str
    status: str

class AccountDetailOut(AccountOut):
    cards: list[CardOut] = []

class CardRequisitesOut(BaseModel):
    card_number: str
    expiration_date: date
    account_number: str

class CardSettingsIn(BaseModel):
    internet_payments_enabled: bool | None = None
    cash_withdrawal_enabled: bool | None = None
    limit: Decimal | None = Field(None, ge=0, max_digits=18, decimal_places=2)
