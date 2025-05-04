from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

# Import necessary modules and classes
from models.authentication_model import LoginValidate             # Validation model for login
from crud_db.crud_auth import crud_auth                           # CRUD operations for authentication
from security.password_hash import verify_password                # Password verification
from security.token_handler import create_access_token            # Token creation

router = APIRouter()

@router.post("/")
async def login(user: LoginValidate):
        exist = crud_auth.FindByEmail(user.email)
        if not exist:
            raise HTTPException(status_code=400, detail="Account does not exist, please Sign Up")

        result = crud_auth.Login(user.email)
        is_verified = verify_password(user.password, result["password"])

        if not result or not is_verified:
            raise HTTPException(status_code=400, detail="Invalid email or password")

        # Create access token
        access_token = create_access_token(data={"sub": result["email"], "user_id": result["id"]})
        return JSONResponse(status_code=200, content={
            "message": "User logged in successfully",
            "user": {
                "id": result["id"],
                "username": result["username"],
                "email": result["email"],
            },
            "access_token": access_token
        })