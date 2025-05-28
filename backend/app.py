from flask import Flask
from flask_cors import CORS
from models import init_models
from config import Config
from extensions import db
from routes.mood import mood_bp
from routes.journal import journal_bp
from routes.cbt import cbt_bp
from routes.chat import chat_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    
    # Initialize models
    with app.app_context():
        init_models()
        db.create_all()
    
    # Register blueprints
    app.register_blueprint(mood_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(cbt_bp)
    app.register_blueprint(chat_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5002, debug=True)
