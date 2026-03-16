from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.comparison import CompareResponse
from app.schemas.error import ErrorResponse
from app.services import price_service

router = APIRouter()


@router.get(
    "/compare",
    response_model=CompareResponse,
    responses={400: {"model": ErrorResponse}},
    summary="多城市对比",
    description="对比多个城市的生活成本数据，至少需要2个城市",
)
async def compare_cities(
    cities: str = Query(
        ...,
        description="逗号分隔的城市标识列表，至少2个",
        examples=["beijing,shanghai"],
    ),
    db: Session = Depends(get_db),
):
    city_keys = [c.strip() for c in cities.split(",") if c.strip()]

    if len(city_keys) < 2:
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_PARAMS", "message": "至少需要2个城市进行对比"},
        )

    result = price_service.get_cities_comparison(db, city_keys)
    if not result:
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_PARAMS", "message": "未找到足够的有效城市"},
        )
    return result
