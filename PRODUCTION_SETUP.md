# Production Setup Guide

Complete guide for deploying CoffeeChat AI to production.

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- Redis server (for distributed rate limiting)
- SMTP email service account
- Domain name with SSL certificate

## 🔧 Step 1: Configure SMTP Email Service

### Option A: Gmail (Development/Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "CoffeeChat AI" as the name
   - Copy the generated 16-character password

3. **Set Environment Variables**:
```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=your-email@gmail.com
export SMTP_PASSWORD=your-16-char-app-password
export EMAIL_FROM=your-email@gmail.com
export EMAIL_FROM_NAME=CoffeeChat AI
export FRONTEND_URL=https://yourdomain.com
```

### Option B: SendGrid (Recommended for Production)

1. **Sign up** at https://sendgrid.com
2. **Create API Key**:
   - Go to Settings > API Keys
   - Create new API key with "Mail Send" permissions
   - Copy the API key

3. **Set Environment Variables**:
```bash
export SMTP_SERVER=smtp.sendgrid.net
export SMTP_PORT=587
export SMTP_USERNAME=apikey
export SMTP_PASSWORD=your-sendgrid-api-key
export EMAIL_FROM=noreply@yourdomain.com
export EMAIL_FROM_NAME=CoffeeChat AI
export FRONTEND_URL=https://yourdomain.com
```

### Option C: AWS SES

1. **Verify Domain** in AWS SES
2. **Create SMTP Credentials**:
   - Go to SES > SMTP Settings
   - Create SMTP credentials
   - Copy username and password

3. **Set Environment Variables**:
```bash
export SMTP_SERVER=email-smtp.us-east-1.amazonaws.com
export SMTP_PORT=587
export SMTP_USERNAME=your-aws-smtp-username
export SMTP_PASSWORD=your-aws-smtp-password
export EMAIL_FROM=noreply@yourdomain.com
export EMAIL_FROM_NAME=CoffeeChat AI
export FRONTEND_URL=https://yourdomain.com
```

### Test Email Configuration

```bash
cd backend
python scripts/test_email.py
```

## 🔧 Step 2: Set Up Redis for Rate Limiting

### Local Redis Installation

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Docker:**
```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

### Cloud Redis Options

- **Redis Cloud**: https://redis.com/cloud/
- **AWS ElastiCache**: https://aws.amazon.com/elasticache/
- **Azure Cache for Redis**: https://azure.microsoft.com/services/cache/
- **Heroku Redis**: https://elements.heroku.com/addons/heroku-redis

### Configure Redis Connection

**Local Redis:**
```bash
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=0
export RATE_LIMIT_STORAGE=redis
```

**Cloud Redis (Redis URL):**
```bash
export REDIS_URL=redis://:password@host:port/db
export RATE_LIMIT_STORAGE=redis
```

**Example (Redis Cloud):**
```bash
export REDIS_URL=redis://:mypassword@redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com:12345
export RATE_LIMIT_STORAGE=redis
```

### Test Redis Connection

```bash
cd backend
python scripts/test_redis.py
```

## 🔧 Step 3: Configure PostgreSQL Database

### Create Database

```sql
CREATE DATABASE coffeechat_db;
CREATE USER coffeechat_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE coffeechat_db TO coffeechat_user;
```

### Set Environment Variable

```bash
export DATABASE_URL=postgresql://coffeechat_user:secure_password_here@localhost:5432/coffeechat_db
```

### Run Migrations

```bash
cd backend
python migrations/migrate_password_reset_and_activity.py
```

## 🔧 Step 4: Configure Application Secrets

### Generate JWT Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Set All Environment Variables

Create a `.env` file or set environment variables:

```bash
# Database
export DATABASE_URL=postgresql://user:password@host:port/database

# JWT
export JWT_SECRET_KEY=your-generated-secret-key-here

# Email (see Step 1)
export SMTP_SERVER=smtp.sendgrid.net
export SMTP_PORT=587
export SMTP_USERNAME=apikey
export SMTP_PASSWORD=your-api-key
export EMAIL_FROM=noreply@yourdomain.com
export EMAIL_FROM_NAME=CoffeeChat AI
export FRONTEND_URL=https://yourdomain.com

# Redis (see Step 2)
export REDIS_URL=redis://:password@host:port/db
export RATE_LIMIT_STORAGE=redis

# API Keys
export OPENAI_API_KEY=sk-...
export STRIPE_SECRET_KEY=sk_live_...

