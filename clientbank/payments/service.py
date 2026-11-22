import logging
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.models.products import Account
from core.models.payments import Favorite, Operation
from .schemas import FavoriteIn

logger = logging.getLogger("bank.payments")

OWN_TRANSFER = "между своими счетами"
PHONE_TRANSFER = "по номеру телефона"

def _my_account_ids(me: uuid.UUID):
    return select(Account.account_id).where(Account.client_id == me)

def list_operations(db: Session, me: uuid.UUID, account_id: uuid.UUID | None,
                    limit: int, offset: int) -> list[Operation]:
    q = select(Operation).where(Operation.source_account_id.in_(_my_account_ids(me)))
    if account_id is not None:
        q = q.where(Operation.source_account_id == account_id)
    q = q.order_by(Operation.date.desc()).limit(limit).offset(offset)
    return list(db.scalars(q))

def get_operation(db: Session, me: uuid.UUID, operation_id: uuid.UUID) -> Operation:
    op = db.scalar(select(Operation).where(Operation.operation_id == operation_id,
                                           Operation.source_account_id.in_(_my_account_ids(me))))
    if op is None:
        raise HTTPException(404, "Операция не найдена")
    return op

def list_favorites(db: Session, me: uuid.UUID) -> list[Favorite]:
    return list(db.scalars(select(Favorite).where(Favorite.client_id == me)))

def add_favorite(db: Session, me: uuid.UUID, data: FavoriteIn) -> Favorite:
    fav = Favorite(client_id=me, **data.model_dump())
    db.add(fav)
    db.commit()
    return fav
