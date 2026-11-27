import pytest_asyncio
from core.models import Faq


@pytest_asyncio.fixture
async def faq_items(session):
    session.add_all([
        Faq(question="Как заблокировать карту?", answer="Через раздел «Карты».", category="Карты"),
        Faq(question="Как сделать перевод?", answer="Через раздел «Платежи».", category="Переводы"),
    ])
    await session.commit()


async def test_all_faq_empty_table(client):
    r = await client.get("/test_support/faq")
    assert r.status_code == 200
    assert r.json() == []


async def test_all_faq(client, faq_items):
    r = await client.get("/test_support/faq")
    assert len(r.json()) == 2


async def test_faq_by_category(client, faq_items):
    r = await client.get("/test_support/faq/Карты")
    assert r.status_code == 200
    assert len(r.json()) == 1


async def test_faq_unknown_category(client, faq_items):
    r = await client.get("/test_support/faq/Такой-нет")
    assert r.status_code == 404


async def test_faq_category_case_sensitive(client, faq_items):
    r = await client.get("/test_support/faq/карты")     # с маленькой буквы
    assert r.status_code == 404