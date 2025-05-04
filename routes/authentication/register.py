from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

# Import necessary modules and classes
from models.authentication_model import RegisterValidate, EmailOnlyValidate, VerifyOTPValidate
from crud_db.crud_auth import crud_auth, OTP_handler, EmailService                
from security.password_hash import hash_password                            

router = APIRouter()

@router.post("/start")
async def start_registration(user: EmailOnlyValidate):
    # Check if email already exists
    exist = crud_auth.FindByEmail(user.email)
    if exist:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Generate OTP and expiry time
    OTP = OTP_handler.GenerateOTP()
    expire_time = OTP_handler.GenerateExpiryTime()
    
    # Insert OTP into the database
    insert_otp = OTP_handler.InsertOTP(user.email, OTP, expire_time)
    if insert_otp:
        OTP_sended = EmailService.send_otp_email(user.email, OTP)
        
        if OTP_sended:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "OTP sent successfully",
                    "email": user.email
                }
            )
        else:
            # If email sending failed, raise an HTTPException
            raise HTTPException(status_code=500, detail="Failed to send OTP")
    else:
        # If OTP insertion fails
        raise HTTPException(status_code=500, detail="Failed to insert OTP")


@router.post("/verify")
async def verify_otp(verify: VerifyOTPValidate): 
    # Check if email already exists
    exist = crud_auth.FindByEmail(verify.email)
    if exist:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    exist = OTP_handler.FindByEmailAndOTP(verify.email, verify.otp)
    if not exist:
        raise HTTPException(status_code=400, detail="Invalid email or OTP")
    
    result = OTP_handler.VerifyOTP(verify.email, verify.otp)
    if result:
        return JSONResponse(
            status_code=200,
            content={
                "message": "OTP verified successfully",
                "email": verify.email
            })
    else:
        raise HTTPException(status_code=400, detail="Failed to verify OTP")
    

@router.post("/complete")
async def complete_registration(user: RegisterValidate):  # username + password + email
    # Check if email already exists
    exist = crud_auth.FindByEmail(user.email)
    if exist:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    is_verified = OTP_handler.CheckIfVerified(user.email)
    if not is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")
    
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    hashed = hash_password(user.password)
    print(user, hashed)
    result = crud_auth.Register(user.username, user.email, hashed)
    if result:
        return JSONResponse(
            status_code=201,
            content={"message": "User registered successfully", "user": {
                "username": user.username,
                "email": user.email
            }}
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")
