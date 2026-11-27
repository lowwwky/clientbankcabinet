import uuid
from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import TYPE_CHECKING

from core.models import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class ClientCredential(Base, SQLAlchemyBaseUserTableUUID):

    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("clients.client_id"), unique=True, nullable=False,
    )
    failed_attempts: Mapped[int] = mapped_column(default=0)
    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    @classmethod
    def get_db(cls, session:"AsyncSession"):
        return SQLAlchemyUserDatabase(session,ClientCredential)