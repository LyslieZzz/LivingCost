from sqlalchemy.orm import Session

from app.models import City, Category, Item, CityPrice, MonthlyEstimate
from app.schemas.comparison import (
    CategoryComparisonResponse,
    CategoryComparisonItem,
    CompareResponse,
)
from app.schemas.cost import MonthlyEstimateResponse


def get_category_comparison(db: Session, category_key: str) -> CategoryComparisonResponse | None:
    """获取某分类下所有城市的价格对比"""
    category = db.query(Category).filter(
        Category.category_key == category_key
    ).first()
    if not category:
        return None

    items = (
        db.query(Item)
        .filter(Item.category_key == category_key)
        .order_by(Item.sort_order)
        .all()
    )

    cities = db.query(City).all()
    city_keys = [c.city_key for c in cities]

    comparison_items = []
    for idx, item in enumerate(items):
        prices = (
            db.query(CityPrice)
            .filter(CityPrice.item_id == item.id)
            .all()
        )

        price_dict = {p.city_key: float(p.price) for p in prices}

        if price_dict:
            price_values = list(price_dict.values())
            comparison_items.append(
                CategoryComparisonItem(
                    index=idx,
                    name=item.name,
                    prices=price_dict,
                    min=min(price_values),
                    max=max(price_values),
                )
            )

    return CategoryComparisonResponse(
        category=category_key,
        categoryName=category.name,
        items=comparison_items,
    )


def get_category_by_key(db: Session, category_key: str) -> Category | None:
    """根据 key 获取分类"""
    return db.query(Category).filter(Category.category_key == category_key).first()


def get_cities_comparison(db: Session, city_keys: list[str]) -> CompareResponse | None:
    """多城市对比"""
    cities = db.query(City).filter(City.city_key.in_(city_keys)).all()
    if len(cities) < 2:
        return None

    found_keys = [c.city_key for c in cities]

    monthly_estimates = {}
    estimates = db.query(MonthlyEstimate).filter(
        MonthlyEstimate.city_key.in_(found_keys)
    ).all()
    for est in estimates:
        monthly_estimates[est.city_key] = {"single": float(est.single_estimate)}

    avg_salaries = {}
    salary_items = (
        db.query(CityPrice, Item)
        .join(Item, CityPrice.item_id == Item.id)
        .filter(
            Item.is_salary == True,
            CityPrice.city_key.in_(found_keys),
        )
        .all()
    )
    for price, item in salary_items:
        avg_salaries[price.city_key] = float(price.price)

    center_defs = {c.city_key: c.center_def for c in cities}

    categories = db.query(Category).order_by(Category.sort_order).all()
    categories_comparison = {}

    for category in categories:
        category_data = {}
        for city_key in found_keys:
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

            category_data[city_key] = [
                {
                    "name": item.name,
                    "price": float(price.price),
                    "unit": item.unit,
                }
                for item, price in items_with_prices
            ]

        if any(category_data.values()):
            categories_comparison[category.category_key] = category_data

    return CompareResponse(
        cities=found_keys,
        comparison={
            "monthlyEstimate": monthly_estimates,
            "avgSalary": avg_salaries,
            "centerDef": center_defs,
            "categories": categories_comparison,
        },
    )
