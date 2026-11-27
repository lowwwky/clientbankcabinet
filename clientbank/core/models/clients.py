import uuid
from datetime import date

from sqlalchemy import Date,ForeignKey,String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base

class Client(Base):
    __tablename__ = "test_clients"

    client_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    last_name: Mapped[str] = mapped_column(String(500))
    first_name: Mapped[str] = mapped_column(String(500))
    middle_name: Mapped[str | None] = mapped_column(String(500))
    birth_date: Mapped[date] = mapped_column(Date)
    phone: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str | None] = mapped_column(String(500))
    avatar_url: Mapped[str | None] = mapped_column(String(500))

class Document(Base):
    document_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("test_clients.client_id"), index=True)
    document_type: Mapped[str] = mapped_column(String(200))
    series: Mapped[str] = mapped_column(String(20))
    number: Mapped[str] = mapped_column(String(20))
    issue_date: Mapped[date] = mapped_column(Date)
    issued_by: Mapped[str] = mapped_column(String(300))

class ClientRelation(Base):
    relation_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("test_clients.client_id"), index=True)
    related_client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("test_clients.client_id"))
    relation_type: Mapped[str] = mapped_column(String(50))