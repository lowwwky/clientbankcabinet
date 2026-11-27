from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Document


async def list_documents(
        session: AsyncSession,
        client_id: UUID,
) -> list[Document]:
    result = await session.scalars(
        select(Document).where(Document.client_id == client_id)
    )
    return list(result.all())


async def get_document(
        session: AsyncSession,
        document_id: UUID,
        client_id: UUID,
) -> Document:
    return await session.scalars(
        select(Document)
        .where(
            Document.document_id == document_id,
            Document.client_id == client_id,
        )
    )


async def add_document(
        session: AsyncSession,
        document: Document,
) -> Document:
    session.add(document)
    await session.commit()
    await session.refresh(document)
    return document


async def update_document(
        session: AsyncSession,
        document: Document,
        update_data: dict,
) -> Document:
    for key, value in update_data.items():
        setattr(document, key, value)
    await session.commit()
    await session.refresh(document)
    return document


async def delete_document(
        session: AsyncSession,
        document: Document,
):
    await session.delete(document)
    await session.commit()
