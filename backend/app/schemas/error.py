from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., description="错误码")
    message: str = Field(..., description="错误信息")


class ErrorResponse(BaseModel):
    error: ErrorDetail
