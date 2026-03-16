from sqlalchemy import Column, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    city_key = Column(String(50), primary_key=True, comment="城市唯一标识")
    name = Column(String(100), nullable=False, comment="城市中文名称")
    emoji = Column(String(10), nullable=False, comment="城市图标")
    center_def = Column(String(200), nullable=False, comment="市中心定义描述")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    prices = relationship("CityPrice", back_populates="city")
    monthly_estimate = relationship("MonthlyEstimate", back_populates="city", uselist=False)
    submissions = relationship("PriceSubmission", back_populates="city")
