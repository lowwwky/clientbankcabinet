from uuid import UUID

from fastapi import APIRouter

from .schemas import ClientOut
from .service import get_client
from core.dependencies import SESSION_DEPENDENCY
from clients.documents.documents_router import router as documents_router

router = APIRouter(prefix="/clients", tags=["Клиенты"])
router.include_router(documents_router)


@router.get("/{client_id}/info/", response_model=ClientOut)
async def get_client_info(
        client_id: UUID,
        session: SESSION_DEPENDENCY
):
    return await get_client(session=session, client_id=client_id)
