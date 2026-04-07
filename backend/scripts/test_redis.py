"""Test Redis connection for rate limiting"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_redis_connection():
    """Test Redis connection"""
    print("=" * 60)
    print("Redis Connection Test")
    print("=" * 60)
    
    try:
        import redis
        print("[OK] Redis module is installed")
    except ImportError:
        print("[FAIL] Redis module not installed")
        print("  Install with: pip install redis")
        return False
    
    # Get Redis configuration
    redis_url = os.environ.get('REDIS_URL')
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', '6379'))
    redis_password = os.environ.get('REDIS_PASSWORD')
    redis_db = int(os.environ.get('REDIS_DB', '0'))
    
    print(f"\nConfiguration:")
    if redis_url:
        print(f"  REDIS_URL: {redis_url}")
    else:
        print(f"  REDIS_HOST: {redis_host}")
        print(f"  REDIS_PORT: {redis_port}")
        print(f"  REDIS_DB: {redis_db}")
        print(f"  REDIS_PASSWORD: {'*' * len(redis_password) if redis_password else 'Not set'}")
    
    # Try to connect
    try:
        if redis_url:
            client = redis.from_url(redis_url, decode_responses=True)
        else:
            client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=redis_db,
                decode_responses=True
            )
        
        # Test connection
        client.ping()
        print("\n[OK] Redis connection successful!")
        
        # Test rate limiting operations
        print("\nTesting rate limiting operations...")
        test_key = "test_rate_limit_key"
        
        # Test sorted set operations
        now = 1234567890.0
        client.zadd(test_key, {str(now): now})
        count = client.zcard(test_key)
        print(f"  [OK] Added test entry, count: {count}")
        
        # Test expiration
        client.expire(test_key, 60)
        ttl = client.ttl(test_key)
        print(f"  [OK] Set expiration, TTL: {ttl} seconds")
        
        # Cleanup
        client.delete(test_key)
        print(f"  [OK] Cleaned up test key")
        
        # Get Redis info
        info = client.info('server')
        print(f"\nRedis Server Info:")
        print(f"  Version: {info.get('redis_version', 'Unknown')}")
        print(f"  Uptime: {info.get('uptime_in_seconds', 0)} seconds")
        
        return True
        
    except redis.ConnectionError as e:
        print(f"\n[FAIL] Redis connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Redis server is running")
        print("2. Check host and port are correct")
        print("3. Verify firewall allows connections")
        print("4. Check password if authentication is enabled")
        return False
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        return False

def test_rate_limiting():
    """Test rate limiting functionality"""
    print("\n" + "=" * 60)
    print("Rate Limiting Test")
    print("=" * 60)
    
    try:
        from services.rate_limiter import _redis_client, RATE_LIMIT_STORAGE
        
        if RATE_LIMIT_STORAGE == 'redis' and _redis_client:
            print("[OK] Rate limiting is using Redis")
            return True
        else:
            print(f"[INFO] Rate limiting is using {RATE_LIMIT_STORAGE} storage")
            print("  To use Redis, set RATE_LIMIT_STORAGE=redis in environment")
            return False
    except Exception as e:
        print(f"[FAIL] Error checking rate limiting: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Redis Test Suite")
    print("=" * 60)
    
    connection_ok = test_redis_connection()
    
    if connection_ok:
        test_rate_limiting()
    
    print("\n" + "=" * 60)
    if connection_ok:
        print("[OK] Redis is ready for production use!")
    else:
        print("[FAIL] Please fix Redis configuration before production")
    print("=" * 60)



