import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.models.payments import Operation
from core.models.products import Account
from core.models.support import Faq, SupportRequest
from .schemas import RequestIn

SUPPORT_BOT_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


def create_request(db: Session, me: uuid.UUID, data: RequestIn, ip: str | None) -> SupportRequest:
    if data.operation_id is not None:
        op = db.get(Operation, data.operation_id)
        account = db.get(Account, op.source_account_id) if op else None
        if account is None or account.client_id != me:
            raise HTTPException(404, "Операция не найдена")
    req = SupportRequest(client_id=me, **data.model_dump())
    db.add(req)
    db.commit()
    return req


def list_requests(db: Session, me: uuid.UUID) -> list[SupportRequest]:
    return list(db.scalars(
        select(SupportRequest).where(SupportRequest.client_id == me)
        .order_by(SupportRequest.created_at.desc())
    ))


async def category_faq(
        session: AsyncSession,
        category: str,

) -> list[Faq]:
    result = await session.scalars(
        select(Faq)
        .where(Faq.category == category)
    )
    return list(result.all())


async def get_all_answers(
        session: AsyncSession,
) -> list[Faq]:
    result = await session.scalars(
        select(Faq)
    )
    return list(result.all())
