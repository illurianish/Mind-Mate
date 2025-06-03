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

def create_default_user():
    """
    Creates a default user (ID=1) for the app if it doesn't exist
    This is needed because the whole app is hardcoded to use user_id=1
    """
    try:
        from models.user import User
        
        # Check if default user already exists
        default_user = User.query.filter_by(id=1).first()
        
        if not default_user:
            # Create a default user for the mental health app
            default_user = User(
                email='default@mindmate.app',
                name='MindMate User',
                password='placeholder'  # Not used since no real auth
            )
            # Force the ID to be 1
            default_user.id = 1
            db.session.add(default_user)
            db.session.commit()
            print("✅ Created default user (ID=1) for the app")
        else:
            print("✅ Default user already exists")
            
    except Exception as e:
        print(f"⚠️ Could not create default user: {str(e)}")

def create_app():
    """
    Creates and configures our Flask app
    This is where the magic happens!
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Set up CORS so our frontend can actually talk to us
    # Without this, browsers get all grumpy about cross-origin requests
    CORS(app, 
         resources={r"/*": {
             "origins": Config.CORS_ORIGIN_WHITELIST,
             "methods": Config.CORS_METHODS,
             "allow_headers": Config.CORS_ALLOW_HEADERS
         }},
         supports_credentials=Config.CORS_SUPPORTS_CREDENTIALS)
    
    # Hook up our database
    db.init_app(app)
    
    # Get the database ready - create tables if they don't exist
    with app.app_context():
        try:
            init_models()
            db.create_all()
            # Create default user for production
            create_default_user()
        except Exception as e:
            # If something goes wrong, at least log it so we know what happened
            app.logger.error(f"Whoops, database setup failed: {str(e)}")
    
    # Wire up all our different route blueprints
    # These handle mood tracking, journaling, CBT exercises, and AI chat
    app.register_blueprint(mood_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(cbt_bp)
    app.register_blueprint(chat_bp)
    
    @app.route('/health')
    def health_check():
        """Simple health check for monitoring - just returns OK if we're alive"""
        return jsonify({"status": "healthy"}), 200
    
    @app.errorhandler(500)
    def handle_500(error):
        """When things go really wrong on our end"""
        return jsonify({"error": "Internal Server Error"}), 500
    
    @app.errorhandler(404)
    def handle_404(error):
        """When someone asks for something that doesn't exist"""
        return jsonify({"error": "Not Found"}), 404
    
    return app

if __name__ == '__main__':
    # Only runs when we start this file directly (not through gunicorn)
    app = create_app()
    port = int(os.getenv('PORT', 5002))  # Use PORT from env or default to 5002
    app.run(host='0.0.0.0', port=port, debug=True)
