from flask import Blueprint, request, jsonify, redirect
from app import db
from app.models.url import URL
from app.utils.validators import validate_url

api_bp = Blueprint('api', __name__)

@api_bp.route('/shorten', methods=['POST'])
def create_short_url():
    """Create a new short URL - POST /shorten"""
    try:
        data = request.get_json()
        
        # Validate request body
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        original_url = data['url'].strip()
        
        # Validate URL format
        if not validate_url(original_url):
            return jsonify({'error': 'Invalid URL format. URL must start with http:// or https://'}), 400
        
        # Check if URL already exists (optional - remove if you want duplicates)
        existing_url = URL.query.filter_by(original_url=original_url).first()
        if existing_url:
            return jsonify(existing_url.to_dict()), 201
        
        # Generate unique short code
        short_code = URL.generate_short_code()
        
        # Create new URL record
        new_url = URL(
            original_url=original_url,
            short_code=short_code
        )
        
        db.session.add(new_url)
        db.session.commit()
        
        return jsonify(new_url.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating short URL: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    """Retrieve original URL - GET /shorten/{shortCode}"""
    try:
        url_record = URL.query.filter_by(short_code=short_code).first()
        
        if not url_record:
            return jsonify({'error': 'Short URL not found'}), 404
        
        # Increment access count
        url_record.access_count += 1
        db.session.commit()
        
        # Return the URL data (as per requirements)
        return jsonify(url_record.to_dict()), 200
        
    except Exception as e:
        print(f"Error retrieving URL: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    """Update an existing short URL - PUT /shorten/{shortCode}"""
    try:
        data = request.get_json()
        
        # Validate request body
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url_record = URL.query.filter_by(short_code=short_code).first()
        
        if not url_record:
            return jsonify({'error': 'Short URL not found'}), 404
        
        new_url = data['url'].strip()
        
        # Validate URL format
        if not validate_url(new_url):
            return jsonify({'error': 'Invalid URL format. URL must start with http:// or https://'}), 400
        
        # Update URL
        url_record.original_url = new_url
        db.session.commit()
        
        return jsonify(url_record.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating URL: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/shorten/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    """Delete a short URL - DELETE /shorten/{shortCode}"""
    try:
        url_record = URL.query.filter_by(short_code=short_code).first()
        
        if not url_record:
            return jsonify({'error': 'Short URL not found'}), 404
        
        db.session.delete(url_record)
        db.session.commit()
        
        return '', 204  # No Content status code
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting URL: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    """Get statistics for a short URL - GET /shorten/{shortCode}/stats"""
    try:
        url_record = URL.query.filter_by(short_code=short_code).first()
        
        if not url_record:
            return jsonify({'error': 'Short URL not found'}), 404
        
        return jsonify(url_record.to_dict()), 200
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Bonus: Direct redirect functionality (browser-friendly)
@api_bp.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to original URL (for browser testing)"""
    try:
        url_record = URL.query.filter_by(short_code=short_code).first()
        
        if not url_record:
            return jsonify({'error': 'Short URL not found'}), 404
        
        # Increment access count
        url_record.access_count += 1
        db.session.commit()
        
        return redirect(url_record.original_url, code=301)
        
    except Exception as e:
        print(f"Error redirecting: {e}")
        return jsonify({'error': 'Internal server error'}), 500