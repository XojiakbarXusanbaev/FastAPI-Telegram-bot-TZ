import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
import requests
import json

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

API_BASE_URL = "http://localhost:8000"

PHONE, VERIFICATION = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    
    context.user_data["telegram_id"] = user.id
    
    keyboard = [[KeyboardButton("Telefon raqamni yuborish", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_html(
        f"Salom, {user.mention_html()}! 👋\n\n"
        "Ro'yxatdan o'tkazish botiga xush kelibsiz.\n"
        "Ro'yxatdan o'tish uchun telefon raqamingizni ulashing.",
        reply_markup=reply_markup,
    )
    
    return PHONE


async def request_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[KeyboardButton("Telefon raqamni yuborish", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        "Telefon raqamingizni yuborish uchun quyidagi tugmani bosing.",
        reply_markup=reply_markup,
    )
    
    return PHONE


async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone_number = update.message.contact.phone_number
    telegram_id = context.user_data.get("telegram_id")
    
    if not phone_number.startswith("+"):
        phone_number = f"+{phone_number}"
    
    context.user_data["phone_number"] = phone_number
    try:
        response = requests.post(
            f"{API_BASE_URL}/register",
            json={
                "telegram_id": telegram_id,
                "phone_number": phone_number
            }
        )
        response.raise_for_status()
        
        logger.info(f"User {telegram_id} registered with phone number {phone_number}")
        
        verification_code = ""
        
        code_response = requests.get(f"{API_BASE_URL}/get_verification_code/{telegram_id}")
        if code_response.status_code == 200:
            verification_code = code_response.json().get("verification_code", "")
        
        registration_message = "Siz muvaffaqiyatli ro'yxatdan o'tdingiz!\n\n"
        
        if verification_code:
            registration_message += f"Tasdiqlash kodingiz: {verification_code}\n"
        else:
            registration_message += "Siz uchun 6 raqamli tasdiqlash kodi yaratildi.\n"
            
        registration_message += "Hisobingizni tasdiqlash uchun kodni kiriting."
        
        await update.message.reply_text(
            registration_message,
            reply_markup=ReplyKeyboardRemove(),
        )
        
        return VERIFICATION
    
    except requests.exceptions.RequestException as e:
        error_message = "An error occurred during registration."
        
        if hasattr(e, 'response') and e.response:
            try:
                error_data = e.response.json()
                if 'detail' in error_data:
                    error_message = error_data['detail']
            except json.JSONDecodeError:
                pass
        
        logger.error(f"Registration error for user {telegram_id}: {str(e)}")
        
        await update.message.reply_text(
            f"Xato: {error_message}\n"
            "Qaytadan urinib ko'rish uchun /start tugmasini bosing",
            reply_markup=ReplyKeyboardRemove(),
        )
        
        return ConversationHandler.END


async def handle_verification_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    verification_code = update.message.text.strip()
    telegram_id = context.user_data.get("telegram_id")
    try:
        response = requests.post(
            f"{API_BASE_URL}/verify",
            json={
                "verification_code": verification_code
            }
        )
        response.raise_for_status()
        
        logger.info(f"Verification code {verification_code} verified successfully for user with telegram_id {telegram_id}")
        
        await update.message.reply_text(
            "🎉 Hisobingiz muvaffaqiyatli tasdiqlandi!\n"
            "Endi xizmatdan foydalanishingiz mumkin.",
            reply_markup=ReplyKeyboardRemove(),
        )
        
        return ConversationHandler.END
    
    except requests.exceptions.RequestException as e:
        error_message = "Invalid or expired verification code."
        
        if hasattr(e, 'response') and e.response:
            try:
                error_data = e.response.json()
                if 'detail' in error_data:
                    error_message = error_data['detail']
            except json.JSONDecodeError:
                pass
        
        logger.error(f"Verification error for user {telegram_id}: {str(e)}")
        
        await update.message.reply_text(
            f"Xato: {error_message}\n"
            "Qaytadan urinib ko'ring yoki jarayonni qayta boshlash uchun /start tugmasini bosing.",
        )
        
        return VERIFICATION


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Ro'yxatdan o'tish bekor qilindi. /start orqali qayta boshlashingiz mumkin.",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return ConversationHandler.END
