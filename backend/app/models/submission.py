from sqlalchemy import Column, String, Integer, DECIMAL, TIMESTAMP, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class SubmissionStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PriceSubmission(Base):
    """用户提交的价格数据（预留功能）"""
    __tablename__ = "price_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_key = Column(
        String(50),
        ForeignKey("cities.city_key", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    item_id = Column(
        Integer,
        ForeignKey("items.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    submitted_price = Column(DECIMAL(12, 2), nullable=False, comment="用户提交的价格")
    source_desc = Column(String(200), comment="数据来源描述")
    status = Column(
        Enum(SubmissionStatus),
        default=SubmissionStatus.PENDING,
        comment="审核状态",
    )
    reviewer_note = Column(String(500), comment="审核备注")
    ip_address = Column(String(45), comment="提交者IP地址")
    fingerprint = Column(String(100), comment="设备指纹")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    reviewed_at = Column(TIMESTAMP, nullable=True)

    city = relationship("City", back_populates="submissions")
    item = relationship("Item", back_populates="submissions")
