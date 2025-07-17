# Import required Flask modules and our custom components
from flask import Blueprint, request, jsonify, redirect
from app import db  # Database instance
from app.models.url import URL  # URL model for database operations
from app.utils.validators import validate_url  # URL validation utility

# Create a Blueprint for organizing API routes
# This allows us to group related routes and register them with the main app
api_bp = Blueprint('api', __name__)

@api_bp.route('/shorten', methods=['POST'])
def create_short_url():
    """
    Create a new short URL - POST /shorten
    
    This endpoint accepts a JSON payload with a 'url' field and creates
    a shortened version. It validates the URL format, checks for duplicates,
    generates a unique short code, and stores the mapping in the database.
    
    Request Body:
        {
            "url": "https://www.example.com/very/long/url"
        }
    
    Returns:
        201 Created: Successfully created short URL with full URL data
        400 Bad Request: Invalid or missing URL
        500 Internal Server Error: Database or server error
    """
    try:
        # Extract JSON data from the request body
        data = request.get_json()
        
        # Validate that request contains required data
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        # Clean the URL by removing leading/trailing whitespace
        original_url = data['url'].strip()
        
        # Validate URL format using our custom validator
        if not validate_url(original_url):
            return jsonify({'error': 'Invalid URL format. URL must start with http:// or https://'}), 400
        
        # Check if this URL already exists in our database (prevents duplicates)
        existing_url = URL.query.filter_by(original_url=original_url).first()
        if existing_url:
            # Return existing URL data instead of creating duplicate
            return jsonify(existing_url.to_dict()), 201
        
        # Generate a unique short code for this URL
        short_code = URL.generate_short_code()
        
        # Create new URL record with the original URL and generated short code
        new_url = URL(
            original_url=original_url,
            short_code=short_code
        )
        
        # Add to database session and commit the transaction
        db.session.add(new_url)
        db.session.commit()
        
        # Return the newly created URL data with 201 Created status
        return jsonify(new_url.to_dict()), 201
        
    except Exception as e:
        # Rollback any pending database changes on error
        db.session.rollback()
        print(f"Error creating short URL: {e}")  # Log error for debugging
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    """
    Retrieve original URL from short code - GET /shorten/{shortCode}
    
    This endpoint takes a short code and returns the corresponding original URL
    data. It also increments the access count to track usage statistics.
    
    URL Parameters:
        short_code (str): The unique short code to look up
    
    Returns:
        200 OK: Successfully found URL with updated access count
        404 Not Found: Short code doesn't exist in database
        500 Internal Server Error: Database or server error
    """
    try:
        # Search for URL record with the provided short code
        url_record = URL.query.filter_by(short_code=short_code).first()
        
        # Return 404 if short code doesn't exist
        if not url_record:
            return jsonify({'error': 'Short URL not found'}), 404
        
        # Increment access count to track how many times this URL was accessed
        url_record.access_count += 1
        db.session.commit()  # Save the updated count
        
        # Return the complete URL data including updated access count
        return jsonify(url_record.to_dict()), 200
        
    except Exception as e:
        print(f"Error retrieving URL: {e}")  # Log error for debugging
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    """
    Update an existing short URL - PUT /shorten/{shortCode}
    
    This endpoint allows updating the original URL associated with a short code.
    The short code remains the same, but it will now point to a different URL.
    
    URL Parameters:
        short_code (str): The unique short code to update
        
    Request Body:
        {
            "url": "https://www.new-example.com/updated/url"
        }
    
    Returns:
        200 OK: Successfully updated URL
        400 Bad Request: Invalid or missing URL
        404 Not Found: Short code doesn't exist
        500 Internal Server Error: Database or server error
    """
    try:
        # Extract JSON data from request body
        data = request.get_json()
        
        # Validate that request contains required data
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        # Find the URL record to update
        url_record = URL.query.filter_by(short_code=short_code).first()
        
        # Return 404 if short code doesn't exist
        if not url_record:
            return jsonify({'error': 'Short URL not found'}), 404
        
        # Clean the new URL
        new_url = data['url'].strip()
        
        # Validate the new URL format
        if not validate_url(new_url):
            return jsonify({'error': 'Invalid URL format. URL must start with http:// or https://'}), 400
        
        # Update the original URL field (updated_at will be automatically set)
        url_record.original_url = new_url
        db.session.commit()  # Save changes to database
        
        # Return the updated URL data
        return jsonify(url_record.to_dict()), 200
        
    except Exception as e:
        # Rollback any pending changes on error
        db.session.rollback()
        print(f"Error updating URL: {e}")  # Log error for debugging
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/shorten/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    """
    Delete a short URL - DELETE /shorten/{shortCode}
    
    This endpoint permanently removes a short URL from the database.
    Once deleted, the short code becomes available for reuse.
    
    URL Parameters:
        short_code (str): The unique short code to delete
    
    Returns:
        204 No Content: Successfully deleted (empty response body)
        404 Not Found: Short code doesn't exist
        500 Internal Server Error: Database or server error
    """
    try:
        # Find the URL record to delete
        url_record = URL.query.filter_by(short_code=short_code).first()
        
        # Return 404 if short code doesn't exist
        if not url_record:
            return jsonify({'error': 'Short URL not found'}), 404
        
        # Delete the record from database
        db.session.delete(url_record)
        db.session.commit()  # Commit the deletion
        
        # Return 204 No Content (successful deletion with no response body)
        return '', 204
        
    except Exception as e:
        # Rollback any pending changes on error
        db.session.rollback()
        print(f"Error deleting URL: {e}")  # Log error for debugging
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    """
    Get statistics for a short URL - GET /shorten/{shortCode}/stats
    
    This endpoint returns statistical information about a short URL,
    including access count, creation time, and last update time.
    Note: This does NOT increment the access count (read-only operation).
    
    URL Parameters:
        short_code (str): The unique short code to get stats for
    
    Returns:
        200 OK: Successfully retrieved stats
        404 Not Found: Short code doesn't exist
        500 Internal Server Error: Database or server error
    """
    try:
        # Find the URL record
        url_record = URL.query.filter_by(short_code=short_code).first()
        
        # Return 404 if short code doesn't exist
        if not url_record:
            return jsonify({'error': 'Short URL not found'}), 404
        
        # Return complete URL data (same as GET but without incrementing access count)
        return jsonify(url_record.to_dict()), 200
        
    except Exception as e:
        print(f"Error getting stats: {e}")  # Log error for debugging
        return jsonify({'error': 'Internal server error'}), 500

# Bonus endpoint: Direct redirect functionality for browser usage
@api_bp.route('/<short_code>')
def redirect_to_url(short_code):
    """
    Redirect to original URL - GET /{shortCode}
    
    This endpoint provides browser-friendly redirect functionality.
    When someone visits the short URL in a browser, they are automatically
    redirected to the original URL. This also increments the access count.
    
    URL Parameters:
        short_code (str): The unique short code to redirect
    
    Returns:
        301 Moved Permanently: Redirect to original URL
        404 Not Found: Short code doesn't exist
        500 Internal Server Error: Database or server error
    """
    try:
        # Find the URL record
        url_record = URL.query.filter_by(short_code=short_code).first()
        
        # Return 404 if short code doesn't exist
        if not url_record:
            return jsonify({'error': 'Short URL not found'}), 404
        
        # Increment access count for tracking
        url_record.access_count += 1
        db.session.commit()
        
        # Perform HTTP 301 redirect to the original URL
        return redirect(url_record.original_url, code=301)
        
    except Exception as e:
        print(f"Error redirecting: {e}")  # Log error for debugging
        return jsonify({'error': 'Internal server error'}), 500