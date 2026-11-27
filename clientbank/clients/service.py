from uuid import UUID
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.models.clients import Client
from .schemas import ClientOut, ContactsUpdate


def calc_age(birthdate: date, today: date | None = None) -> int:
    today = today or date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


async def get_client(
        session: AsyncSession,
        client_id: UUID
) -> type[ClientOut]:
    client = await session.get(ClientOut, client_id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не найден"
        )
    return client


def client_out(client: Client) -> ClientOut:
    out = ClientOut.model_validate(client)
    out.age = calc_age(client.birth_date)
    return out


def update_contacts(db: Session, client: Client, data: ContactsUpdate) -> Client:
    changes = data.model_dump(exclude_unset=True, exclude_none=True)
    if not changes:
        raise HTTPException(404, "Не указано, что менять")
    if "phone" in changes and changes["phone"] != client.phone:
        busy = db.scalar(select(Client).where(Client.phone == changes["phone"]))
        if busy is not None:
            raise HTTPException(409, "Этот номер телефона уже используется")
        client.phone = changes["phone"]

    if "email" in changes:
        client.email = changes["email"]

    db.commit()
    return client
