import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..core.db import get_db
from . import service
from .schemas import (FavoriteIn, FavoriteOut, OperationOut,)

router = APIRouter(tags=["Платежи и переводы"])

@router.get("/operations", response_model=list[OperationOut])
def get_operations(client_id: uuid.UUID, account_id: uuid.UUID | None = None,
                   limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0),
                   db: Session = Depends(get_db)):
    return service.list_operations(db, client_id, account_id, limit, offset)

@router.get("/operations/{operation_id}", response_model=OperationOut)
def get_operation(operation_id: uuid.UUID, me: uuid.UUID,
                  db: Session = Depends(get_db)):
    return service.get_operation(db, me, operation_id)

@router.get("/favorites", response_model=list[FavoriteOut])
def get_favorites(me: uuid.UUID, db: Session = Depends(get_db)):
    return service.list_favorites(db, me)

@router.post("/favorites", response_model=FavoriteOut, status_code=201)
def add_favorite(data: FavoriteIn, me: uuid.UUID, db: Session = Depends(get_db)):
    return service.add_favorite(db, me, data)
