# Configuration class for Flask application settings
# This centralizes all configuration variables in one place

class Config:
    """
    Application configuration class containing all Flask and database settings.
    
    This class stores configuration variables that control how the Flask
    application behaves, including security settings, database connections,
    and other application-specific parameters.
    
    In production, these values should be loaded from environment variables
    or secure configuration files rather than being hardcoded.
    """
    
    # Flask secret key used for session management and security features
    # WARNING: In production, this should be a strong, randomly generated key
    # and should be loaded from environment variables for security
    SECRET_KEY = 'your-secret-key'
    
    # Database connection string for MySQL
    # Format: mysql+pymysql://username:password@host/database_name
    # Components:
    #   - mysql+pymysql: Database dialect and driver
    #   - root: MySQL username
    #   - jiyaHoney17$: MySQL password (should be in environment variable)
    #   - localhost: Database server host
    #   - url_shortener: Database name
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:jiyaHoney17$@localhost/url_shortener'
    
    # Disable SQLAlchemy event tracking to improve performance
    # This feature tracks modifications to objects but is not needed for our use case
    # Setting to False reduces memory usage and improves performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False