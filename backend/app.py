from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt
import json
import os
import secrets
from datetime import timedelta, datetime
import stripe
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from services.ai_people_search import process_user_request, generate_email, create_gmail_draft, update_email_content
from models import db, User, Subscription, ActivityLog, Email
from auth import validate_password, validate_email, authenticate_user, require_admin
from services.stripe_service import (
    create_stripe_customer, 
    is_stripe_configured,
    create_checkout_session,
    get_subscription_status,
    create_portal_session
)
from services.resume_parser import parse_resume_file
from services.email_service import send_password_reset_email, is_email_configured
from services.rate_limiter import rate_limit, get_rate_limit_key_by_email
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'coffeechat.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or secrets.token_urlsafe(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Configuration
API_BASE_URL = "http://localhost:5000"

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "CoffeeChat AI Backend is running"})

@app.route('/api/search-people', methods=['POST'])
@jwt_required()
def search_people():
    """Search for people based on user query"""
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({"error": "Query is required"}), 400
        
        # Process the user request using the existing function
        results = process_user_request(user_query)
        
        return jsonify({
            "success": True,
            "query": user_query,
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@app.route('/api/generate-email', methods=['POST'])
@jwt_required()
def generate_email_endpoint():
    """Generate personalized email for a person"""
    try:
        data = request.get_json()
        
        person_info = data.get('person_info', {})
        email_type = data.get('email_type', 'cold_outreach')
        custom_message = data.get('custom_message', '')
        
        if not person_info:
            return jsonify({"error": "Person information is required"}), 400
        
        # Generate email using the existing function
        email_content = generate_email(person_info, email_type, custom_message)
        
        # Track email generation
        try:
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            if user:
                ip_address = request.remote_addr
                user_agent = request.headers.get('User-Agent', '')
                recipient = person_info.get('work_email', person_info.get('personal_email', 'N/A'))
                
                # Create Email record
                email_record = Email(
                    user_id=user.id,
                    recipient_email=recipient,
                    recipient_name=person_info.get('name', 'Unknown'),
                    subject=f"{email_type.replace('_', ' ').title()} - {person_info.get('name', 'Contact')}",
                    email_body=email_content,
                    email_type=email_type,
                    status='generated',
                    person_company=person_info.get('company', ''),
                    person_role=person_info.get('title', ''),
                    ip_address=ip_address
                )
                db.session.add(email_record)
                
                # Create activity log
                activity_log = ActivityLog(
                    user_id=user.id,
                    activity_type='email_generated',
                    description=f'Email generated for {recipient}',
                    ip_address=ip_address,
                    user_agent=user_agent,
                    extra_data=json.dumps({
                        'email_type': email_type,
                        'recipient': recipient,
                        'person_name': person_info.get('name', 'Unknown'),
                        'email_id': email_record.id
                    })
                )
                db.session.add(activity_log)
                db.session.commit()
        except Exception as log_error:
            print(f"Warning: Failed to log email: {log_error}")
            db.session.rollback()
        
        return jsonify({
            "success": True,
            "email_content": email_content,
            "email_type": email_type,
            "recipient": person_info.get('work_email', person_info.get('personal_email', 'N/A'))
        })
        
    except Exception as e:
        return jsonify({"error": f"Email generation failed: {str(e)}"}), 500

@app.route('/api/create-gmail-draft', methods=['POST'])
@jwt_required()
def create_gmail_draft_endpoint():
    """Create Gmail draft from generated email"""
    try:
        data = request.get_json()
        
        to_email = data.get('to_email', '')
        subject = data.get('subject', '')
        body = data.get('body', '')
        
        if not all([to_email, subject, body]):
            return jsonify({"error": "Email, subject, and body are required"}), 400
        
        # Create Gmail draft using the existing function
        result = create_gmail_draft(to_email, subject, body)
        
        # Update email record if draft was created successfully
        if result.get('success') and result.get('draft_id'):
            try:
                user_id = get_jwt_identity()
                user = User.query.get(int(user_id))
                if user:
                    # Find the most recent email for this recipient by this user
                    email_record = Email.query.filter_by(
                        user_id=user.id,
                        recipient_email=to_email,
                        status='generated'
                    ).order_by(Email.created_at.desc()).first()
                    
                    if email_record:
                        email_record.status = 'draft_created'
                        email_record.gmail_draft_id = result.get('draft_id')
                        email_record.subject = subject
                        db.session.commit()
            except Exception as update_error:
                print(f"Warning: Failed to update email record: {update_error}")
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Draft creation failed: {str(e)}"}), 500

@app.route('/api/update-email', methods=['POST'])
@jwt_required()
def update_email_endpoint():
    """Update an existing email based on user instructions"""
    try:
        data = request.get_json()
        
        original_email = data.get('original_email', '')
        person_info = data.get('person_info', {})
        update_instructions = data.get('update_instructions', '')
        email_type = data.get('email_type', 'cold_outreach')
        
        if not all([original_email, person_info, update_instructions]):
            return jsonify({"error": "Original email, person info, and update instructions are required"}), 400
        
        # Generate updated email using OpenAI with context
        updated_email = update_email_content(original_email, person_info, update_instructions, email_type)
        
        return jsonify({
            "success": True,
            "updated_email": updated_email,
            "person_info": person_info
        })
        
    except Exception as e:
        return jsonify({"error": f"Email update failed: {str(e)}"}), 500

@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat_endpoint():
    """Main chat endpoint that handles people search"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Process the user request
        search_results = process_user_request(user_message)
        
        # Check if search_results is an error or message dict
        if isinstance(search_results, dict):
            if 'error' in search_results:
                return jsonify({
                    "success": False,
                    "error": search_results.get('error', 'Search failed'),
                    "message": user_message,
                    "search_results": [],
                    "count": 0
                }), 500
            elif 'message' in search_results:
                return jsonify({
                    "success": True,
                    "message": user_message,
                    "search_results": [],
                    "count": 0,
                    "info": search_results.get('message', 'No results found')
                })
        
        # Simplify the results to only include required fields
        simplified_results = []
        if isinstance(search_results, list):
            for person in search_results:
                simplified_person = {
                    "name": person.get('name', 'N/A'),
                    "title": person.get('title', 'N/A'),
                    "company": person.get('company', 'N/A'),
                    "work_email": person.get('work_email', 'N/A'),
                    "personal_email": person.get('personal_email', 'N/A'),
                    "linkedin": person.get('linkedin', 'N/A'),
                    "education": person.get('education', [])
                }
                simplified_results.append(simplified_person)
        
        return jsonify({
            "success": True,
            "message": user_message,
            "search_results": simplified_results,
            "count": len(simplified_results)
        })
        
    except Exception as e:
        return jsonify({"error": f"Chat processing failed: {str(e)}"}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Validate input
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        if not password:
            return jsonify({"error": "Password is required"}), 400
        
        # Validate email format
        is_valid_email, email_error = validate_email(email)
        if not is_valid_email:
            return jsonify({"error": email_error}), 400
        
        # Validate password strength
        is_valid_password, password_error = validate_password(password)
        if not is_valid_password:
            return jsonify({"error": password_error}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 409
        
        # Create Stripe customer (if Stripe is configured)
        stripe_customer_id = None
        stripe_error = None
        
        if is_stripe_configured():
            stripe_result = create_stripe_customer(email, name)
            if stripe_result.get('success'):
                stripe_customer_id = stripe_result['customer']['id']
            else:
                # Log error but don't fail registration if Stripe fails
                stripe_error = stripe_result.get('error', 'Unknown Stripe error')
                print(f"Warning: Stripe customer creation failed: {stripe_error}")
        else:
            print("Info: Stripe not configured, skipping customer creation")
        
        # Create new user
        new_user = User(
            email=email,
            name=name if name else None,
            stripe_customer_id=stripe_customer_id
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate JWT token (identity must be string)
        access_token = create_access_token(identity=str(new_user.id))
        
        response_data = {
            "success": True,
            "message": "User registered successfully",
            "user": new_user.to_dict(),
            "access_token": access_token
        }
        
        # Include Stripe status in response
        if stripe_customer_id:
            response_data["stripe_customer_created"] = True
        elif stripe_error:
            response_data["stripe_customer_created"] = False
            response_data["stripe_warning"] = stripe_error
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Authenticate user
        user, error = authenticate_user(email, password)
        if not user:
            return jsonify({"error": error}), 401
        
        # Update last login timestamp
        user.last_login = datetime.utcnow()
        
        # Create activity log
        try:
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            activity_log = ActivityLog(
                user_id=user.id,
                activity_type='login',
                description=f'User logged in from {ip_address}',
                ip_address=ip_address,
                user_agent=user_agent
            )
            db.session.add(activity_log)
        except Exception as log_error:
            # Don't fail login if activity logging fails
            print(f"Warning: Failed to log activity: {log_error}")
        
        db.session.commit()
        
        # Generate JWT token (identity must be string)
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": user.to_dict(),
            "access_token": access_token
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout endpoint (client-side token removal)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        # Create activity log
        if user:
            try:
                ip_address = request.remote_addr
                user_agent = request.headers.get('User-Agent', '')
                activity_log = ActivityLog(
                    user_id=user.id,
                    activity_type='logout',
                    description='User logged out',
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                db.session.add(activity_log)
                db.session.commit()
            except Exception as log_error:
                print(f"Warning: Failed to log activity: {log_error}")
        
        # Since we're using stateless JWT tokens, logout is handled client-side
        # In a production app, you might want to implement token blacklisting
        return jsonify({
            "success": True,
            "message": "Logged out successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "success": True,
            "message": "Logged out successfully"
        }), 200

@app.route('/api/auth/forgot-password', methods=['POST'])
@rate_limit(max_requests=3, window_seconds=3600, key_func=get_rate_limit_key_by_email)  # 3 requests per hour per email
def forgot_password():
    """Request password reset - sends email with reset link"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        # Validate email format
        is_valid_email, email_error = validate_email(email)
        if not is_valid_email:
            return jsonify({"error": email_error}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        # Always return success message (security best practice - don't reveal if email exists)
        if user:
            # Generate reset token
            reset_token = user.generate_password_reset_token()
            db.session.commit()
            
            # Send password reset email
            email_result = send_password_reset_email(email, reset_token, user.name)
            
            # Log activity
            try:
                ip_address = request.remote_addr
                user_agent = request.headers.get('User-Agent', '')
                activity_log = ActivityLog(
                    user_id=user.id,
                    activity_type='password_reset_requested',
                    description='Password reset requested',
                    ip_address=ip_address,
                    user_agent=user_agent,
                    extra_data=json.dumps({'email_sent': email_result.get('success', False)})
                )
                db.session.add(activity_log)
                db.session.commit()
            except Exception as log_error:
                print(f"Warning: Failed to log activity: {log_error}")
            
            # In development/testing, return token if email not configured
            response_data = {
                "success": True,
                "message": "If an account with that email exists, a password reset link has been sent."
            }
            
            # Only include token in development (when email not configured)
            if not is_email_configured():
                response_data["reset_token"] = reset_token
                response_data["dev_mode"] = True
                response_data["warning"] = "Email service not configured. Token included for testing only."
            
            return jsonify(response_data), 200
        else:
            # Still return success for security (don't reveal if email exists)
            return jsonify({
                "success": True,
                "message": "If an account with that email exists, a password reset link has been sent."
            }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to process password reset request: {str(e)}"}), 500

@app.route('/api/auth/reset-password', methods=['POST'])
@rate_limit(max_requests=5, window_seconds=3600)  # 5 attempts per hour per IP
def reset_password():
    """Reset password using reset token"""
    try:
        data = request.get_json()
        token = data.get('token', '').strip()
        new_password = data.get('password', '')
        email = data.get('email', '').strip().lower()
        
        if not token or not new_password:
            return jsonify({"error": "Token and password are required"}), 400
        
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        # Find user by email and token
        user = User.query.filter_by(email=email, password_reset_token=token).first()
        
        if not user:
            return jsonify({"error": "Invalid or expired reset token"}), 400
        
        # Verify token is valid and not expired
        if not user.verify_password_reset_token(token):
            return jsonify({"error": "Invalid or expired reset token"}), 400
        
        # Validate new password
        is_valid_password, password_error = validate_password(new_password)
        if not is_valid_password:
            return jsonify({"error": password_error}), 400
        
        # Update password
        user.set_password(new_password)
        user.clear_password_reset_token()
        
        # Create activity log
        try:
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            activity_log = ActivityLog(
                user_id=user.id,
                activity_type='password_reset',
                description='Password reset completed',
                ip_address=ip_address,
                user_agent=user_agent
            )
            db.session.add(activity_log)
        except Exception as log_error:
            print(f"Warning: Failed to log activity: {log_error}")
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Password reset successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to reset password: {str(e)}"}), 500

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user information"""
    try:
        user_id = get_jwt_identity()
        # Convert string ID back to integer for database query
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get user: {str(e)}"}), 500

@app.route('/api/auth/activity', methods=['GET'])
@jwt_required()
def get_user_activity():
    """Get activity logs for current user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        activity_type = request.args.get('type', None)
        
        # Build query
        query = ActivityLog.query.filter_by(user_id=user.id)
        
        if activity_type:
            query = query.filter_by(activity_type=activity_type)
        
        # Order by most recent first
        logs = query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
        
        return jsonify({
            "success": True,
            "activities": [log.to_dict() for log in logs],
            "count": len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get activity logs: {str(e)}"}), 500

@app.route('/api/auth/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile information"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            user.name = data['name'].strip() if data['name'] else None
        if 'bio' in data:
            user.bio = data['bio'].strip() if data['bio'] else None
        if 'company' in data:
            user.company = data['company'].strip() if data['company'] else None
        if 'role' in data:
            user.role = data['role'].strip() if data['role'] else None
        if 'linkedin_profile' in data:
            user.linkedin_profile = data['linkedin_profile'].strip() if data['linkedin_profile'] else None
        if 'profile_picture_url' in data:
            user.profile_picture_url = data['profile_picture_url'].strip() if data['profile_picture_url'] else None
        if 'preferences' in data:
            user.preferences = json.dumps(data['preferences']) if data['preferences'] else None
        
        # Track updated fields
        updated_fields = [key for key in ['name', 'bio', 'company', 'role', 'linkedin_profile', 'profile_picture_url', 'preferences'] if key in data]
        
        # Create activity log
        try:
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            activity_log = ActivityLog(
                user_id=user.id,
                activity_type='profile_update',
                description=f'Profile updated: {", ".join(updated_fields)}',
                ip_address=ip_address,
                user_agent=user_agent,
                extra_data=json.dumps({'updated_fields': updated_fields})
            )
            db.session.add(activity_log)
        except Exception as log_error:
            print(f"Warning: Failed to log activity: {log_error}")
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update profile: {str(e)}"}), 500

@app.route('/api/resume/parse', methods=['POST'])
@jwt_required()
def parse_resume():
    """Parse resume file and extract profile information"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Check if file is uploaded
        if 'file' not in request.files and 'file_data' not in request.json:
            return jsonify({"error": "No file provided"}), 400
        
        # Handle file upload (multipart/form-data)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No file selected"}), 400
            
            file_content = file.read()
            filename = file.filename
        # Handle base64 encoded file (JSON)
        elif 'file_data' in request.json:
            file_data = request.json['file_data']
            filename = request.json.get('filename', 'resume.pdf')
            
            # Decode base64
            try:
                if ',' in file_data:
                    # Remove data URL prefix if present
                    file_data = file_data.split(',')[1]
                file_content = base64.b64decode(file_data)
            except Exception as e:
                return jsonify({"error": f"Invalid file data: {str(e)}"}), 400
        else:
            return jsonify({"error": "No file provided"}), 400
        
        # Parse resume
        parsed_data = parse_resume_file(file_content, filename)
        
        if parsed_data.get('error'):
            return jsonify({
                "success": False,
                "error": parsed_data['error']
            }), 400
        
        # Update user profile with extracted data
        updated_fields = []
        if parsed_data.get('bio'):
            user.bio = parsed_data['bio']
            updated_fields.append('bio')
        if parsed_data.get('company'):
            user.company = parsed_data['company']
            updated_fields.append('company')
        if parsed_data.get('role'):
            user.role = parsed_data['role']
            updated_fields.append('role')
        if parsed_data.get('linkedin_profile'):
            user.linkedin_profile = parsed_data['linkedin_profile']
            updated_fields.append('linkedin_profile')
        
        # Create activity log
        try:
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            talking_points = parsed_data.get('talking_points', [])
            activity_log = ActivityLog(
                user_id=user.id,
                activity_type='resume_uploaded',
                description=f'Resume uploaded and parsed: {filename}',
                ip_address=ip_address,
                user_agent=user_agent,
                extra_data=json.dumps({
                    'filename': filename,
                    'updated_fields': updated_fields,
                    'talking_points_count': len(talking_points)
                })
            )
            db.session.add(activity_log)
        except Exception as log_error:
            print(f"Warning: Failed to log activity: {log_error}")
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Resume parsed successfully",
            "profile_data": {
                "bio": parsed_data.get('bio'),
                "company": parsed_data.get('company'),
                "role": parsed_data.get('role'),
                "linkedin_profile": parsed_data.get('linkedin_profile')
            },
            "talking_points": parsed_data.get('talking_points', []),
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to parse resume: {str(e)}"}), 500

@app.route('/api/user/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Get user-specific statistics"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Count emails generated by this user
        emails_generated = Email.query.filter_by(user_id=user.id).count()
        
        # Count unique conversations (unique email recipients)
        from sqlalchemy import func
        unique_recipients = db.session.query(
            func.count(func.distinct(Email.recipient_email))
        ).filter_by(user_id=user.id).scalar() or 0
        
        return jsonify({
            "success": True,
            "stats": {
                "emails_generated": emails_generated,
                "conversations": unique_recipients
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get user stats: {str(e)}"}), 500

@app.route('/api/user/emails', methods=['GET'])
@jwt_required()
def get_user_emails():
    """Get emails for current user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get query parameters
        limit = request.args.get('limit', 50, type=int)
        status = request.args.get('status', None)
        
        # Build query
        query = Email.query.filter_by(user_id=user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Order by most recent first
        emails = query.order_by(Email.created_at.desc()).limit(limit).all()
        
        return jsonify({
            "success": True,
            "emails": [email.to_dict() for email in emails],
            "count": len(emails)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get emails: {str(e)}"}), 500

@app.route('/api/admin/emails', methods=['GET'])
@jwt_required()
@require_admin
def get_all_emails():
    """Get all emails for admin dashboard"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        status = request.args.get('status', None)
        email_type = request.args.get('email_type', None)
        user_id = request.args.get('user_id', None, type=int)
        
        # Build query
        query = Email.query
        
        if status:
            query = query.filter_by(status=status)
        if email_type:
            query = query.filter_by(email_type=email_type)
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        # Order by most recent first
        query = query.order_by(Email.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "success": True,
            "emails": [email.to_dict() for email in pagination.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "pages": pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get emails: {str(e)}"}), 500

@app.route('/api/admin/emails/stats', methods=['GET'])
@jwt_required()
@require_admin
def get_email_stats():
    """Get email statistics for admin dashboard"""
    try:
        from sqlalchemy import func
        
        # Total emails
        total_emails = Email.query.count()
        
        # Emails by status
        status_counts = db.session.query(
            Email.status,
            func.count(Email.id)
        ).group_by(Email.status).all()
        
        # Emails by type
        type_counts = db.session.query(
            Email.email_type,
            func.count(Email.id)
        ).group_by(Email.email_type).all()
        
        # Emails by day (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        daily_counts = db.session.query(
            func.date(Email.created_at).label('date'),
            func.count(Email.id).label('count')
        ).filter(
            Email.created_at >= thirty_days_ago
        ).group_by(func.date(Email.created_at)).order_by('date').all()
        
        # Top users by email count
        top_users = db.session.query(
            User.id,
            User.email,
            User.name,
            func.count(Email.id).label('email_count')
        ).join(Email).group_by(User.id, User.email, User.name).order_by(
            func.count(Email.id).desc()
        ).limit(10).all()
        
        # Top recipients
        top_recipients = db.session.query(
            Email.recipient_email,
            Email.recipient_name,
            func.count(Email.id).label('email_count')
        ).group_by(Email.recipient_email, Email.recipient_name).order_by(
            func.count(Email.id).desc()
        ).limit(10).all()
        
        return jsonify({
            "success": True,
            "stats": {
                "total_emails": total_emails,
                "by_status": {status: count for status, count in status_counts},
                "by_type": {email_type: count for email_type, count in type_counts if email_type},
                "daily_counts": [
                    {"date": str(date), "count": count} 
                    for date, count in daily_counts
                ],
                "top_users": [
                    {
                        "user_id": user_id,
                        "email": email,
                        "name": name,
                        "email_count": count
                    }
                    for user_id, email, name, count in top_users
                ],
                "top_recipients": [
                    {
                        "recipient_email": recipient_email,
                        "recipient_name": recipient_name,
                        "email_count": count
                    }
                    for recipient_email, recipient_name, count in top_recipients
                ]
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get email stats: {str(e)}"}), 500

@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
@require_admin
def get_all_users():
    """Get all users for admin dashboard"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        query = User.query.order_by(User.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "success": True,
            "users": [user.to_dict() for user in pagination.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "pages": pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get users: {str(e)}"}), 500

@app.route('/api/admin/users/<int:user_id>/make-admin', methods=['POST'])
@jwt_required()
@require_admin
def make_user_admin(user_id):
    """Make a user an admin"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user.is_admin = True
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"User {user.email} is now an admin",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to make user admin: {str(e)}"}), 500

@app.route('/api/subscription/create-checkout-session', methods=['POST'])
@jwt_required()
def create_subscription_checkout():
    """Create Stripe checkout session for subscription with trial"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get Stripe price ID from environment
        price_id = os.environ.get('STRIPE_PRICE_ID')
        if not price_id:
            return jsonify({"error": "Stripe price ID not configured"}), 500
        
        # Ensure user has a Stripe customer ID
        if not user.stripe_customer_id:
            if not is_stripe_configured():
                return jsonify({"error": "Stripe not configured"}), 500
            
            # Create Stripe customer
            customer_result = create_stripe_customer(user.email, user.name)
            if not customer_result.get('success'):
                return jsonify({"error": f"Failed to create Stripe customer: {customer_result.get('error')}"}), 500
            
            user.stripe_customer_id = customer_result['customer']['id']
            db.session.commit()
        
        # Get success and cancel URLs from request or use defaults
        data = request.get_json() or {}
        success_url = data.get('success_url', 'http://localhost:5173/?subscription=success')
        cancel_url = data.get('cancel_url', 'http://localhost:5173/?subscription=canceled')
        
        # Create checkout session
        checkout_result = create_checkout_session(
            customer_id=user.stripe_customer_id,
            price_id=price_id,
            success_url=success_url,
            cancel_url=cancel_url,
            trial_period_days=7
        )
        
        if not checkout_result.get('success'):
            return jsonify({"error": checkout_result.get('error', 'Failed to create checkout session')}), 500
        
        return jsonify({
            "success": True,
            "checkout_url": checkout_result['checkout_session']['url'],
            "session_id": checkout_result['checkout_session']['id']
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error creating checkout session: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({"error": f"Failed to create checkout session: {str(e)}"}), 500

@app.route('/api/subscription/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    try:
        payload = request.data
        sig_header = request.headers.get('Stripe-Signature')
        webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
        
        if not webhook_secret:
            # In development, skip signature verification
            print("Warning: STRIPE_WEBHOOK_SECRET not set, skipping webhook verification")
            event = json.loads(payload)
        else:
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, webhook_secret
                )
            except ValueError as e:
                print(f"Invalid payload: {e}")
                return jsonify({"error": "Invalid payload"}), 400
            except stripe.error.SignatureVerificationError as e:
                print(f"Invalid signature: {e}")
                return jsonify({"error": "Invalid signature"}), 400
        
        # Handle the event
        event_type = event['type']
        event_data = event['data']['object']
        
        if event_type == 'customer.subscription.created':
            subscription_id = event_data['id']
            customer_id = event_data['customer']
            
            # Find user by Stripe customer ID
            user = User.query.filter_by(stripe_customer_id=customer_id).first()
            if user:
                # Check if subscription already exists
                subscription = Subscription.query.filter_by(
                    stripe_subscription_id=subscription_id
                ).first()
                
                if not subscription:
                    subscription = Subscription(
                        user_id=user.id,
                        stripe_subscription_id=subscription_id,
                        status=event_data.get('status', 'active'),
                        plan_type='monthly'
                    )
                    db.session.add(subscription)
                
                # Update subscription details
                subscription.status = event_data.get('status', 'active')
                if event_data.get('trial_start'):
                    subscription.trial_start = datetime.fromtimestamp(event_data['trial_start'])
                if event_data.get('trial_end'):
                    subscription.trial_period_end = datetime.fromtimestamp(event_data['trial_end'])
                if event_data.get('current_period_end'):
                    subscription.current_period_end = datetime.fromtimestamp(event_data['current_period_end'])
                
                db.session.commit()
        
        elif event_type == 'customer.subscription.updated':
            subscription_id = event_data['id']
            subscription = Subscription.query.filter_by(
                stripe_subscription_id=subscription_id
            ).first()
            
            if subscription:
                subscription.status = event_data.get('status', subscription.status)
                if event_data.get('trial_end'):
                    subscription.trial_period_end = datetime.fromtimestamp(event_data['trial_end'])
                if event_data.get('current_period_end'):
                    subscription.current_period_end = datetime.fromtimestamp(event_data['current_period_end'])
                db.session.commit()
        
        elif event_type == 'customer.subscription.deleted':
            subscription_id = event_data['id']
            subscription = Subscription.query.filter_by(
                stripe_subscription_id=subscription_id
            ).first()
            
            if subscription:
                subscription.status = 'canceled'
                db.session.commit()
        
        return jsonify({"success": True}), 200
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({"error": f"Webhook processing failed: {str(e)}"}), 500

@app.route('/api/subscription/status', methods=['GET'])
@jwt_required()
def get_subscription_status_endpoint():
    """Get current user's subscription status"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Check database subscription first
        subscription = Subscription.query.filter_by(user_id=user.id).order_by(
            Subscription.created_at.desc()
        ).first()
        
        # If user has Stripe customer ID, also check Stripe
        stripe_status = None
        if user.stripe_customer_id and is_stripe_configured():
            stripe_status = get_subscription_status(user.stripe_customer_id)
        
        # Determine overall status
        status = 'none'
        is_trial = False
        trial_end = None
        current_period_end = None
        
        if subscription:
            if subscription.is_active():
                status = 'trial' if subscription.is_trial_active() else 'active'
                is_trial = subscription.is_trial_active()
                trial_end = subscription.trial_period_end.isoformat() if subscription.trial_period_end else None
                current_period_end = subscription.current_period_end.isoformat() if subscription.current_period_end else None
            else:
                status = subscription.status
        elif stripe_status and stripe_status.get('success') and stripe_status.get('has_subscription'):
            status = stripe_status.get('status', 'none')
            is_trial = stripe_status.get('is_trial', False)
            trial_end = stripe_status.get('trial_end')
            if stripe_status.get('subscription'):
                current_period_end_timestamp = stripe_status['subscription'].get('current_period_end')
                if current_period_end_timestamp:
                    current_period_end = datetime.fromtimestamp(current_period_end_timestamp).isoformat()
        
        return jsonify({
            "success": True,
            "status": status,
            "is_trial": is_trial,
            "trial_end": trial_end,
            "current_period_end": current_period_end,
            "subscription": subscription.to_dict() if subscription else None
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get subscription status: {str(e)}"}), 500

@app.route('/api/subscription/cancel', methods=['POST'])
@jwt_required()
def cancel_subscription_endpoint():
    """Cancel user's subscription"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        subscription = Subscription.query.filter_by(
            user_id=user.id,
            status='active'
        ).first()
        
        if not subscription or not subscription.stripe_subscription_id:
            return jsonify({"error": "No active subscription found"}), 404
        
        # Cancel via Stripe
        from services.stripe_service import cancel_subscription
        cancel_result = cancel_subscription(subscription.stripe_subscription_id)
        
        if not cancel_result.get('success'):
            return jsonify({"error": cancel_result.get('error', 'Failed to cancel subscription')}), 500
        
        subscription.status = 'canceled'
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Subscription canceled successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to cancel subscription: {str(e)}"}), 500

@app.route('/api/subscription/portal', methods=['POST'])
@jwt_required()
def create_portal_session_endpoint():
    """Create Stripe Customer Portal session for subscription management"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if not user.stripe_customer_id:
            return jsonify({"error": "No Stripe customer found"}), 404
        
        data = request.get_json() or {}
        return_url = data.get('return_url', 'http://localhost:5173/profile')
        
        portal_result = create_portal_session(user.stripe_customer_id, return_url)
        
        if not portal_result.get('success'):
            return jsonify({"error": portal_result.get('error', 'Failed to create portal session')}), 500
        
        return jsonify({
            "success": True,
            "url": portal_result['url']
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to create portal session: {str(e)}"}), 500

@app.route('/api/test-db', methods=['GET'])
def test_database():
    """Test endpoint to verify database is working"""
    try:
        # Try to query users
        user_count = User.query.count()
        subscription_count = Subscription.query.count()
        
        return jsonify({
            "success": True,
            "message": "Database connection successful",
            "user_count": user_count,
            "subscription_count": subscription_count,
            "database_path": app.config['SQLALCHEMY_DATABASE_URI']
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("Starting CoffeeChat AI Backend Server...")
    print("Gmail integration enabled")
    print("People search API ready")
    print("Chat API ready")
    print("=" * 50)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database initialized")
        print(f"Database path: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Check if credentials exist
    if not os.path.exists('credentials.json'):
        print("WARNING: Gmail credentials.json not found!")
        print("   Gmail draft creation will not work until credentials are set up.")
        print("   See docs/GMAIL_SETUP.md for instructions.")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
