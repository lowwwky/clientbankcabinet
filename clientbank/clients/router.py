from fastapi import APIRouter

from clients.documents.documents_router import router as documents_router
from clients.general.client_info_router import router as client_info_router
from clients.relations.relations_router import router as relations_router

router = APIRouter(prefix="/test_clients", tags=["Клиенты"])
router.include_router(documents_router)
router.include_router(client_info_router)
router.include_router(relations_router)

