import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models import City, Category, Item, CityPrice, MonthlyEstimate


@pytest.fixture(scope="function")
def test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def seed_data(test_db):
    """插入测试数据"""
    cities = [
        City(city_key="beijing", name="北京", emoji="🏛️", center_def="三环内"),
        City(city_key="shanghai", name="上海", emoji="🌆", center_def="内环内"),
    ]
    test_db.add_all(cities)

    categories = [
        Category(category_key="dining", name="餐饮", icon="🥗", sort_order=1),
        Category(category_key="market", name="超市/市场", icon="🛒", sort_order=2),
    ]
    test_db.add_all(categories)

    items = [
        Item(
            id=1,
            category_key="dining",
            name="平价餐厅一顿饭",
            description="普通快餐/盖浇饭/工作餐",
            unit="元",
            sort_order=1,
        ),
        Item(
            id=2,
            category_key="dining",
            name="麦当劳套餐",
            description="标准化价格参考",
            unit="元",
            sort_order=2,
        ),
        Item(
            id=3,
            category_key="market",
            name="牛奶 (1L)",
            description="",
            unit="元",
            sort_order=1,
        ),
    ]
    test_db.add_all(items)

    prices = [
        CityPrice(city_key="beijing", item_id=1, price=Decimal("40")),
        CityPrice(city_key="beijing", item_id=2, price=Decimal("42")),
        CityPrice(city_key="beijing", item_id=3, price=Decimal("14")),
        CityPrice(city_key="shanghai", item_id=1, price=Decimal("38")),
        CityPrice(city_key="shanghai", item_id=2, price=Decimal("42")),
        CityPrice(city_key="shanghai", item_id=3, price=Decimal("13.5")),
    ]
    test_db.add_all(prices)

    estimates = [
        MonthlyEstimate(city_key="beijing", single_estimate=Decimal("8500")),
        MonthlyEstimate(city_key="shanghai", single_estimate=Decimal("8200")),
    ]
    test_db.add_all(estimates)

    test_db.commit()
    return test_db
