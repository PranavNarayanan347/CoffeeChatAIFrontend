"""Script to make a user an admin"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User

def make_admin(email: str):
    """Make a user an admin by email"""
    with app.app_context():
        user = User.query.filter_by(email=email.lower().strip()).first()
        
        if not user:
            print(f"[FAIL] User with email '{email}' not found")
            return False
        
        if user.is_admin:
            print(f"[INFO] User '{email}' is already an admin")
            return True
        
        user.is_admin = True
        db.session.commit()
        
        print(f"[OK] User '{email}' is now an admin")
        return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python make_admin.py <email>")
        print("\nExample:")
        print("  python make_admin.py admin@example.com")
        sys.exit(1)
    
    email = sys.argv[1]
    success = make_admin(email)
    sys.exit(0 if success else 1)

