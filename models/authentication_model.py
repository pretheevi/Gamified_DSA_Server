from pydantic import BaseModel

class RegisterValidate(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str

class LoginValidate(BaseModel):
    email: str
    password: str

class EmailOnlyValidate(BaseModel):
    email: str

class UpdatePasswordValidate(BaseModel):
    email: str
    password: str

class VerifyOTPValidate(BaseModel):
    email: str
    otp: str

class TimePayload(BaseModel):
    time: int
    status: str

class StatusCheck(BaseModel):
    status: str