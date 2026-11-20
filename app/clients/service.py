import uuid
from datetime import date

from fastapi import HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Client, Document
from .schemas import ClientOut, ContactsUpdate, DocumentIn

def calc_age(birthdate: date, today:date | None = None) -> int:
    today = today or date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def get_client(db: Session, client_id: uuid.UUID) -> type[Client]:
    client = db.get(Client,client_id)
    if client is None:
        raise HTTPException(404, "Клиент не найден")
    return client

def client_out(client: Client) -> ClientOut:
    out = ClientOut.model_validate(client)
    out.age = calc_age(client.birth_date)
    return out

def update_contacts(db: Session, client: Client, data: ContactsUpdate ) -> Client:
    changes = data.model_dump(exclude_unset=True, exclude_none=True)
    if not changes:
        raise HTTPException(404, "Не указано, что менять")
    if "phone" in changes and changes["phone"] != client.phone:
        busy = db.scalar(select(Client).where(Client.phone == changes["phone"]))
        if busy is not None:
            raise HTTPException(409, "Этот номер телефона уже используется")
        client.phone = changes["phone"]

    if "email" in changes:
        client.email = changes["email"]

    db.commit()
    return client

def list_documents(db: Session, client_id: uuid.UUID) -> list[Document]:
    return list(db.scalars(select(Document).where(Document.client_id == client_id)))

def add_document(db: Session, client_id: uuid.UUID, data: DocumentIn, ) -> type[Document]:
    doc = Document(client_id=client_id, **data.model_dump())
    db.add(doc)
    db.commit()
    return doc
