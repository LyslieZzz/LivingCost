from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.submission import SubmissionStatus


class SubmissionCreate(BaseModel):
    city_key: str = Field(..., description="城市标识")
    item_id: int = Field(..., description="项目ID")
    submitted_price: float = Field(..., gt=0, description="提交的价格")
    source_desc: Optional[str] = Field(None, max_length=200, description="数据来源描述")


class SubmissionResponse(BaseModel):
    id: int
    city_key: str
    item_id: int
    submitted_price: float
    source_desc: Optional[str]
    status: SubmissionStatus
    reviewer_note: Optional[str]
    created_at: datetime
    reviewed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class SubmissionReview(BaseModel):
    status: SubmissionStatus = Field(..., description="审核状态")
    reviewer_note: Optional[str] = Field(None, max_length=500, description="审核备注")


class SubmissionListResponse(BaseModel):
    submissions: list[SubmissionResponse]
    total: int
