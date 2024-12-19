import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Set up logging to see error details if any
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    # Create the inline keyboard with buttons
    keyboard = [
        [InlineKeyboardButton("Owner", callback_data='owner')],
        [InlineKeyboardButton("Sport Group", callback_data='sport_group')],
        [InlineKeyboardButton("Channel", callback_data='channel')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send welcome message with inline buttons
    update.message.reply_text(f"Hi {user.first_name}, welcome to the bot! Choose an option below:", reply_markup=reply_markup)

# Function to handle button press callbacks
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()  # Acknowledge the callback

    # Process the callback based on the button clicked
    if query.data == 'owner':
        query.edit_message_text(text="You pressed 'Owner' button.")
    elif query.data == 'sport_group':
        query.edit_message_text(text="You pressed 'Sport Group' button.")
    elif query.data == 'channel':
        query.edit_message_text(text="You pressed 'Channel' button.")
    elif query.data == 'help':
        query.edit_message_text(text="You pressed 'Help' button. How can I assist you?")
    
# Function to start the bot
def main():
    # Replace 'YOUR_TOKEN' with your actual bot token from BotFather
    updater = Updater("YOUR_TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register /start command handler
    dispatcher.add_handler(CommandHandler("start", start))

    # Register callback query handler for the buttons
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process is stopped
    updater.idle()

if __name__ == '__main__':
    main()
