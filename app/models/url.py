from app import db
from datetime import datetime
import string
import random

class URL(db.Model):
    __tablename__ = 'urls'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    access_count = db.Column(db.Integer, default=0, nullable=False)
    
    def __repr__(self):
        return f'<URL {self.short_code}: {self.original_url}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'url': self.original_url,
            'shortCode': self.short_code,
            'createdAt': self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updatedAt': self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'accessCount': self.access_count
        }
    
    @staticmethod
    def generate_short_code(length=6):
        """Generate a random short code"""
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(characters) for _ in range(length))
            # Check if code already exists
            if not URL.query.filter_by(short_code=short_code).first():
                return short_code"# Updated URL model" 
