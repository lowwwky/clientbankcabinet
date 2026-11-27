from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from clients.schemas import RelationOut, RelationIn
from clients.relations.relations_service import get_relations, find_relation, add_relations, delete_relations
from clients.general.client_info_service import get_client
from core.dependencies import SESSION_DEPENDENCY
from core.models.clients import ClientRelation

router = APIRouter(prefix="/{client_id}/relations", tags=["Связи"])


@router.get("/all/", response_model=list[RelationOut])
async def get_client_relations(
        session: SESSION_DEPENDENCY,
        client_id: UUID,
):
    await get_client(session=session, client_id=client_id)
    return await get_relations(session, client_id)


@router.post("/add/", response_model=RelationOut, status_code=status.HTTP_201_CREATED)
async def add_client_relation(
        session: SESSION_DEPENDENCY,
        client_id: UUID,
        data: RelationIn,
):
    await get_client(session=session, client_id=client_id)
    await get_client(session=session, client_id=data.related_client_id)
    if data.related_client_id == client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя добавить связь с собой."
        )
    if await find_relation(session=session, client_id=client_id, child_id=data.related_client_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такая связь уже существует."
        )
    relation = ClientRelation(client_id=client_id, **data.model_dump())
    return await add_relations(session=session, relation=relation)


@router.delete("/delete/", response_model=RelationOut, status_code=status.HTTP_200_OK)
async def delete_client_relation(
        session: SESSION_DEPENDENCY,
        client_id: UUID,
        data: RelationIn,

) -> None:
    await get_client(session=session, client_id=client_id)
    await get_client(session=session, client_id=data.related_client_id)
    relation = await find_relation(session=session, client_id=client_id, child_id=data.related_client_id)
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Связи не существует."
        )
    await delete_relations(session=session,relation=relation)
