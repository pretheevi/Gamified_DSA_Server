from fastapi import APIRouter, HTTPException
from .problems import router as Problems


product_router = APIRouter()

product_router.include_router(Problems, prefix="/problems", tags=["Problems"])
