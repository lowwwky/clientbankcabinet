import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Account(Base):
    account_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("test_clients.client_id"), index=True)
    account_number: Mapped[str] = mapped_column(String(200), unique=True)
    name: Mapped[str | None] = mapped_column(String(400))
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0"))
    currency: Mapped[str] = mapped_column(String(20), default="RUB")
    tariff: Mapped[str] = mapped_column(String(20), default="standard")   # standard / pro / business
    status: Mapped[str] = mapped_column(String(20), default="Активен")    # Активен / Заблокирован / Закрыт


class Card(Base):
    card_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accounts.account_id"), index=True)
    card_number: Mapped[str] = mapped_column(String(50))
    card_type: Mapped[str] = mapped_column(String(50))          # Дебетовая / Кредитная / Виртуальная
    expiration_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50), default="Активна")  # Активна / Заблокирована / Заморожена / Закрыта
    internet_payments_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    cash_withdrawal_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    limit: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0"))
