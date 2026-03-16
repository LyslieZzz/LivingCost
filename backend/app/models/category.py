from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_key = Column(String(50), primary_key=True, comment="分类唯一标识")
    name = Column(String(100), nullable=False, comment="分类中文名称")
    icon = Column(String(10), nullable=False, comment="分类图标")
    sort_order = Column(Integer, default=0, comment="排序顺序")

    items = relationship("Item", back_populates="category", order_by="Item.sort_order")
