from sqlalchemy import Column, String, Integer, DECIMAL, TIMESTAMP, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class CityPrice(Base):
    __tablename__ = "city_prices"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    city_key = Column(
        String(50),
        ForeignKey("cities.city_key", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        comment="城市标识",
    )
    item_id = Column(
        Integer,
        ForeignKey("items.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        comment="项目ID",
    )
    price = Column(DECIMAL(12, 2), nullable=False, comment="价格")
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    __table_args__ = (
        UniqueConstraint("city_key", "item_id", name="uk_city_item"),
    )

    city = relationship("City", back_populates="prices")
    item = relationship("Item", back_populates="prices")


class MonthlyEstimate(Base):
    __tablename__ = "monthly_estimates"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    city_key = Column(
        String(50),
        ForeignKey("cities.city_key", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        unique=True,
        comment="城市标识",
    )
    single_estimate = Column(DECIMAL(10, 2), nullable=False, comment="单人月度预估支出")
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    city = relationship("City", back_populates="monthly_estimate")
