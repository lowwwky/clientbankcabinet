import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..core.db import get_db
from . import service
from .schemas import AccountDetailOut, AccountOut, CardOut, CardRequisitesOut, CardSettingsIn

router = APIRouter(tags=["Банковские продукты"])

@router.get("/clients/{client_id}/accounts", response_model=list[AccountOut])
def get_accounts(client_id: uuid.UUID, db: Session = Depends(get_db)):
    return service.list_accounts(db, client_id)

@router.get("/accounts/{account_id}", response_model=AccountDetailOut)
def get_account(account_id: uuid.UUID, me: uuid.UUID,
                db: Session = Depends(get_db)):
    return service.account_detail(db, service.get_own_account(db, account_id, me))

@router.get("/cards/{card_id}", response_model=CardOut)
def get_card(card_id: uuid.UUID, me: uuid.UUID, db: Session = Depends(get_db)):
    card, _ = service.get_own_card(db, card_id, me)
    return service.card_out(card)

@router.post("/cards/{card_id}/block", response_model=CardOut)
def block_card(card_id: uuid.UUID, client_id: uuid.UUID, db: Session = Depends(get_db)):
    card, _ = service.get_own_card(db, card_id, client_id)
    service.change_status(db, card, "Заблокирована", ("Активна", "Заморожена"))
    return service.card_out(card)

@router.post("/cards/{card_id}/freeze", response_model=CardOut)
def freeze_card(card_id: uuid.UUID, client_id: uuid.UUID, db: Session = Depends(get_db)):
    card, _ = service.get_own_card(db, card_id, client_id)
    service.change_status(db, card, "Заморожена", ("Активна",))
    return service.card_out(card)

@router.post("/cards/{card_id}/unfreeze", response_model=CardOut)
def unfreeze_card(card_id: uuid.UUID, client_id: uuid.UUID, db: Session = Depends(get_db)):
    card, _ = service.get_own_card(db, card_id, client_id)
    service.change_status(db, card, "Активна", ("Заморожена",))
    return service.card_out(card)

@router.patch("/cards/{card_id}/settings", response_model=CardOut)
def update_card_settings(card_id: uuid.UUID, client_id: uuid.UUID, data: CardSettingsIn,
                         db: Session = Depends(get_db)):
    card, _ = service.get_own_card(db, card_id, client_id)
    service.update_settings(db, card, data)
    return service.card_out(card)