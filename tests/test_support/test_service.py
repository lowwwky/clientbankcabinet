# tests/test_support/test_service.py
import pytest
from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from support.service import category_faq, create_request


async def test_category_faq_empty():
    result = MagicMock()
    result.all.return_value = []
    session = AsyncMock()
    session.scalars.return_value = result

    assert await category_faq(session=session, category="Карты") == []


def test_create_request_operation_not_found():
    db = MagicMock()
    db.get.return_value = None
    data = SimpleNamespace(operation_id=uuid4())

    with pytest.raises(HTTPException) as error:
        create_request(db=db, me=uuid4(), data=data, ip=None)

    assert error.value.status_code == 404