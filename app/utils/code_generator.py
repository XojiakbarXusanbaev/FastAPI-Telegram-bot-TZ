import random
import string
from app.config import VERIFICATION_CODE_LENGTH


def generate_verification_code() -> str:
    digits = string.digits
    code = ''.join(random.choice(digits) for _ in range(VERIFICATION_CODE_LENGTH))
    return code