# Production Mode
export FLASK_ENV=production
export FLASK_DEBUG=False
```

## 🔧 Step 5: Remove Token from API Responses

The code already conditionally removes tokens in production. Verify:

1. **Email is configured** → Token removed from response
2. **Email not configured** → Token included (dev mode only)

To force production mode:
```bash
export PRODUCTION_MODE=true
```

## 🔧 Step 6: Set Up Monitoring and Alerts

### Application Monitoring

**Option A: Sentry (Error Tracking)**
```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    environment="production"
)
```

**Option B: Datadog**
```bash
pip install datadog
```

**Option C: New Relic**
```bash
pip install newrelic
```

### Health Check Endpoint

Already available at `/api/health`. Set up monitoring to check:
- Response time < 200ms
- Status code = 200
- Database connectivity
- Redis connectivity

### Key Metrics to Monitor

1. **API Response Times**
   - Average response time
   - P95/P99 response times
   - Slow endpoints

2. **Error Rates**
   - 4xx errors (client errors)
   - 5xx errors (server errors)
   - Rate limit violations (429)

3. **Email Delivery**
   - Success rate
   - Bounce rate
   - Delivery time

4. **Database Performance**
   - Query execution time
   - Connection pool usage
   - Slow queries

5. **Rate Limiting**
   - Requests blocked per hour
   - Top IPs hitting limits
   - Suspicious patterns

### Alert Thresholds

Set up alerts for:
- Error rate > 1%
- Response time P95 > 1s
- Database connection failures
- Redis connection failures
- Email delivery failures > 5%
- Rate limit violations spike

## 🔧 Step 7: Security Checklist

- [ ] HTTPS enabled (SSL certificate)
- [ ] CORS configured for production domain only
- [ ] JWT secret key is strong and secure
- [ ] Database credentials are secure
- [ ] Redis password is set
- [ ] SMTP credentials are secure
- [ ] Environment variables not in code
- [ ] Rate limiting enabled
- [ ] Activity logging enabled
- [ ] Regular security updates
- [ ] Firewall configured
- [ ] Backup strategy in place

## 🔧 Step 8: Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Using Systemd Service

Create `/etc/systemd/system/coffeechat.service`:

```ini
[Unit]
Description=CoffeeChat AI Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/coffeechat/backend
Environment="PATH=/opt/coffeechat/venv/bin"
ExecStart=/opt/coffeechat/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🧪 Step 9: Testing

### Test Email Delivery

```bash
cd backend
python scripts/test_email.py
```

### Test Redis Connection

```bash
cd backend
python scripts/test_redis.py
```

### Test API Endpoints

```bash
# Health check
curl https://yourdomain.com/api/health

# Test rate limiting
for i in {1..5}; do
  curl -X POST https://yourdomain.com/api/auth/forgot-password \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com"}'
done
```

## 📊 Monitoring Dashboard

Create a simple monitoring dashboard:

```python
@app.route('/api/admin/stats', methods=['GET'])
@jwt_required()
def admin_stats():
    """Admin endpoint for monitoring stats"""
    # Check if user is admin (implement admin check)
    
    stats = {
        'database': {
            'connected': db.session.execute(text('SELECT 1')).scalar() == 1
        },
        'redis': {
            'connected': _redis_client.ping() if _redis_client else False
        },
        'email': {
            'configured': is_email_configured()
        }
    }
    
    return jsonify(stats)
```

## 🚨 Troubleshooting

### Email Not Sending

1. Check SMTP credentials
2. Verify firewall allows SMTP connections
3. Check spam folder
4. Review email service logs
5. Test with `test_email.py` script

### Redis Connection Failed

1. Verify Redis is running: `redis-cli ping`
2. Check host/port configuration
3. Verify firewall allows connections
4. Check Redis password
5. Test with `test_redis.py` script

### Rate Limiting Not Working

1. Verify Redis is connected
2. Check `RATE_LIMIT_STORAGE` environment variable
3. Review rate limit logs
4. Test with multiple requests

## 📝 Production Checklist

- [ ] SMTP configured and tested
- [ ] Redis configured and tested
- [ ] PostgreSQL database set up
- [ ] Environment variables configured
- [ ] SSL certificate installed
- [ ] Monitoring set up
- [ ] Alerts configured
- [ ] Backups scheduled
- [ ] Security checklist completed
- [ ] Load testing completed
- [ ] Documentation updated

## 🔗 Additional Resources

- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [PostgreSQL Best Practices](https://www.postgresql.org/docs/current/admin.html)
- [Redis Best Practices](https://redis.io/docs/manual/patterns/)
- [Email Deliverability Guide](https://sendgrid.com/resource/email-deliverability-guide/)



