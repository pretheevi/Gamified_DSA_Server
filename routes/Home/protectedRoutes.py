from fastapi import APIRouter, HTTPException
from .problems import router as problems_router
from .status import router as status_router
from .time import router as time_router

product_router = APIRouter()

product_router.include_router(problems_router, prefix="/problems", tags=["Problems"])
product_router.include_router(time_router, prefix="/updateTime", tags=["Timer"])
product_router.include_router(status_router, prefix="/updateStatus", tags=["Status"])