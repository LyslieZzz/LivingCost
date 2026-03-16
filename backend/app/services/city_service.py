from sqlalchemy.orm import Session

from app.models import City, Category, Item, CityPrice, MonthlyEstimate
from app.schemas.city import CityBase, CitiesResponse
from app.schemas.cost import (
    CostResponse,
    CityInfoResponse,
    MonthlyEstimateResponse,
    CategoryResponse,
    ItemResponse,
    EstimateResponse,
)


def get_all_cities(db: Session) -> CitiesResponse:
    """获取所有城市列表"""
    cities = db.query(City).order_by(City.city_key).all()
    return CitiesResponse(
        cities=[
            CityBase(
                key=city.city_key,
                name=city.name,
                emoji=city.emoji,
                centerDef=city.center_def,
            )
            for city in cities
        ]
    )


def get_city_by_key(db: Session, city_key: str) -> City | None:
    """根据 key 获取城市"""
    return db.query(City).filter(City.city_key == city_key).first()


def get_city_costs(db: Session, city_key: str) -> CostResponse | None:
    """获取城市完整生活成本数据"""
    city = get_city_by_key(db, city_key)
    if not city:
        return None

    estimate = db.query(MonthlyEstimate).filter(
        MonthlyEstimate.city_key == city_key
    ).first()

    categories = db.query(Category).order_by(Category.sort_order).all()

    categories_data = {}
    for category in categories:
        items_with_prices = (
            db.query(Item, CityPrice)
            .join(CityPrice, Item.id == CityPrice.item_id)
            .filter(
                Item.category_key == category.category_key,
                CityPrice.city_key == city_key,
            )
            .order_by(Item.sort_order)
            .all()
        )

        if items_with_prices:
            categories_data[category.category_key] = CategoryResponse(
                name=category.name,
                icon=category.icon,
                items=[
                    ItemResponse(
                        name=item.name,
                        desc=item.description or "",
                        price=float(price.price),
                        unit=item.unit,
                        isBigPrice=item.is_big_price,
                        isSalary=item.is_salary,
                    )
                    for item, price in items_with_prices
                ],
            )

    return CostResponse(
        city=CityInfoResponse(
            key=city.city_key,
            name=city.name,
            centerDef=city.center_def,
            emoji=city.emoji,
        ),
        monthlyEstimate=MonthlyEstimateResponse(
            single=float(estimate.single_estimate) if estimate else 0.0
        ),
        categories=categories_data,
    )


def get_city_estimate(db: Session, city_key: str) -> EstimateResponse | None:
    """获取城市月度预估支出"""
    city = get_city_by_key(db, city_key)
    if not city:
        return None

    estimate = db.query(MonthlyEstimate).filter(
        MonthlyEstimate.city_key == city_key
    ).first()

    return EstimateResponse(
        cityKey=city.city_key,
        cityName=city.name,
        estimate=MonthlyEstimateResponse(
            single=float(estimate.single_estimate) if estimate else 0.0
        ),
    )
