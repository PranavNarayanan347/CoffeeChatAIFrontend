from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and Stripe integration"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    stripe_customer_id = db.Column(db.String(255), nullable=True, index=True)
    
    # Profile fields
    bio = db.Column(db.Text, nullable=True)  # Bio/description from resume
    company = db.Column(db.String(255), nullable=True)  # Current company
    role = db.Column(db.String(255), nullable=True)  # Current role/title
    linkedin_profile = db.Column(db.String(500), nullable=True)  # LinkedIn URL
    profile_picture_url = db.Column(db.String(500), nullable=True)  # Profile picture URL
    email_verified = db.Column(db.Boolean, default=False, nullable=False)  # Email verification status
    preferences = db.Column(db.Text, nullable=True)  # JSON string for user preferences
    
    # Password reset fields
    password_reset_token = db.Column(db.String(255), nullable=True, index=True)  # Password reset token
    password_reset_expires = db.Column(db.DateTime, nullable=True)  # Token expiration time
    
    # Activity tracking
    last_login = db.Column(db.DateTime, nullable=True)  # Last login timestamp
    
    # Admin role
    is_admin = db.Column(db.Boolean, default=False, nullable=False)  # Admin access flag
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to subscriptions
    subscriptions = db.relationship('Subscription', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def generate_password_reset_token(self):
        """Generate a password reset token"""
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_expires = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
        return self.password_reset_token
    
    def verify_password_reset_token(self, token):
        """Verify if password reset token is valid"""
        if not self.password_reset_token or not self.password_reset_expires:
            return False
        if self.password_reset_token != token:
            return False
        if datetime.utcnow() > self.password_reset_expires:
            return False
        return True
    
    def clear_password_reset_token(self):
        """Clear password reset token after use"""
        self.password_reset_token = None
        self.password_reset_expires = None
    
    def to_dict(self):
        """Convert user to dictionary (exclude password)"""
        import json
        preferences = None
        if self.preferences:
            try:
                preferences = json.loads(self.preferences)
            except:
                preferences = None
        
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'stripe_customer_id': self.stripe_customer_id,
            'bio': self.bio,
            'company': self.company,
            'role': self.role,
            'linkedin_profile': self.linkedin_profile,
            'profile_picture_url': self.profile_picture_url,
            'email_verified': self.email_verified,
            'is_admin': self.is_admin,
            'preferences': preferences,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'


class Subscription(db.Model):
    """Subscription model for tracking Stripe subscriptions"""
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    stripe_subscription_id = db.Column(db.String(255), unique=True, nullable=True, index=True)
    status = db.Column(db.String(50), nullable=False, default='inactive')  # active, canceled, past_due, etc.
    plan_type = db.Column(db.String(100), nullable=True)  # monthly, yearly, etc.
    current_period_end = db.Column(db.DateTime, nullable=True)
    trial_start = db.Column(db.DateTime, nullable=True)  # When trial period started
    trial_period_end = db.Column(db.DateTime, nullable=True)  # When trial period ends
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert subscription to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'stripe_subscription_id': self.stripe_subscription_id,
            'status': self.status,
            'plan_type': self.plan_type,
            'current_period_end': self.current_period_end.isoformat() if self.current_period_end else None,
            'trial_start': self.trial_start.isoformat() if self.trial_start else None,
            'trial_period_end': self.trial_period_end.isoformat() if self.trial_period_end else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_trial_active(self):
        """Check if trial period is currently active"""
        if not self.trial_period_end:
            return False
        return datetime.utcnow() < self.trial_period_end
    
    def is_active(self):
        """Check if subscription is active (either trial or paid)"""
        if self.status == 'active':
            return True
        if self.status == 'trialing' and self.is_trial_active():
            return True
        return False
    
    def __repr__(self):
        return f'<Subscription {self.stripe_subscription_id} - {self.status}>'


class ActivityLog(db.Model):
    """Activity log model for tracking user actions"""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    activity_type = db.Column(db.String(100), nullable=False)  # login, logout, password_reset, etc.
    description = db.Column(db.Text, nullable=True)  # Human-readable description
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6
    user_agent = db.Column(db.String(500), nullable=True)  # Browser/client info
    extra_data = db.Column(db.Text, nullable=True)  # JSON string for additional data
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationship to user
    user = db.relationship('User', backref='activity_logs', lazy=True)
    
    def to_dict(self):
        """Convert activity log to dictionary"""
        import json
        extra_data = None
        if self.extra_data:
            try:
                extra_data = json.loads(self.extra_data)
            except:
                extra_data = None
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'extra_data': extra_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<ActivityLog {self.activity_type} - User {self.user_id}>'


class Email(db.Model):
    """Email tracking model for admin analytics"""
    __tablename__ = 'emails'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Email details
    recipient_email = db.Column(db.String(255), nullable=False, index=True)
    recipient_name = db.Column(db.String(255), nullable=True)
    subject = db.Column(db.String(500), nullable=True)
    email_body = db.Column(db.Text, nullable=True)
    email_type = db.Column(db.String(100), nullable=True)  # cold_outreach, job_inquiry, etc.
    
    # Status tracking
    status = db.Column(db.String(50), nullable=False, default='generated')  # generated, draft_created, sent, failed
    gmail_draft_id = db.Column(db.String(255), nullable=True)  # Gmail draft ID if created
    
    # Metadata
    person_company = db.Column(db.String(255), nullable=True)
    person_role = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to user
    user = db.relationship('User', backref='emails', lazy=True)
    
    def to_dict(self):
        """Convert email to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_email': self.user.email if self.user else None,
            'user_name': self.user.name if self.user else None,
            'recipient_email': self.recipient_email,
            'recipient_name': self.recipient_name,
            'subject': self.subject,
            'email_body': self.email_body,
            'email_type': self.email_type,
            'status': self.status,
            'gmail_draft_id': self.gmail_draft_id,
            'person_company': self.person_company,
            'person_role': self.person_role,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Email {self.recipient_email} - {self.status}>'

