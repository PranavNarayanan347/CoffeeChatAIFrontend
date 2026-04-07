"""Migration script to add profile fields to existing User table"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from backend.app import app, db
from backend.models import User
from sqlalchemy import text

def migrate_user_profile_fields():
    """Add new profile fields to User table"""
    with app.app_context():
        print("=" * 60)
        print("User Profile Fields Migration")
        print("=" * 60)
        
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('users')]
            
            new_columns = {
                'bio': 'TEXT',
                'company': 'VARCHAR(255)',
                'role': 'VARCHAR(255)',
                'linkedin_profile': 'VARCHAR(500)',
                'profile_picture_url': 'VARCHAR(500)',
                'email_verified': 'BOOLEAN DEFAULT 0',
                'preferences': 'TEXT'
            }
            
            columns_to_add = []
            for col_name, col_type in new_columns.items():
                if col_name not in existing_columns:
                    columns_to_add.append((col_name, col_type))
                    print(f"  Adding column: {col_name} ({col_type})")
                else:
                    print(f"  Column already exists: {col_name}")
            
            if not columns_to_add:
                print("\n[OK] All profile fields already exist. Migration not needed.")
                return True
            
            # Add new columns
            with db.engine.connect() as connection:
                for col_name, col_type in columns_to_add:
                    if col_name == 'email_verified':
                        # SQLite specific syntax for boolean
                        connection.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} BOOLEAN DEFAULT 0"))
                    else:
                        connection.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                    connection.commit()
                    print(f"  [OK] Added column: {col_name}")
            
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
    success = migrate_user_profile_fields()
    exit(0 if success else 1)

