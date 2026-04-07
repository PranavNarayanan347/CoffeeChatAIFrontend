"""Authentication utilities for JWT token management"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from werkzeug.security import check_password_hash
from models import User
import re

def validate_password(password):
    """
    Validate password strength
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    
    return True, None

def validate_email(email):
    """
    Validate email format
    Returns: (is_valid, error_message)
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    return True, None

def authenticate_user(email, password):
    """
    Authenticate a user with email and password
    Returns: (user_object, error_message)
    """
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return None, "Invalid email or password"
    
    if not user.check_password(password):
        return None, "Invalid email or password"
    
    return user, None

def get_current_user():
    """
    Get the current authenticated user from JWT token
    Returns: user_object or None
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        if user_id is None:
            return None
        # Convert string ID back to integer for database query
        user = User.query.get(int(user_id))
        return user
    except (ValueError, TypeError) as e:
        # Handle invalid user_id format
        return None
    except Exception:
        return None

def require_admin(f):
    """
    Decorator to require admin access for an endpoint
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            if user_id is None:
                return jsonify({"error": "Invalid token"}), 401
            
            # Convert string ID back to integer for database query
            user = User.query.get(int(user_id))
            
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            if not user.is_admin:
                return jsonify({"error": "Admin access required"}), 403
            
            return f(*args, **kwargs)
        except (ValueError, TypeError) as e:
            return jsonify({"error": "Invalid token format", "message": str(e)}), 401
        except Exception as e:
            return jsonify({"error": "Authentication required", "message": str(e)}), 401
    
    return decorated_function

def require_auth(f):
    """
    Decorator to require authentication for an endpoint
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            if user_id is None:
                return jsonify({"error": "Invalid token"}), 401
            # Convert string ID back to integer for database query
            user = User.query.get(int(user_id))
            
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            # Pass user object to the route handler
            return f(*args, **kwargs, current_user=user)
        except (ValueError, TypeError) as e:
            # Handle invalid user_id format
            return jsonify({"error": "Invalid token format", "message": str(e)}), 401
        except Exception as e:
            return jsonify({"error": "Authentication required", "message": str(e)}), 401
    
    return decorated_function
