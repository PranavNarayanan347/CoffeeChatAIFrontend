# Admin Dashboard Documentation

Complete administrative section for tracking emails and managing users.

## ✅ Features Implemented

### 1. Database Models

**Email Model** (`backend/models.py`):
- Tracks all email generation and draft creation
- Fields: recipient, subject, body, status, email_type, user info, timestamps
- Statuses: `generated`, `draft_created`, `sent`, `failed`

**User Model Updates**:
- Added `is_admin` boolean field for admin access control

### 2. Backend API Endpoints

**Admin Endpoints** (all require admin authentication):

- `GET /api/admin/emails` - Get all emails with pagination and filters
  - Query params: `page`, `per_page`, `status`, `email_type`, `user_id`
  
- `GET /api/admin/emails/stats` - Get email statistics
  - Returns: total emails, by status, by type, daily counts, top users, top recipients
  
- `GET /api/admin/users` - Get all users with pagination
  
- `POST /api/admin/users/<user_id>/make-admin` - Make a user an admin

**Email Tracking**:
- Email generation automatically creates Email records
- Gmail draft creation updates Email status to `draft_created`
- All tracked with user, IP, and metadata

### 3. Frontend Admin Dashboard

**Admin Page** (`pages/Admin.tsx`):
- **Statistics Tab**: Overview cards, top users, top recipients, email types breakdown
- **Emails Tab**: List of all emails with filters (status, type), pagination
- **Users Tab**: User list with ability to make users admin

**Navigation**:
- Admin link appears in navigation for admin users only
- Protected route - requires admin access

## 🔐 Admin Access

### Making a User Admin

**Option 1: Via Admin Dashboard**
1. Login as existing admin
2. Go to Admin → Users tab
3. Click "Make Admin" button next to user

**Option 2: Via Database**
```sql
UPDATE users SET is_admin = 1 WHERE email = 'admin@example.com';
```

**Option 3: Via Python Script**
```python
from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(email='admin@example.com').first()
    if user:
        user.is_admin = True
        db.session.commit()
        print(f"User {user.email} is now an admin")
```

## 📊 Email Tracking

### What Gets Tracked

1. **Email Generation**:
   - Recipient email and name
   - Subject and body content
   - Email type (cold_outreach, job_inquiry, etc.)
   - User who generated it
   - Timestamp
   - IP address

2. **Draft Creation**:
   - Gmail draft ID
   - Status updated to `draft_created`
   - Timestamp updated

### Email Statuses

- `generated` - Email was generated but not sent to Gmail
- `draft_created` - Gmail draft was successfully created
- `sent` - Email was sent (future feature)
- `failed` - Email generation or draft creation failed

## 🎨 Admin Dashboard Features

### Statistics View

- **Overview Cards**: Total emails, generated count, drafts created, top users count
- **Top Users**: Users who generated the most emails
- **Top Recipients**: Most contacted email addresses
- **Email Types**: Breakdown by email type (cold_outreach, job_inquiry, etc.)
- **Daily Counts**: Email generation trends over last 30 days

### Emails View

- **Filters**: By status, by email type
- **Pagination**: 20 emails per page
- **Email Details**: Shows recipient, sender, subject, company, role, status, timestamp
- **Status Badges**: Color-coded status indicators

### Users View

- **User List**: All registered users
- **Admin Badge**: Shows which users are admins
- **Make Admin**: Button to grant admin access
- **User Info**: Email, name, last login

## 🔧 Usage

### Accessing Admin Dashboard

1. **Login** as an admin user
2. **Click "Admin"** in the navigation bar (only visible to admins)
3. **View statistics**, emails, or manage users

### Filtering Emails

- Use dropdown filters to filter by:
  - Status (generated, draft_created, sent, failed)
  - Email type (cold_outreach, job_inquiry, etc.)

### Making Users Admin

1. Go to Admin → Users tab
2. Find the user you want to make admin
3. Click "Make Admin" button
4. User will immediately have admin access

## 📁 Files Created/Modified

### New Files
- `pages/Admin.tsx` - Admin dashboard component
- `services/admin.ts` - Admin API service
- `backend/migrations/migrate_admin_and_emails.py` - Database migration

### Modified Files
- `backend/models.py` - Added Email model and is_admin field
- `backend/app.py` - Added admin endpoints and email tracking
- `backend/auth.py` - Added `require_admin` decorator
- `App.tsx` - Added admin route and navigation
- `components/Navigation.tsx` - Added admin link for admin users
- `services/auth.ts` - Added is_admin to User interface

## 🚀 Next Steps

### Potential Enhancements

1. **Email Analytics**:
   - Response rate tracking
   - Open rate tracking (if email service supports)
   - Click-through rate

2. **Advanced Filtering**:
   - Date range filters
   - Search by recipient name/email
   - Export to CSV

3. **User Management**:
   - Suspend/activate users
   - View user activity logs
   - User statistics

4. **Real-time Updates**:
   - WebSocket for live stats
   - Auto-refresh dashboard

5. **Email Preview**:
   - View full email content in modal
   - Edit email before sending

## 🔒 Security Notes

- Admin endpoints protected with `@require_admin` decorator
- Frontend checks `is_admin` before showing admin link
- Admin routes protected in App.tsx
- All admin actions logged in activity logs

## 📝 Notes

- First admin must be created manually via database or script
- Email tracking starts automatically when emails are generated
- All email data is stored securely in database
- Admin dashboard requires authentication + admin role


