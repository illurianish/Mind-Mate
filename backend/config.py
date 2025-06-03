import os
from dotenv import load_dotenv

# Load up any environment variables we have in our .env file
load_dotenv()

class Config:
    """
    All the configuration stuff for our mental health app - SIMPLIFIED
    """
    
    # Flask secret key - super important for security stuff
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-123')
    
    # Database connection - Use the provided PostgreSQL URL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 
        'postgresql://mindmate_database_user:YFmc7ebd3NHBFYEMcB8C4yTYKdLoiU1V@dpg-d0vjs66mcj7s73ena0sg-a.ohio-postgres.render.com/mindmate_database')
    
    # Heroku/Render gives us postgres:// but SQLAlchemy wants postgresql://
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    # Turn off modification tracking - we don't need it and it uses extra memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS settings - SIMPLIFIED for debugging
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGIN_WHITELIST = [
        'http://localhost:3000',    # Local React dev server
        'http://localhost:5002',    # Local Flask dev server
        'https://illurianish.github.io',  # GitHub Pages root
        'https://illurianish.github.io/Mind-Mate',  # Our actual GitHub Pages frontend URL
        'https://mind-mate-fe88.onrender.com'  # Our Render backend URL
    ]
    CORS_SUPPORTS_CREDENTIALS = False  # Simplified
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    
    # OpenAI API key for our AI chat functionality
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Let the user know if they forgot to set up OpenAI
    if not OPENAI_API_KEY:
        print("⚠️  Hey! You need to set up your OpenAI API key for the chat feature to work.")
        print("   Add OPENAI_API_KEY to your environment variables")
    
    # Development vs production settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'
