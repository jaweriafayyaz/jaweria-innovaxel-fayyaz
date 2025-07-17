# Import required Flask modules and configuration
from flask import Flask  # Main Flask application class
from flask_sqlalchemy import SQLAlchemy  # Database ORM extension
from config import Config  # Application configuration settings

# Create global database instance
# This will be initialized with the Flask app in create_app() function
db = SQLAlchemy()

def create_app():
    """
    Application factory function for creating Flask app instances.
    
    This function implements the Flask application factory pattern, which:
    - Creates and configures a Flask application instance
    - Initializes extensions (database, etc.)
    - Registers blueprints (route modules)
    - Sets up database tables
    - Defines basic routes
    
    The factory pattern allows for easier testing and multiple app configurations.
    
    Returns:
        Flask: Configured Flask application instance ready to run
    """
    
    # Create the Flask application instance
    app = Flask(__name__)
    
    # Load configuration from Config class
    # This includes database URI, secret key, and other settings
    app.config.from_object(Config)
    
    # Initialize Flask extensions with the app instance
    # This connects SQLAlchemy to our Flask app
    db.init_app(app)
    
    # Import models here to avoid circular import issues
    # Models need to be imported after db is created but before tables are created
    from app.models.url import URL
    
    # Register blueprints (route modules) with the application
    # This adds all the API routes defined in api.py to our app
    from app.routes.api import api_bp
    app.register_blueprint(api_bp)
    
    # Create database tables within application context
    # This ensures all tables are created when the app starts
    with app.app_context():
        try:
            # Create all database tables based on model definitions
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            # Log any errors during table creation
            print(f"❌ Error creating tables: {e}")
    
    # Define the root route for basic API information
    @app.route('/')
    def home():
        """
        Root endpoint that provides API information and available endpoints.
        
        This serves as a simple health check and documentation endpoint
        that shows all available API operations.
        
        Returns:
            dict: JSON response with API status and endpoint information
        """
        return {
            "message": "URL Shortener API is running!",
            "endpoints": {
                "create": "POST /shorten",  # Create new short URL
                "get": "GET /shorten/{shortCode}",  # Retrieve original URL
                "update": "PUT /shorten/{shortCode}",  # Update existing URL
                "delete": "DELETE /shorten/{shortCode}",  # Delete short URL
                "stats": "GET /shorten/{shortCode}/stats"  # Get URL statistics
            }
        }
    
    # Return the fully configured Flask application
    return app