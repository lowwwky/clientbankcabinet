import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import JSON, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base, utcnow


class Operation(Base):
    __tablename__ = "operations"

    operation_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accounts.account_id"), index=True)
    operation_type: Mapped[str] = mapped_column(String(50))   # Перевод / Платёж / Пополнение / Списание
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    date: Mapped[datetime] = mapped_column(default=utcnow, index=True)
    status: Mapped[str] = mapped_column(String(200))          # Создана / В обработке / Успешно / Отклонено / Ошибка
    description: Mapped[str | None] = mapped_column(Text)


class Transfer(Base):
    __tablename__ = "transfers"

    transfer_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    operation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("operations.operation_id"), unique=True)
    recipient: Mapped[str] = mapped_column(String(500))
    recipient_bank: Mapped[str] = mapped_column(String(1000))
    message: Mapped[str | None] = mapped_column(Text)
    transfer_type: Mapped[str] = mapped_column(String(150))


class Favorite(Base):
    __tablename__ = "favorites"

    favorite_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.client_id"), index=True)
    name: Mapped[str] = mapped_column(Text)
    payment_type: Mapped[str | None] = mapped_column(String(150))
    recipient_data: Mapped[dict] = mapped_column(JSON)


class RecentRecipient(Base):
    __tablename__ = "recent_recipients"

    recipient_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.client_id"), index=True)
    phone: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(Text)
    last_used_at: Mapped[datetime] = mapped_column(default=utcnow)