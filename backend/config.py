import os
from dotenv import load_dotenv

# Load up any environment variables we have in our .env file
load_dotenv()

class Config:
    """
    All the configuration stuff for our mental health app
    This is where we keep all our secrets and settings!
    """
    
    # Flask secret key - super important for security stuff
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-123')
    
    # Database connection - SQLite for local dev, PostgreSQL for production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///mental_health.db')
    
    # Heroku gives us postgres:// but SQLAlchemy wants postgresql://
    # So we do a little switcheroo here
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    # Turn off modification tracking - we don't need it and it uses extra memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS settings - this lets our frontend talk to our backend
    # Without these, browsers block the requests thinking we're sketchy
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGIN_WHITELIST = [
        'http://localhost:3000',    # Local React dev server
        'http://localhost:3001',    # Backup local port
        'http://localhost:3002',    # Another backup port
        'http://localhost:5002',    # Local Flask dev server
        'https://illurianish.github.io',  # GitHub Pages root
        'https://illurianish.github.io/Mind-Mate',  # Our actual GitHub Pages frontend URL
        'https://mind-mate-fe88.onrender.com'  # Our Render backend URL (for health checks)
    ]
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    
    # OpenAI API key for our AI chat functionality
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Let the user know if they forgot to set up OpenAI
    if not OPENAI_API_KEY:
        print("⚠️  Hey! You need to set up your OpenAI API key for the chat feature to work.")
        print("   Add OPENAI_API_KEY to your environment variables or .env file")
    
    # Google OAuth stuff (not implemented yet but ready for future)
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    
    # Email settings for potential future features like password reset
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Important crisis resources - these are real numbers that could save lives
    EMERGENCY_NUMBER = os.getenv('EMERGENCY_NUMBER', '911')
    CRISIS_HOTLINE = os.getenv('CRISIS_HOTLINE', '988')  # Updated to new 988 crisis line
    
    # JWT tokens for user authentication
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour seems reasonable
    
    # Development vs production settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'  # Only debug in development mode
