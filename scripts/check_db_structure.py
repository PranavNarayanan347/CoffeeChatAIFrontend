"""Check database structure"""
import sqlite3
import os

db_path = 'coffeechat.db'

if os.path.exists(db_path):
    print(f"Database file exists: {db_path}\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("Tables in database:")
    for table in tables:
        table_name = table[0]
        print(f"\n  Table: {table_name}")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print("  Columns:")
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            pk_str = " [PRIMARY KEY]" if pk else ""
            not_null_str = " NOT NULL" if not_null else ""
            default_str = f" DEFAULT {default_val}" if default_val else ""
            print(f"    - {col_name}: {col_type}{not_null_str}{default_str}{pk_str}")
    
    conn.close()
    print("\n[OK] Database structure verified!")
else:
    print(f"[FAIL] Database file not found: {db_path}")

