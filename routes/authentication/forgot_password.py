from fastapi import APIRouter, HTTPException
from models.authentication_model import UpdatePasswordValidate
from crud_db.crud_auth import crud_auth
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/")
async def forgot_password(user: UpdatePasswordValidate):
        exist = crud_auth.FindByEmail(user.email)
        if not exist:
            raise HTTPException(
                status_code=404,
                detail="Account not found. Please sign up first."
            )
        result = crud_auth.UpdatePassword(user.email, user.password)
        if not result:
            raise HTTPException(
                status_code=400,
                detail="Failed to update password. Please try again."
            )
        return JSONResponse( status_code=200, content={"message": "Password updated successfully"})
