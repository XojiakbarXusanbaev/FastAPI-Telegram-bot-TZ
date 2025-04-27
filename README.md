# Telegram Bot orqali Foydalanuvchilarni Ro'yxatdan o'tkazish

Bu loyiha foydalanuvchilarni Telegram bot orqali ro'yxatdan o'tkazish va SMS tasdiqlash kodlari bilan tasdiqlash imkonini beradi.

## Texnologiyalar

- FastAPI - Asosiy API server
- SQLAlchemy - ORM orqali bazani boshqarish
- PostgreSQL - Ma'lumotlar bazasi
- python-telegram-bot - Telegram bilan integratsiya
- Pydantic - Ma'lumotlar validatsiyasi
- Python-dotenv - Konfiguratsiya boshqaruvi (.env)

## O'rnatish

1. Loyihani klonlang:
```bash
git clone https://github.com/username/FastAPI-Telegram-bot-TZ.git
cd FastAPI-Telegram-bot-TZ
```

2. Kerakli paketlarni o'rnating:
```bash
pip install -r requirements.txt
```

3. `.env` faylini yarating va sozlang:
```
# .env.example faylidan nusxa ko'chiring
cp .env.example .env
# .env faylini o'zgartiring va kerakli ma'lumotlarni kiriting
```

4. PostgreSQL ma'lumotlar bazasini yarating:
```bash
createdb telegram_bot_db
```

## Ishga tushirish

API serverni ishga tushirish:
```bash
python run.py --api
```

Telegram botni ishga tushirish:
```bash
python run.py --bot
```

Ikkisini ham bir vaqtda ishga tushirish:
```bash
python run.py
```

## API endpointlari

### `POST /register`

Telegramdan olingan foydalanuvchi ma'lumotlarini bazaga yozadi va tasdiqlash kodi yuboradi.

**Request Body**:
```json
{
  "telegram_id": 123456789,
  "phone_number": "+998901234567"
}
```

**Response (success)**:
```json
{
  "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tkazildi. Tasdiqlash kodi yuborildi."
}
```

### `POST /verify`

Kiritilgan `verification_code` va `telegram_id` ma'lumotlari bazadagi foydalanuvchi bilan solishtiriladi.

**Request Body**:
```json
{
  "telegram_id": 123456789,
  "verification_code": "123456"
}
```

**Response (success)**:
```json
{
  "message": "Foydalanuvchi muvaffaqiyatli tasdiqlandi"
}
```

### `GET /user/{telegram_id}`

Foydalanuvchi ma'lumotlarini olish.

**Response (success)**:
```json
{
  "id": 1,
  "telegram_id": 123456789,
  "phone_number": "+998901234567",
  "is_verified": true
}
```

## Telegram bot buyruqlari

- `/start` - Ro'yxatdan o'tish jarayonini boshlash
- `/cancel` - Ro'yxatdan o'tish jarayonini bekor qilish
