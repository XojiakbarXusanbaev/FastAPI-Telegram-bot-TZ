import argparse
import asyncio
import threading
import uvicorn
import logging

from app.telegram_bot.bot import run_bot
from app.main import app as fastapi_app

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_api_server():
    """Run the FastAPI server"""
    logger.info("Starting FastAPI server...")
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)


def run_telegram_bot():
    """Run the Telegram bot"""
    logger.info("Starting Telegram bot...")
    run_bot()


def run_both():
    """Run both the API server and Telegram bot in separate threads"""
    # Create and start API server thread
    api_thread = threading.Thread(target=run_api_server)
    api_thread.daemon = True
    api_thread.start()
    
    # Run Telegram bot in the main thread
    run_telegram_bot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI server and/or Telegram bot")
    parser.add_argument("--api", action="store_true", help="Run only the FastAPI server")
    parser.add_argument("--bot", action="store_true", help="Run only the Telegram bot")
    
    args = parser.parse_args()
    
    if args.api:
        run_api_server()
    elif args.bot:
        run_telegram_bot()
    else:
        run_both()
