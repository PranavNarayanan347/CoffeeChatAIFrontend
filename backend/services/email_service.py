"""Email service for sending transactional emails"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from datetime import datetime

# Email configuration from environment variables
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
EMAIL_FROM = os.environ.get('EMAIL_FROM', SMTP_USERNAME)
EMAIL_FROM_NAME = os.environ.get('EMAIL_FROM_NAME', 'CoffeeChat AI')

# Frontend URL for reset links
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

def is_email_configured() -> bool:
    """Check if email service is configured"""
    return bool(SMTP_USERNAME and SMTP_PASSWORD)

def send_password_reset_email(email: str, reset_token: str, user_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Send password reset email
    
    Args:
        email: Recipient email address
        reset_token: Password reset token
        user_name: User's name (optional)
    
    Returns:
        Dictionary with success status and message
    """
    if not is_email_configured():
        return {
            'success': False,
            'error': 'Email service not configured. Set SMTP_USERNAME and SMTP_PASSWORD environment variables.'
        }
    
    try:
        # Create reset link
        reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}&email={email}"
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Reset Your Password - CoffeeChat AI'
        msg['From'] = f"{EMAIL_FROM_NAME} <{EMAIL_FROM}>"
        msg['To'] = email
        
        # Email content
        name = user_name or 'there'
        
        text_content = f"""
Hello {name},

You requested to reset your password for your CoffeeChat AI account.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

If you didn't request this password reset, please ignore this email.

Best regards,
CoffeeChat AI Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }}
        .button {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%); color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }}
        .warning {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>☕ CoffeeChat AI</h1>
        </div>
        <div class="content">
            <h2>Password Reset Request</h2>
            <p>Hello {name},</p>
            <p>You requested to reset your password for your CoffeeChat AI account.</p>
            <p style="text-align: center;">
                <a href="{reset_link}" class="button">Reset Password</a>
            </p>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #6b7280;">{reset_link}</p>
            <div class="warning">
                <strong>⚠️ Important:</strong> This link will expire in 1 hour. If you didn't request this password reset, please ignore this email.
            </div>
        </div>
        <div class="footer">
            <p>Best regards,<br>CoffeeChat AI Team</p>
            <p>This is an automated message. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Add parts to message
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        return {
            'success': True,
            'message': 'Password reset email sent successfully'
        }
        
    except smtplib.SMTPException as e:
        return {
            'success': False,
            'error': f'SMTP error: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to send email: {str(e)}'
        }

def send_welcome_email(email: str, user_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Send welcome email to new users
    
    Args:
        email: Recipient email address
        user_name: User's name (optional)
    
    Returns:
        Dictionary with success status and message
    """
    if not is_email_configured():
        return {
            'success': False,
            'error': 'Email service not configured'
        }
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Welcome to CoffeeChat AI!'
        msg['From'] = f"{EMAIL_FROM_NAME} <{EMAIL_FROM}>"
        msg['To'] = email
        
        name = user_name or 'there'
        
        text_content = f"""
Hello {name},

Welcome to CoffeeChat AI! We're excited to have you on board.

Get started by:
1. Upload your resume to extract talking points
2. Search for industry contacts
3. Generate personalized networking emails

If you have any questions, feel free to reach out.

Best regards,
CoffeeChat AI Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
        .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }}
        .button {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%); color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>☕ Welcome to CoffeeChat AI!</h1>
        </div>
        <div class="content">
            <p>Hello {name},</p>
            <p>Welcome to CoffeeChat AI! We're excited to have you on board.</p>
            <p><strong>Get started:</strong></p>
            <ul>
                <li>Upload your resume to extract talking points</li>
                <li>Search for industry contacts</li>
                <li>Generate personalized networking emails</li>
            </ul>
            <p style="text-align: center;">
                <a href="{FRONTEND_URL}" class="button">Get Started</a>
            </p>
        </div>
    </div>
</body>
</html>
        """
        
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        return {
            'success': True,
            'message': 'Welcome email sent successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to send welcome email: {str(e)}'
        }



