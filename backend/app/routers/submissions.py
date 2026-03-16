"""
用户提交价格数据的 API 路由（预留功能）

MVP 阶段暂不实现具体逻辑，仅预留接口结构。
后期实现时需要添加：
1. 用户认证
2. 防刷机制（IP限制、设备指纹）
3. 数据验证（价格合理性检查）
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.submission import (
    SubmissionCreate,
    SubmissionResponse,
    SubmissionReview,
    SubmissionListResponse,
)
from app.schemas.error import ErrorResponse

router = APIRouter()


@router.post(
    "/submissions",
    response_model=SubmissionResponse,
    responses={
        400: {"model": ErrorResponse},
        501: {"model": ErrorResponse},
    },
    summary="提交价格数据（预留）",
    description="用户提交价格数据，MVP 阶段暂未实现",
)
async def create_submission(
    submission: SubmissionCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    raise HTTPException(
        status_code=501,
        detail={
            "code": "NOT_IMPLEMENTED",
            "message": "该功能正在开发中，敬请期待",
        },
    )


@router.get(
    "/submissions",
    response_model=SubmissionListResponse,
    responses={501: {"model": ErrorResponse}},
    summary="获取提交列表（预留）",
    description="管理员查看待审核的提交列表，MVP 阶段暂未实现",
)
async def list_submissions(
    status: Optional[str] = Query(None, description="筛选状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
):
    raise HTTPException(
        status_code=501,
        detail={
            "code": "NOT_IMPLEMENTED",
            "message": "该功能正在开发中，敬请期待",
        },
    )


@router.patch(
    "/submissions/{submission_id}",
    response_model=SubmissionResponse,
    responses={
        404: {"model": ErrorResponse},
        501: {"model": ErrorResponse},
    },
    summary="审核提交（预留）",
    description="管理员审核用户提交的价格数据，MVP 阶段暂未实现",
)
async def review_submission(
    submission_id: int,
    review: SubmissionReview,
    db: Session = Depends(get_db),
):
    raise HTTPException(
        status_code=501,
        detail={
            "code": "NOT_IMPLEMENTED",
            "message": "该功能正在开发中，敬请期待",
        },
    )
