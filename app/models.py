from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime
from sqlalchemy.sql import func
from datetime import datetime, timedelta

from app.database import Base
from app.config import VERIFICATION_CODE_EXPIRY_MINUTES


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    phone_number = Column(String, index=True)
    verification_code = Column(String)
    expires_at = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def set_verification_code(self, code: str):
        self.verification_code = code
        self.expires_at = datetime.now() + timedelta(minutes=VERIFICATION_CODE_EXPIRY_MINUTES)
        self.is_verified = False

    def is_code_valid(self, code: str) -> bool:
        if self.is_verified:
            return False
        
        if self.verification_code != code:
            return False
        
        if datetime.now() > self.expires_at:
            return False
        
        return True
