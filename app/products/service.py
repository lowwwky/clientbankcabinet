import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Account, Card
from .schemas import AccountDetailOut, CardOut, CardSettingsIn


def mask_card(number: str) -> str:
    digits = number.replace(" ", "")
    return "**** **** **** " + digits[-4:]

def card_out(card: Card) -> CardOut:
    return CardOut(
        card_id=card.card_id, account_id=card.account_id, masked_number=mask_card(card.card_number),
        card_type=card.card_type, expiration_date=card.expiration_date, status=card.status,
        internet_payments_enabled=card.internet_payments_enabled,
        cash_withdrawal_enabled=card.cash_withdrawal_enabled, limit=card.limit,
    )

def list_accounts(db: Session, client_id: uuid.UUID) -> list[Account]:
    return list(db.scalars(select(Account).where(Account.client_id == client_id)))

def get_own_account(db: Session, account_id: uuid.UUID, me: uuid.UUID) -> Account:
    account = db.get(Account, account_id)
    if account is None or account.client_id != me:
        raise HTTPException(404, "Счёт не найден")
    return account

def account_detail(db: Session, account: Account) -> AccountDetailOut:
    cards = db.scalars(select(Card).where(Card.account_id == account.account_id))
    out = AccountDetailOut.model_validate(account)
    out.cards = [card_out(c) for c in cards]
    return out

def get_own_card(db: Session, card_id: uuid.UUID, me: uuid.UUID) -> tuple[Card, Account]:
    card = db.get(Card, card_id)
    account = db.get(Account, card.account_id) if card else None
    if card is None or account is None or account.client_id != me:
        raise HTTPException(404, "Карта не найдена")
    return card, account

def change_status(db: Session, card: Card, new_status: str, allowed_from: tuple[str, ...]) -> Card:
    if card.status not in allowed_from:
        raise HTTPException(409, f"Нельзя выполнить действие: карта в статусе «{card.status}»")
    card.status = new_status
    db.commit()
    return card

def update_settings(db: Session, card: Card, data: CardSettingsIn) -> Card:
    if card.status in ("Заблокирована", "Закрыта"):
        raise HTTPException(409, "Настройки недоступны для заблокированной или закрытой карты")
    changes = data.model_dump(exclude_unset=True, exclude_none=True)
    if not changes:
        raise HTTPException(400, "Не указано, что менять")
    for field, value in changes.items():
        setattr(card, field, value)
    db.commit()
    return card