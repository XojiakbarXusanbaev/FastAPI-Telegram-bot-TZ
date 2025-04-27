# FastAPI-Telegram-bot-TZ
📘 Texnik Topshiriq (TZ)
# 📲 Telegram orqali LMS foydalanuvchini ro'yxatdan o'tkazish va tasdiqlash tizimi

Loyiha maqsadi — foydalanuvchilarni **faqat Telegram bot orqali** ro'yxatdan o'tkazish va 1 daqiqalik tasdiqlash kodi bilan `is_verified=True` holatiga olib chiqish. API FastAPI yordamida qurilgan.

---

## 🎯 Loyiha vazifalari

- Foydalanuvchi `/start` bosgach, Telegram orqali `phone_number` va `telegram_id` yuboriladi.
- API foydalanuvchini bazaga qo‘shadi va unga 6 xonali 1 daqiqalik tasdiqlash kodini yuboradi.
- Foydalanuvchi ushbu kodni yuborish orqali o‘zini tasdiqlaydi (`/verify` endpoint orqali).
- Tizim `is_verified=True` holatini saqlaydi.

---

## 🧱 Texnologiyalar

| Texnologiya     | Tavsif                                   |
|------------------|--------------------------------------------|
| FastAPI          | Asosiy API server                          |
| SQLAlchemy / Tortoise ORM | ORM orqali bazani boshqarish      |
| SQLite / Postgres | Ma'lumotlar bazasi                        |
| Telegram Bot SDK  | Telegram bilan integratsiya (`aiogram`, `python-telegram-bot`) |
| Pydantic          | Ma'lumotlar validatsiyasi                 |
| Python-dotenv     | Konfiguratsiya boshqaruvi (.env)          |

---

## ⚙️ API Endpoints

### `POST /register`

Telegramdan olingan foydalanuvchi ma'lumotlarini bazaga yozadi va tasdiqlash kodi yuboradi.

**Request Body**:
```json
{
  "telegram_id": 123456789,
  "phone_number": "+998901234567"
}
```

### Amallar:
Kiritilgan `verification_code` va `telegram_id` ma'lumotlari bazadagi foydalanuvchi bilan solishtiriladi.
Agar kod to‘g‘ri va 1 daqiqa ichida yuborilgan bo‘lsa, `is_verified=True` bo‘ladi.
Aks holda `400 Bad Request` qaytariladi.

### Response (success):
```
{
  "message": "User successfully verified"
}
```
### Response (error):
```
{
  "detail": "Invalid or expired code"
}
```
### 🗃️ Ma'lumotlar bazasi modeli (ORM)

Jadval: `users`
Maydon nomi	Tipi	Tavsif
- id	int (PK)	Avtoinkrement ID
- telegram_id	bigint	Telegram foydalanuvchi ID
- phone_number	string	Telefon raqami
- verification_code	string	6 xonali kod
- expires_at	datetime	Kodning tugash vaqti
- is_verified	boolean	Foydalanuvchi tasdiqlanganmi
  
### ✅ Foydalanish Senariylari
📲 1. Telegramdan boshlash

Foydalanuvchi botda `/start` bosadi → bot telefon raqamini so‘raydi.
Telefon raqami va Telegram ID orqali POST `/register` chaqiriladi.
Foydalanuvchiga Telegram orqali Tasdiqlash kodingiz: `123456` yuboriladi.

### 🔐 2. Kodni tekshirish
Foydalanuvchi kodni kiritadi `(masalan, Telegram orqali "348291")`.
Front yoki bot POST `/verify` endpointini chaqiradi.
Kod to‘g‘ri bo‘lsa → foydalanuvchi `is_verified=True` holatiga o‘tadi.

### 🔒 Qo‘shimcha talablar
Har bir foydalanuvchining telegram_id unikal bo‘lishi shart.
Verification code faqat `1 daqiqa` amal qiladi.
Xatoliklar uchun `HTTPException` formatida javob qaytarilsin.
Kodlar logger orqali loglanishi kerak (opsional).
Kiritilgan kodlar maxfiy va token orqali yuborilmasin (faqat API).

### 📁 Loyihani papkalar tuzilishi (tavsiya)
```
app/
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── crud.py
├── config.py
├── telegram_bot/
│   ├── bot.py
│   └── handlers.py
├── utils/
│   └── code_generator.py
```
### 📦 Paketlar (requirements.txt)
```
fastapi
uvicorn
sqlalchemy
pydantic
python-telegram-bot
python-dotenv
```
- 🧪 Test holatlari
- ✅ To‘g‘ri telefon raqam va Telegram ID bilan ro‘yxatdan o‘tish
- ✅ 1 daqiqa ichida kodni yuborib tasdiqlash
- ❌ Eskirgan yoki noto‘g‘ri kod yuborish
- ❌ Allaqachon `is_verified=True` bo‘lgan foydalanuvchini takror tasdiqlash