from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Import models here to avoid circular imports
    from app.models.url import URL
    
    # Register blueprints
    from app.routes.api import api_bp
    app.register_blueprint(api_bp)
    
    # Create tables within app context
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
    
    @app.route('/')
    def home():
        return {
            "message": "URL Shortener API is running!",
            "endpoints": {
                "create": "POST /shorten",
                "get": "GET /shorten/{shortCode}",
                "update": "PUT /shorten/{shortCode}",
                "delete": "DELETE /shorten/{shortCode}",
                "stats": "GET /shorten/{shortCode}/stats"
            }
        }
    
    return app