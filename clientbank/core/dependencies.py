from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

SESSION_DEPENDENCY = Annotated[AsyncSession, Depends(db_helper.session_getter)]