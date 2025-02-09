import logging
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TELEGRAM_TOKEN
from handlers import start_command, help_command, handle_message, button_callback, handle_document
from log_config import setup_logging

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

def init_application():
    """Initialize and configure the application"""
    # Create application instance
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Add callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    # Add document handler
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Add message handler (should be last to catch all other text messages)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return application

async def main():
    """Main function to run the bot"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting bot...")

    # Initialize application
    application = init_application()

    # Start the bot
    logger.info("Bot started, polling for updates...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass