# PostgreSQL Migration Guide

This guide explains how to migrate from SQLite (development) to PostgreSQL (production).

## Why PostgreSQL?

- **Concurrent Connections**: SQLite has limitations with concurrent writes
- **Scalability**: Better performance for production workloads
- **Advanced Features**: Full SQL support, better indexing, transactions
- **Production Ready**: Industry standard for production applications

## Prerequisites

1. PostgreSQL installed and running
2. Database created for the application
3. User credentials with appropriate permissions

## Step 1: Install PostgreSQL Dependencies

```bash
pip install psycopg2-binary
```

Or for Python 3.11+:
```bash
pip install psycopg2-binary
```

## Step 2: Create PostgreSQL Database

```sql
-- Connect to PostgreSQL as superuser
CREATE DATABASE coffeechat_db;
CREATE USER coffeechat_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE coffeechat_db TO coffeechat_user;
```

## Step 3: Update Environment Variables

Create a `.env` file or set environment variables:

```bash
# Development (SQLite)
DATABASE_URL=sqlite:///coffeechat.db

# Production (PostgreSQL)
DATABASE_URL=postgresql://coffeechat_user:your_secure_password@localhost:5432/coffeechat_db
```

## Step 4: Update backend/app.py Configuration

The app already supports DATABASE_URL environment variable:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'coffeechat.db')
```

Just set the `DATABASE_URL` environment variable to your PostgreSQL connection string.

## Step 5: Migrate Data (Optional)

If you have existing SQLite data to migrate:

### Option A: Using SQLAlchemy (Recommended)

```python
# migrate_to_postgresql.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from backend.app import app, db
from backend.models import User, Subscription, ActivityLog

# SQLite connection
sqlite_uri = 'sqlite:///coffeechat.db'
sqlite_engine = create_engine(sqlite_uri)

# PostgreSQL connection
postgres_uri = os.environ.get('DATABASE_URL')
postgres_engine = create_engine(postgres_uri)

with app.app_context():
    # Create tables in PostgreSQL
    db.create_all()
    
    # Migrate Users
    with sqlite_engine.connect() as sqlite_conn:
        users = sqlite_conn.execute(text("SELECT * FROM users")).fetchall()
        
        for user_row in users:
            # Convert SQLite row to User object and insert into PostgreSQL
            # (Implementation depends on your specific schema)
            pass
```

### Option B: Using pgloader (Linux/Mac)

```bash
# Install pgloader
sudo apt-get install pgloader  # Ubuntu/Debian
brew install pgloader  # macOS

# Migrate data
pgloader sqlite:///path/to/coffeechat.db postgresql://user:pass@localhost/coffeechat_db
```

## Step 6: Update Requirements

Add to `requirements.txt`:

```
psycopg2-binary>=2.9.0
```

## Step 7: Test Connection

```python
# test_postgresql_connection.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from backend.app import app, db
from backend.models import User

with app.app_context():
    try:
        # Test connection
        db.engine.execute(text("SELECT 1"))
        print("[OK] PostgreSQL connection successful")
        
        # Test query
        user_count = User.query.count()
        print(f"[OK] Found {user_count} users in database")
    except Exception as e:
        print(f"[FAIL] Connection failed: {e}")
```

## Production Deployment

### Environment Variables

Set these in your production environment:

```bash
DATABASE_URL=postgresql://user:password@host:5432/database
JWT_SECRET_KEY=your-secret-key-here
STRIPE_SECRET_KEY=sk_live_...
OPENAI_API_KEY=sk-...
```

### Connection Pooling

For production, consider using connection pooling:

```python
from sqlalchemy.pool import QueuePool

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 10,
    'max_overflow': 20,
    'pool_pre_ping': True  # Verify connections before using
}
```

### SSL Connection (Recommended for Production)

```python
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```

## Differences Between SQLite and PostgreSQL

1. **Boolean Types**: PostgreSQL uses `BOOLEAN`, SQLite uses `INTEGER` (0/1)
2. **DateTime**: Both support DATETIME, but PostgreSQL has better timezone support
3. **String Length**: PostgreSQL VARCHAR is more efficient than SQLite TEXT
4. **Transactions**: PostgreSQL has better transaction isolation

## Troubleshooting

### Connection Refused
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify connection string format
- Check firewall settings

### Authentication Failed
- Verify username and password
- Check `pg_hba.conf` configuration
- Ensure user has proper permissions

### Encoding Issues
- Ensure database uses UTF-8 encoding
- Set client encoding: `SET client_encoding TO 'UTF8';`

## Rollback Plan

If migration fails:

1. Keep SQLite database as backup
2. Test PostgreSQL migration in staging first
3. Have rollback script ready to switch back to SQLite
4. Monitor application logs after migration

## Best Practices

1. **Backup First**: Always backup SQLite database before migration
2. **Test in Staging**: Test PostgreSQL migration in staging environment first
3. **Monitor Performance**: Watch query performance after migration
4. **Index Optimization**: Review and optimize indexes for PostgreSQL
5. **Connection Limits**: Set appropriate connection pool sizes
6. **Regular Backups**: Set up automated PostgreSQL backups

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy PostgreSQL Dialect](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

