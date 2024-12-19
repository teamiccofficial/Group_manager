import os

class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///default.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'your-default-bot-token')  # Add the bot token here
