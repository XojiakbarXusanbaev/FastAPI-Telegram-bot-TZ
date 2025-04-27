from pydantic import BaseModel, Field, validator
import re


class UserRegister(BaseModel):
    telegram_id: int
    phone_number: str
    
    @validator('phone_number')
    def validate_phone(cls, value):
        if not re.match(r'^\+[0-9]{12}$', value):
            raise ValueError('Invalid phone number format. It should be like +998901234567')
        return value


class UserVerify(BaseModel):
    telegram_id: int
    verification_code: str = Field(..., min_length=6, max_length=6)


class ResponseMessage(BaseModel):
    message: str


class UserResponse(BaseModel):
    id: int
    telegram_id: int
    phone_number: str
    is_verified: bool
    
    class Config:
        orm_mode = True
