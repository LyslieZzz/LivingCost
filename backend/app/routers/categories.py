from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.comparison import CategoryComparisonResponse
from app.schemas.error import ErrorResponse
from app.services import price_service

router = APIRouter()


@router.get(
    "/categories/{category_key}/comparison",
    response_model=CategoryComparisonResponse,
    responses={404: {"model": ErrorResponse}},
    summary="获取分类价格对比",
    description="获取某分类下所有城市的价格对比，用于显示价格范围条",
)
async def get_category_comparison(
    category_key: str,
    db: Session = Depends(get_db),
):
    result = price_service.get_category_comparison(db, category_key)
    if not result:
        raise HTTPException(
            status_code=404,
            detail={"code": "CATEGORY_NOT_FOUND", "message": "分类不存在"},
        )
    return result
