import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db import Base, utcnow

class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.client_id"), index=True)
    chat_type: Mapped[str] = mapped_column(String(50), default="пользовательский чат")  # или «служебный чат»
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    status: Mapped[str] = mapped_column(String(50), default="Активен")  # Активен / В архиве / Удален

class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.chat_id"), index=True)
    sender: Mapped[uuid.UUID] = mapped_column()   # id клиента, сотрудника или бота поддержки
    text: Mapped[str] = mapped_column(Text)
    sent_at: Mapped[datetime] = mapped_column(default=utcnow)

class SupportRequest(Base):
    __tablename__ = "support_requests"

    request_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.client_id"), index=True)
    operation_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("operations.operation_id"))
    reason: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(200), default="Создано")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    assigned_employee_id: Mapped[uuid.UUID | None] = mapped_column()
    closed_at: Mapped[datetime | None] = mapped_column()

class Faq(Base):
    __tablename__ = "faq"

    faq_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(Text)
