from uuid import UUID

from fastapi import HTTPException, APIRouter, status

from clients.schemas import ClientOut, ContactsUpdate, UpdateAvatar
from clients.general.client_info_service import get_client, update_client, remove_client
from core.dependencies import SESSION_DEPENDENCY

router = APIRouter(prefix="/{client_id}/me", tags=["Информация о клиенте", ])


@router.get("/info/", response_model=ClientOut)
async def get_client_info(
        client_id: UUID,
        session: SESSION_DEPENDENCY,
):
    client = await get_client(session=session, client_id=client_id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не найден",
        )
    return client


@router.patch("/update/", response_model=ClientOut)
async def update_client_info(
        session: SESSION_DEPENDENCY,
        client_id: UUID,
        data: ContactsUpdate,
):
    client = await get_client(session=session, client_id=client_id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не найден",
        )
    return await update_client(
        session=session,
        client=client,
        update_data=data.model_dump(exclude_unset=True)
    )


@router.patch("/photo/update/", response_model=ClientOut)
async def update_client_avatar(
        session: SESSION_DEPENDENCY,
        client_id: UUID,
        data: UpdateAvatar,
):
    client = await get_client(session=session, client_id=client_id)
    return await update_client(
        session=session,
        client=client,
        update_data=data.model_dump()
    )


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client_info(
        session: SESSION_DEPENDENCY,
        client_id: UUID,
) -> None:
    client = await get_client(session=session, client_id=client_id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Клиент не найден",
        )
    await remove_client(session=session, client=client)
