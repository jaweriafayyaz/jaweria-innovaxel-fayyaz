# Import required modules for URL validation                                                                                                                                         
import re  # Regular Expressions for pattern matching
from urllib.parse import urlparse  # Built-in URL parsing utilities

def validate_url(url):
    """
    Validate if the provided string is a valid URL format.
    
    This function performs comprehensive URL validation using both regex pattern
    matching and Python's built-in urlparse module. It ensures the URL has
    proper protocol, domain structure, and optional components.
    
    The validation checks for:
    - Required protocol (http:// or https://)
    - Valid domain name or IP address
    - Optional port number
    - Optional path and query parameters
    
    Args:
        url (str): The URL string to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
        
    Examples:
        >>> validate_url("https://www.google.com")
        True
        >>> validate_url("invalid-url")
        False
        >>> validate_url("http://localhost:3000/api")
        True
    """
    try:
        # Comprehensive regex pattern for URL validation
        url_pattern = re.compile(
            r'^https?://'  # Must start with http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # Domain name pattern
            r'localhost|'  # Allow localhost for development
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # Allow IP address format
            r'(?::\d+)?'  # Optional port number (e.g., :8080)
            r'(?:/?|[/?]\S+)$',  # Optional path and query parameters
            re.IGNORECASE  # Case-insensitive matching
        )
        
        # First validation: Check against regex pattern
        if not url_pattern.match(url):
            return False
        
        # Second validation: Use Python's built-in URL parser for additional checks
        parsed = urlparse(url)
        
        # Ensure both scheme (http/https) and network location (domain) are present
        return all([parsed.scheme, parsed.netloc])
        
    except Exception:
        # If any exception occurs during validation, consider URL invalid
        return False
