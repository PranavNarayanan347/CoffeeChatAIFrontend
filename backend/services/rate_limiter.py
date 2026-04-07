"""Rate limiting service for API endpoints"""
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import os
import json

# Try to import Redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# Configuration
RATE_LIMIT_STORAGE = os.environ.get('RATE_LIMIT_STORAGE', 'memory')  # 'memory' or 'redis'
REDIS_URL = os.environ.get('REDIS_URL')
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_DB = int(os.environ.get('REDIS_DB', '0'))

# Initialize Redis connection if configured
_redis_client = None
if RATE_LIMIT_STORAGE == 'redis' and REDIS_AVAILABLE:
    try:
        if REDIS_URL:
            _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        else:
            _redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                db=REDIS_DB,
                decode_responses=True
            )
        # Test connection
        _redis_client.ping()
        print("[OK] Redis connected for rate limiting")
    except Exception as e:
        print(f"[WARN] Redis connection failed: {e}. Falling back to in-memory storage.")
        _redis_client = None
        RATE_LIMIT_STORAGE = 'memory'

# In-memory rate limit storage (fallback)
_rate_limit_store = defaultdict(list)
_rate_limit_lock = threading.Lock()

def rate_limit(max_requests: int = 5, window_seconds: int = 300, key_func=None):
    """
    Rate limiting decorator with Redis support
    
    Args:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds
        key_func: Function to generate rate limit key (default: uses IP address)
    
    Example:
        @app.route('/api/auth/forgot-password', methods=['POST'])
        @rate_limit(max_requests=3, window_seconds=3600)
        def forgot_password():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate rate limit key
            if key_func:
                key = key_func()
            else:
                # Default: use IP address
                key = request.remote_addr or 'unknown'
            
            # Add endpoint to key for per-endpoint limiting
            endpoint_key = f"rate_limit:{request.endpoint}:{key}"
            
            # Use Redis if available, otherwise use in-memory storage
            if _redis_client and RATE_LIMIT_STORAGE == 'redis':
                try:
                    # Use Redis sorted set for rate limiting
                    now = datetime.utcnow().timestamp()
                    window_start = now - window_seconds
                    
                    # Remove old entries
                    _redis_client.zremrangebyscore(endpoint_key, 0, window_start)
                    
                    # Count current requests
                    current_count = _redis_client.zcard(endpoint_key)
                    
                    if current_count >= max_requests:
                        # Get oldest request time
                        oldest = _redis_client.zrange(endpoint_key, 0, 0, withscores=True)
                        if oldest:
                            oldest_time = oldest[0][1]
                            retry_after = int((oldest_time + window_seconds) - now)
                        else:
                            retry_after = window_seconds
                        
                        return jsonify({
                            "error": "Too many requests. Please try again later.",
                            "retry_after": retry_after
                        }), 429
                    
                    # Add current request
                    _redis_client.zadd(endpoint_key, {str(now): now})
                    # Set expiration
                    _redis_client.expire(endpoint_key, window_seconds)
                    
                except Exception as e:
                    print(f"Warning: Redis rate limiting failed: {e}. Falling back to in-memory.")
                    # Fall through to in-memory implementation
                    pass
            
            # In-memory rate limiting (fallback or default)
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=window_seconds)
            
            with _rate_limit_lock:
                # Clean old entries
                requests = _rate_limit_store[endpoint_key]
                requests[:] = [req_time for req_time in requests if req_time > window_start]
                
                # Check rate limit
                if len(requests) >= max_requests:
                    retry_after = int((requests[0] + timedelta(seconds=window_seconds) - now).total_seconds())
                    return jsonify({
                        "error": "Too many requests. Please try again later.",
                        "retry_after": retry_after
                    }), 429
                
                # Add current request
                requests.append(now)
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def get_rate_limit_key_by_email():
    """Generate rate limit key from email in request body"""
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip().lower()
        if email:
            return f"email:{email}"
    except:
        pass
    return request.remote_addr or 'unknown'

def clear_rate_limits():
    """Clear all rate limits (useful for testing)"""
    global _rate_limit_store
    with _rate_limit_lock:
        _rate_limit_store.clear()

def get_rate_limit_status(key: str) -> dict:
    """Get current rate limit status for a key"""
    with _rate_limit_lock:
        requests = _rate_limit_store.get(key, [])
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=300)  # Default 5 minute window
        recent_requests = [req_time for req_time in requests if req_time > window_start]
        
        return {
            'count': len(recent_requests),
            'limit': 5,  # Default limit
            'window_seconds': 300,
            'reset_at': (recent_requests[0] + timedelta(seconds=300)).isoformat() if recent_requests else None
        }

