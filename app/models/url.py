# Import required modules for database operations and utilities
from app import db
from datetime import datetime
import string
import random

class URL(db.Model):
    """
    URL Model for storing shortened URLs in the database.
    
    This model represents the main entity for our URL shortener service.
    It stores the original URL, generates a unique short code, and tracks
    access statistics and timestamps.
    """
    
    # Define the table name in the database
    __tablename__ = 'urls'
    
    # Primary key field - auto-incrementing integer ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Store the original long URL that was shortened
    original_url = db.Column(db.Text, nullable=False)
    
    # Store the unique short code (6 characters) with database index for fast lookups
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    
    # Timestamp when the URL was first created
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Timestamp when the URL was last updated (automatically updates on changes)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Counter to track how many times this short URL has been accessed
    access_count = db.Column(db.Integer, default=0, nullable=False)
    
    def __repr__(self):
        """
        String representation of the URL object for debugging purposes.
        
        Returns:
            str: Human-readable representation showing short code and original URL
        """
        return f'<URL {self.short_code}: {self.original_url}>'
    
    def to_dict(self):
        """
        Convert the URL object to a dictionary for JSON responses.
        
        This method formats the URL data according to the API specification
        requirements, ensuring proper date formatting and field names.
        
        Returns:
            dict: Dictionary containing all URL fields formatted for API response
        """
        return {
            'id': str(self.id),  # Convert ID to string as required by API spec
            'url': self.original_url,  # The original long URL
            'shortCode': self.short_code,  # The generated short code
            'createdAt': self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),  # ISO format timestamp
            'updatedAt': self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),  # ISO format timestamp
            'accessCount': self.access_count  # Number of times accessed
        }
    
    @staticmethod
    def generate_short_code(length=6):
        """
        Generate a unique random short code for the URL.
        
        This method creates a random alphanumeric string and ensures it's unique
        by checking against existing codes in the database. If a collision occurs,
        it generates a new code until a unique one is found.
        
        Args:
            length (int): Length of the short code to generate (default: 6)
            
        Returns:
            str: A unique short code that doesn't exist in the database
        """
        # Define character set: letters (both cases) and digits
        characters = string.ascii_letters + string.digits
        
        # Keep generating codes until we find a unique one
        while True:
            # Generate random string of specified length
            short_code = ''.join(random.choice(characters) for _ in range(length))
            
            # Check if this code already exists in the database
            if not URL.query.filter_by(short_code=short_code).first():
                return short_code  # Return the unique code