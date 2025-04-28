from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
import uvicorn

from app.database import Base, engine, get_db
from app.models import User
from app.schemas import UserRegister, UserVerify, ResponseMessage, UserResponse
from app.crud import create_user, verify_user

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Telegram Bot Ro'yxatdan o'tkazish API",
    description="Telegram bot orqali foydalanuvchilarni ro'yxatdan o'tkazish va tasdiqlash uchun API",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Telegram Bot Ro'yxatdan o'tkazish API"}


@app.post("/register", response_model=ResponseMessage, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        user, verification_code = create_user(db, user_data)
        logger.info(f"User with telegram_id {user_data.telegram_id} registered successfully")
        
        logger.info(f"Verification code for {user_data.telegram_id}: {verification_code}")
        
        return {"message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tkazildi. Tasdiqlash kodi yuborildi."}
    
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/verify", response_model=ResponseMessage)
def verify_user_code(verification_data: UserVerify, db: Session = Depends(get_db)):
    try:
        user = verify_user(db, verification_data)
        logger.info(f"User with code {verification_data.verification_code} verified successfully. Telegram ID: {user.telegram_id}")
        
        return {"message": "Foydalanuvchi muvaffaqiyatli tasdiqlandi"}
    
    except HTTPException as e:
        logger.error(f"Error verifying user: {e.detail}")
        raise e
    
    except Exception as e:
        logger.error(f"Unexpected error verifying user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@app.get("/user/{telegram_id}", response_model=UserResponse)
def get_user(telegram_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi"
        )
    
    return user


@app.get("/get_verification_code/{telegram_id}")
def get_verification_code(telegram_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    
    if not user or not user.verification_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi yoki tasdiqlash kodi topilmadi"
        )
    
    from datetime import datetime
    if datetime.now() > user.expires_at:
        return {
            "verification_code": "",
            "message": "Tasdiqlash kodining muddati tugagan"
        }
    
    return {
        "verification_code": user.verification_code,
        "expires_at": user.expires_at
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
