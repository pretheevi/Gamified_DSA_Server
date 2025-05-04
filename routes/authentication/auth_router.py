from fastapi import APIRouter
from .login import router as Login
from .register import router as Register
from .forgot_password import router as ForgotPassword

auth_router = APIRouter()

auth_router.include_router(Login, prefix="/login", tags=["Authentication"])
auth_router.include_router(Register, prefix="/register", tags=["Authentication"])
auth_router.include_router(ForgotPassword, prefix="/forgot-password", tags=["Authentication"])