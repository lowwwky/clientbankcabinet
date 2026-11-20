import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..core.db import get_db
from . import service
from .schemas import ClientOut, ContactsUpdate, DocumentIn, DocumentOut

router = APIRouter(prefix="/clients", tags=["Клиенты"])

@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: uuid.UUID, ):
    ...

@router.get("/{client_id}/documents", response_model=DocumentOut)
def get_documents():
    ...

@router.patch("/{client_id}/contacts")
def update_contacts():
    ...

@router.post("/{client_id}/documents", response_model=DocumentOut, status_code=201)
def add_documents():
    ...



