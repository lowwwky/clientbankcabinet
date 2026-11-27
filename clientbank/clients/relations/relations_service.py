from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models.clients import ClientRelation


async def get_relations(
        session: AsyncSession,
        client_id: UUID,
) -> list[ClientRelation]:
    result = await session.scalars(
        select(ClientRelation)
        .where(ClientRelation.client_id == client_id)
    )
    return list(result.all())


async def find_relation(
        session: AsyncSession,
        client_id: UUID,
        child_id: UUID
) -> ClientRelation | None:
    return await session.scalar(
        select(ClientRelation)
        .where(
            ClientRelation.client_id == client_id,
            ClientRelation.related_client_id == child_id,
        )
    )


async def add_relations(
        session: AsyncSession,
        relation: ClientRelation
) -> ClientRelation | None:
    session.add(relation)
    await session.commit()
    await session.refresh(relation)
    return relation


async def delete_relations(
        session: AsyncSession,
        relation: ClientRelation
) -> None:
    await session.delete(relation)
    await session.commit()
