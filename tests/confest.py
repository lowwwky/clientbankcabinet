import pytest_asyncio
from datetime import date
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from main import main_app
from core.models import Base, Client, db_helper

TEST_DB_URL = "postgresql+asyncpg://user:password@localhost:5432/bankclient_test"


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with engine.connect() as conn:
        transaction = await conn.begin()
        async with AsyncSession(
            bind=conn,
            join_transaction_mode="create_savepoint",
            expire_on_commit=False,
        ) as s:
            yield s
        await transaction.rollback()
    await engine.dispose()


@pytest_asyncio.fixture
async def client(session):
    async def override_session():
        yield session

    main_app.dependency_overrides[db_helper.session_getter] = override_session
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as c:
        yield c
    main_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_client_obj(session):
    obj = Client(
        last_name="Иванов",
        first_name="Иван",
        birth_date=date(1990, 1, 1),
        phone="+79990000000",
    )
    session.add(obj)
    await session.commit()
    return obj