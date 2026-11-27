import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (JSON, ForeignKey, Numeric,
    String, Text, DateTime, func)

from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Operation(Base):
    operation_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accounts.account_id"), index=True)
    operation_type: Mapped[str] = mapped_column(String(50))   # Перевод / Платёж / Пополнение / Списание
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    status: Mapped[str] = mapped_column(String(200))          # Создана / В обработке / Успешно / Отклонено / Ошибка
    description: Mapped[str | None] = mapped_column(Text)


class Transfer(Base):
    transfer_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    operation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("operations.operation_id"), unique=True)
    recipient: Mapped[str] = mapped_column(String(500))
    recipient_bank: Mapped[str] = mapped_column(String(1000))
    message: Mapped[str | None] = mapped_column(Text)
    transfer_type: Mapped[str] = mapped_column(String(150))


class Favorite(Base):
    favorite_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("test_clients.client_id"), index=True)
    name: Mapped[str] = mapped_column(Text)
    payment_type: Mapped[str | None] = mapped_column(String(150))
    recipient_data: Mapped[dict] = mapped_column(JSON)


class RecentRecipient(Base):
    recipient_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("test_clients.client_id"), index=True)
    phone: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(Text)
    last_used_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )