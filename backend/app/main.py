from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.config import get_settings
from app.routers import cities, categories, compare, submissions
from app.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

settings = get_settings()

app = FastAPI(
    title="城市生活成本查询 API",
    description="查询和对比中国主要城市（北京、上海、深圳、广州）的生活成本数据",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
if not settings.debug:
    app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(cities.router, prefix="/api", tags=["城市"])
app.include_router(categories.router, prefix="/api", tags=["分类"])
app.include_router(compare.router, prefix="/api", tags=["对比"])
app.include_router(submissions.router, prefix="/api", tags=["用户提交"])


@app.get("/", tags=["健康检查"])
async def root():
    return {"status": "ok", "message": "城市生活成本查询 API"}


@app.get("/health", tags=["健康检查"])
async def health_check():
    return {"status": "healthy"}
