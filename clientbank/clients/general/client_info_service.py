from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.clients import Client


async def get_client(
        session: AsyncSession,
        client_id: UUID
) -> Client:
    client = await session.get(Client, client_id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не найден"
        )
    return client


async def update_client(
        session: AsyncSession,
        client: Client,
        update_data: dict,
) -> Client:
    for key, value in update_data.items():
        if value is not None:
            setattr(client, key, value)
    await session.commit()
    await session.refresh(client)
    return client


async def remove_client(
        session: AsyncSession,
        client: Client,
) -> None:
    await session.delete(client)
    await session.commit()
