import pytest
from uuid import uuid4
from unittest.mock import AsyncMock
from fastapi import HTTPException

from clients.general.client_info_service import get_client


async def test_get_client_found():
    fake_client = object()
    session = AsyncMock()
    session.get.return_value = fake_client

    assert await get_client(session=session, client_id=uuid4()) is fake_client


async def test_get_client_not_found_raises_404():
    session = AsyncMock()
    session.get.return_value = None

    with pytest.raises(HTTPException) as error:
        await get_client(session=session, client_id=uuid4())
    assert error.value.status_code == 404