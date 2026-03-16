from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.city import CitiesResponse
from app.schemas.cost import CostResponse, EstimateResponse
from app.schemas.error import ErrorResponse
from app.services import city_service

router = APIRouter()


@router.get(
    "/cities",
    response_model=CitiesResponse,
    summary="获取城市列表",
    description="获取所有支持的城市列表",
)
async def get_cities(db: Session = Depends(get_db)):
    return city_service.get_all_cities(db)


@router.get(
    "/cities/{city_key}/costs",
    response_model=CostResponse,
    responses={404: {"model": ErrorResponse}},
    summary="获取城市生活成本详情",
    description="获取指定城市的完整生活成本数据，包括各分类价格项目",
)
async def get_city_costs(city_key: str, db: Session = Depends(get_db)):
    result = city_service.get_city_costs(db, city_key)
    if not result:
        raise HTTPException(
            status_code=404,
            detail={"code": "CITY_NOT_FOUND", "message": "城市不存在"},
        )
    return result


@router.get(
    "/cities/{city_key}/estimate",
    response_model=EstimateResponse,
    responses={404: {"model": ErrorResponse}},
    summary="获取城市月度预估支出",
    description="获取指定城市的单人月度预估支出",
)
async def get_city_estimate(city_key: str, db: Session = Depends(get_db)):
    result = city_service.get_city_estimate(db, city_key)
    if not result:
        raise HTTPException(
            status_code=404,
            detail={"code": "CITY_NOT_FOUND", "message": "城市不存在"},
        )
    return result
