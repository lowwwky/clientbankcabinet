import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..core.db import get_db
from . import service
from .schemas import ChatOut, FaqOut, MessageIn, MessageOut, RequestIn, RequestOut

router = APIRouter(tags=["Поддержка и чат"])

@router.get("/faq", response_model=list[FaqOut])
def get_faq(category: str | None = None, db: Session = Depends(get_db)):
    return service.list_faq(db, category)
