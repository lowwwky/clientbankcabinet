# tests/test_support/test_service.py
import pytest
from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from support.service import category_faq, create_request  # подставь свои пути


async def test_category_faq_empty():
    result = MagicMock()
    result.all.return_value = []
    session = AsyncMock()
    session.scalars.return_value = result

    assert await category_faq(session=session, category="Карты") == []


async def test_create_request_operation_not_found():
    session = AsyncMock()
    session.get.return_value = None          # такой операции нет
    data = SimpleNamespace(operation_id=uuid4())

    with pytest.raises(HTTPException) as error:
        await create_request(session=session, client_id=uuid4(), data=data)
    assert error.value.status_code == 404