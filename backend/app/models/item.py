from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="项目ID")
    category_key = Column(
        String(50),
        ForeignKey("categories.category_key", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        comment="所属分类",
    )
    name = Column(String(200), nullable=False, comment="项目名称")
    description = Column(String(500), default="", comment="项目描述")
    unit = Column(String(50), nullable=False, comment="单位")
    is_big_price = Column(Boolean, default=False, comment="是否为大额价格")
    is_salary = Column(Boolean, default=False, comment="是否为薪资数据")
    sort_order = Column(Integer, default=0, comment="在分类内的排序顺序")

    category = relationship("Category", back_populates="items")
    prices = relationship("CityPrice", back_populates="item")
    submissions = relationship("PriceSubmission", back_populates="item")
