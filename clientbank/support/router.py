from fastapi import APIRouter, HTTPException, status

from .schemas import FaqOut
from core.dependencies import SESSION_DEPENDENCY
from .service import get_all_answers, category_faq

router = APIRouter(prefix="/test_support", tags=["Поддержка и чат"])


@router.get("/faq", response_model=list[FaqOut])
async def get_all_faq(
        session: SESSION_DEPENDENCY,
):
    return await get_all_answers(session=session)


@router.get("/faq/{category}", response_model=list[FaqOut])
async def get_faq_for_category(
        session: SESSION_DEPENDENCY,
        category: str,
):
    faq_list = await category_faq(session=session, category=category)
    if not faq_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    return faq_list
