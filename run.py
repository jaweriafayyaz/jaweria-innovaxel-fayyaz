# Main application entry point for the URL Shortener API

# Add current directory to Python path to ensure proper module imports
# This is necessary when running the application from different directories
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the application factory function from our app package
from app import create_app

# Create the Flask application instance using the factory pattern
# This calls our create_app() function which configures and returns a Flask app
app = create_app()

# Main execution block - only runs when this file is executed directly
# (not when imported as a module)
if __name__ == '__main__':
    """
    Start the Flask development server.
    
    This configuration is suitable for development and testing:
    - debug=True: Enables debug mode with auto-reload and detailed error pages
    - host='0.0.0.0': Makes server accessible from any network interface
    - port=5000: Standard Flask development port
    
    For production deployment, use a proper WSGI server like Gunicorn or uWSGI
    instead of the built-in development server.
    """
    app.run(debug=True, host='0.0.0.0', port=5000)