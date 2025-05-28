import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-123')
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mental_health.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS settings
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGIN_WHITELIST = ['http://localhost:3000', 'http://localhost:3001', 'http://localhost:3002']
    CORS_SUPPORTS_CREDENTIALS = True
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-default-key-replace-me')  # Default key for development
    
    if not OPENAI_API_KEY or OPENAI_API_KEY == 'sk-default-key-replace-me':
        print("WARNING: OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file.")
    
    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    
    # Mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Crisis Resources
    EMERGENCY_NUMBER = os.getenv('EMERGENCY_NUMBER', '911')
    CRISIS_HOTLINE = os.getenv('CRISIS_HOTLINE', '1-800-273-8255')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
