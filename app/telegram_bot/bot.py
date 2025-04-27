import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
import requests

from app.config import TELEGRAM_API_TOKEN
from app.telegram_bot.handlers import start, request_phone, handle_phone, handle_verification_code, cancel

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

PHONE, VERIFICATION = range(2)


def create_bot_application():
    if not TELEGRAM_API_TOKEN:
        logger.error("Telegram API token is not set. Please set TELEGRAM_API_TOKEN in .env file.")
        return None
    
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHONE: [
                MessageHandler(filters.CONTACT, handle_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, request_phone)
            ],
            VERIFICATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_verification_code)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(conv_handler)
    
    application.add_error_handler(error_handler)
    
    return application


def error_handler(update, context):
    logger.error(f"Update {update} caused error {context.error}")


def run_bot():
    application = create_bot_application()
    if application:
        application.run_polling()
    else:
        logger.error("Failed to create bot application. Exiting.")


if __name__ == "__main__":
    run_bot()
