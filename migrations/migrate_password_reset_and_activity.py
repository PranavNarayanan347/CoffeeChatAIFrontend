"""Migration script to add password reset and activity tracking fields"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from backend.app import app, db
from backend.models import User, ActivityLog
from sqlalchemy import text

def migrate_password_reset_and_activity():
    """Add password reset and activity tracking fields"""
    with app.app_context():
        print("=" * 60)
        print("Password Reset & Activity Tracking Migration")
        print("=" * 60)
        
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            existing_user_columns = [col['name'] for col in inspector.get_columns('users')]
            
            # Add password reset fields
            password_reset_fields = {
                'password_reset_token': 'VARCHAR(255)',
                'password_reset_expires': 'DATETIME',
                'last_login': 'DATETIME'
            }
            
            columns_to_add = []
            for col_name, col_type in password_reset_fields.items():
                if col_name not in existing_user_columns:
                    columns_to_add.append((col_name, col_type))
                    print(f"  Adding column to users: {col_name} ({col_type})")
                else:
                    print(f"  Column already exists: {col_name}")
            
            # Add new columns to users table
            with db.engine.connect() as connection:
                for col_name, col_type in columns_to_add:
                    connection.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                    connection.commit()
                    print(f"  [OK] Added column: {col_name}")
            
            # Create activity_logs table if it doesn't exist
            existing_tables = inspector.get_table_names()
            
            if 'activity_logs' not in existing_tables:
                print("\n  Creating activity_logs table...")
                db.create_all()
                print("  [OK] activity_logs table created")
            else:
                print("\n  [OK] activity_logs table already exists")
            
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
    success = migrate_password_reset_and_activity()
    exit(0 if success else 1)

