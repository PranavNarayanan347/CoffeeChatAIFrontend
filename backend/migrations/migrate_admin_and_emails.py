"""Migration script to add admin field and emails table"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, Email
from sqlalchemy import text, inspect

def migrate_admin_and_emails():
    """Add admin field and create emails table"""
    with app.app_context():
        print("=" * 60)
        print("Admin & Email Tracking Migration")
        print("=" * 60)
        
        try:
            inspector = db.inspect(db.engine)
            existing_user_columns = [col['name'] for col in inspector.get_columns('users')]
            existing_tables = inspector.get_table_names()
            
            # Add is_admin column to users table
            if 'is_admin' not in existing_user_columns:
                print("\n  Adding 'is_admin' column to users table...")
                with db.engine.connect() as connection:
                    connection.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0 NOT NULL"))
                    connection.commit()
                print("  [OK] Added column: is_admin")
            else:
                print("\n  [OK] Column 'is_admin' already exists")
            
            # Create emails table if it doesn't exist
            if 'emails' not in existing_tables:
                print("\n  Creating emails table...")
                db.create_all()
                print("  [OK] emails table created")
            else:
                print("\n  [OK] emails table already exists")
            
            print("\n" + "=" * 60)
            print("[OK] Migration completed successfully!")
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"\n[FAIL] Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = migrate_admin_and_emails()
    exit(0 if success else 1)

