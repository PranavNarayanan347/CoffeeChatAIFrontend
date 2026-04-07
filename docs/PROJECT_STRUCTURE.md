# Project Structure

This document describes the organized structure of the CoffeeChat AI codebase.

## Directory Organization

```
CoffeeChatAIFrontend/
├── backend/                 # Backend Flask application
│   ├── __init__.py
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models (User, Subscription, ActivityLog)
│   ├── auth.py             # Authentication utilities
│   └── services/           # Backend services
│       ├── __init__.py
│       ├── ai_people_search.py    # Core AI people search functionality
│       ├── ai_search_class.py     # AI search class utilities
│       ├── stripe_service.py      # Stripe payment integration
│       ├── resume_parser.py       # Resume parsing service
│       ├── email_verifier.py      # Email verification service
│       ├── pdl_integration.py    # People Data Labs integration
│       ├── email_service.py      # Email service utilities
│       └── rate_limiter.py       # Rate limiting utilities
│
├── scripts/                 # Utility scripts
│   ├── check_account.py
│   ├── check_db_structure.py
│   ├── get_person.py
│   ├── unlock_emails.py
│   └── unlock_email_final.py
│
├── migrations/              # Database migration scripts
│   ├── migrate_password_reset_and_activity.py
│   └── migrate_user_profile_fields.py
│
├── tests/                   # Test files
│   └── test_password_reset.py
│
├── docs/                    # Documentation
│   ├── Attributions.md
│   ├── FEATURES_SUMMARY.md
│   ├── FULL_STACK_README.md
│   ├── GMAIL_SETUP.md
│   ├── POSTGRESQL_MIGRATION.md
│   └── PROJECT_STRUCTURE.md (this file)
│
├── components/              # React frontend components
├── pages/                   # React page components
├── services/                # Frontend services (TypeScript)
├── styles/                  # CSS styles
│
├── app.py                   # (moved to backend/app.py)
├── models.py                # (moved to backend/models.py)
├── auth.py                  # (moved to backend/auth.py)
└── README.md                # Main project README
```

## Running the Application

### Backend
From the project root:
```bash
python backend/app.py
```

Or use the startup scripts:
- Windows: `start.bat`
- Linux/Mac: `start.sh`

### Migrations
From the project root:
```bash
python migrations/migrate_password_reset_and_activity.py
python migrations/migrate_user_profile_fields.py
```

### Tests
From the project root:
```bash
python tests/test_password_reset.py
```

## Import Paths

### Backend Imports
When importing from `backend/app.py`:
```python
from models import User, Subscription, ActivityLog
from auth import validate_password, validate_email
from services.ai_people_search import process_user_request
from services.stripe_service import create_stripe_customer
from services.resume_parser import parse_resume_file
```

### Migration Scripts
Migration scripts should import from backend:
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from backend.app import app, db
from backend.models import User
```

## Notes

- All Python backend code is now organized in the `backend/` directory
- Service modules are in `backend/services/`
- Utility scripts are in `scripts/`
- Database migrations are in `migrations/`
- Tests are in `tests/`
- Documentation is in `docs/`
- The main `README.md` stays at the root for GitHub visibility



