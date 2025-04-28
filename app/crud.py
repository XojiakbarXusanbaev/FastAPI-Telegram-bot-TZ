from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models import User
from app.schemas import UserRegister, UserVerify
from app.utils.code_generator import generate_verification_code


def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def create_user(db: Session, user_data: UserRegister):
    existing_user = get_user_by_telegram_id(db, user_data.telegram_id)
    
    verification_code = generate_verification_code()
    
    if existing_user:
        existing_user.phone_number = user_data.phone_number
        existing_user.set_verification_code(verification_code)
        db.commit()
        db.refresh(existing_user)
        return existing_user, verification_code
    
    try:
        db_user = User(
            telegram_id=user_data.telegram_id,
            phone_number=user_data.phone_number,
        )
        db_user.set_verification_code(verification_code)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user, verification_code
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu telegram_id bilan foydalanuvchi allaqachon mavjud"
        )


def verify_user(db: Session, verification_data: UserVerify):
    verification_code = verification_data.verification_code
    
    user = db.query(User).filter(User.verification_code == verification_code).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Noto'g'ri kod. Foydalanuvchi topilmadi"
        )
    
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Foydalanuvchi allaqachon tasdiqlangan"
        )
    
    if not user.is_code_valid(verification_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Muddati o'tgan kod"
        )
    
    user.is_verified = True
    user.verification_code = None
    user.expires_at = None
    db.commit()
    db.refresh(user)
    
    return user
