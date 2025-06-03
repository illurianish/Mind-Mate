from flask import Flask, jsonify
from flask_cors import CORS
from models import init_models
from config import Config
from extensions import db
from routes.mood import mood_bp
from routes.journal import journal_bp
from routes.cbt import cbt_bp
from routes.chat import chat_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app, 
         resources={r"/*": {
             "origins": Config.CORS_ORIGIN_WHITELIST,
             "methods": Config.CORS_METHODS,
             "allow_headers": Config.CORS_ALLOW_HEADERS
         }},
         supports_credentials=Config.CORS_SUPPORTS_CREDENTIALS)
    
    db.init_app(app)
    
    # Initialize models
    with app.app_context():
        try:
            init_models()
            db.create_all()
        except Exception as e:
            app.logger.error(f"Database initialization error: {str(e)}")
    
    # Register blueprints
    app.register_blueprint(mood_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(cbt_bp)
    app.register_blueprint(chat_bp)
    
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200
    
    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({"error": "Internal Server Error"}), 500
    
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({"error": "Not Found"}), 404
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5002))
    app.run(host='0.0.0.0', port=port)
