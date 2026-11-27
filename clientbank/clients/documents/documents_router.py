from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from core.dependencies import SESSION_DEPENDENCY
from clients.schemas import DocumentIn, DocumentOut, DocumentUpdate
from clients.documents.documents_service import add_document, get_document, list_documents, update_document, \
    delete_document
from core.models import Document

router = APIRouter(prefix="/{client_id}/documents", tags=["Документы"])


@router.get("/all/", response_model=DocumentOut)
async def get_documents(
        session: SESSION_DEPENDENCY,
        client_id: UUID,
):
    return await list_documents(session=session, client_id=client_id)


@router.post("/add/", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def add_new_document(
        session: SESSION_DEPENDENCY,
        client_id: UUID,
        data: DocumentIn,
):
    document = Document(client_id=client_id, **data.model_dump())
    return await add_document(session=session, document=document)


@router.patch("/update/", response_model=DocumentUpdate)
async def update_document(
        session: SESSION_DEPENDENCY,
        client_id: UUID,
        document_id: UUID,
        data: DocumentIn,
):
    document = await get_document(session=session, client_id=client_id, document_id=document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден",
        )
    return await update_document(session=session, document=document, **data.model_dump(exclude_unset=True))


@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
        session: SESSION_DEPENDENCY,
        client_id: UUID,
        document_id: UUID,
) -> None:
    document = await get_document(session, document_id, client_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Документ не найден",
        )
    await delete_document(session=session, document=document)
