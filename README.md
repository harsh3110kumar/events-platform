# Events Platform

A full-stack events management platform with authentication, role-based access control (RBAC), and event enrollment functionality.

## Features

- **Authentication & Authorization**
  - JWT-based authentication
  - Email OTP verification
  - Role-based access control (Seeker & Facilitator)
  
- **Event Management**
  - Create, read, update, delete events (Facilitators)
  - Search and filter events (Seekers)
  - Event capacity management
  
- **Enrollment System**
  - Enroll in events (Seekers)
  - Track past and upcoming enrollments
  - Cancel enrollments
  
- **Email Notifications**
  - Follow-up email 1 hour after enrollment
  - Reminder email 1 hour before event starts
  
- **Simple Frontend UI**
  - React-based frontend
  - Responsive design
  - Role-specific dashboards

## Tech Stack

### Backend
- Django 4.2+
- Django REST Framework
- JWT Authentication (djangorestframework-simplejwt)
- PostgreSQL (SQLite for development)
- Celery & Redis (for scheduled emails)

### Frontend
- React 18
- Vite
- React Router
- Axios

## Quick Start - How to Run the Project

### Prerequisites
- Python 3.11+
- Node.js 16+
- PostgreSQL (optional, SQLite is used by default for development)
- Redis (optional, only needed for Celery scheduled emails)

### Step-by-Step Setup

#### 1. Backend Setup

**Open PowerShell and run:**

```powershell
# Navigate to backend directory
cd backend

# Activate virtual environment (already created)
.\venv\Scripts\Activate.ps1

# Run migrations (first time only, if not already done)
python manage.py migrate

# Start Django development server
python manage.py runserver
```

The backend will start at: **http://localhost:8000**

**Keep this PowerShell window open** - you'll need it to see OTP codes!

#### 2. Frontend Setup

**Open a NEW PowerShell window and run:**

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start frontend development server
npm run dev
```

The frontend will start at: **http://localhost:3000**

#### 3. Access the Application

1. Open your browser and go to: **http://localhost:3000**
2. Sign up for a new account (choose Seeker or Facilitator role)
3. **Check the Backend PowerShell window** for your OTP code (see below)
4. Verify your email with the OTP
5. Login and start using the platform!

### 📧 Important: Getting Your OTP Code

**OTP codes appear in the Backend PowerShell window**, not in your email!

After signing up:
1. Look at the **Backend PowerShell window** (the one running `python manage.py runserver`)
2. You'll see email output like this:
   ```
   Content-Type: text/plain; charset="utf-8"
   Subject: Verify your email - Events Platform
   From: noreply@eventsplatform.com
   To: your-email@example.com
   
   Your OTP is: 123456. It will expire in 5 minutes.
   ```
3. Copy the 6-digit number (e.g., `123456`)
4. Enter it on the verify email page

**Note:** This is because we're using `console.EmailBackend` for development, which prints emails to the terminal instead of sending real emails.

### Complete Setup Instructions (First Time)

If setting up for the first time:

#### Backend

```powershell
cd backend

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file (already created, but verify it exists)
# It should contain:
# SECRET_KEY=django-insecure-change-me-in-production-12345
# DEBUG=True
# ALLOWED_HOSTS=localhost,127.0.0.1
# USE_SQLITE=True
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

#### Frontend

```powershell
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Running Celery (Optional - for scheduled emails)

Only needed if you want automated email reminders. Requires Redis:

1. Start Redis (if not running):
```powershell
redis-server
```

2. Start Celery worker (new terminal):
```powershell
cd backend
.\venv\Scripts\Activate.ps1
celery -A events_platform worker -l info
```

3. Start Celery beat (another terminal):
```powershell
cd backend
.\venv\Scripts\Activate.ps1
celery -A events_platform beat -l info
```

## Docker Setup (Optional)

1. Build and run with docker-compose:
```bash
cd backend
docker-compose up --build
```

This will start:
- PostgreSQL database
- Redis
- Django backend
- Celery worker
- Celery beat

## API Endpoints

### Authentication
- `POST /api/auth/signup/` - Create new user account
- `POST /api/auth/verify-email/` - Verify email with OTP
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get current user profile

### Events
- `GET /api/events/` - List events (filtered by role)
- `POST /api/events/` - Create event (Facilitator only)
- `GET /api/events/{id}/` - Get event details
- `PUT /api/events/{id}/` - Update event (Facilitator, owner only)
- `DELETE /api/events/{id}/` - Delete event (Facilitator, owner only)

### Enrollments
- `GET /api/enrollments/` - List user's enrollments
- `POST /api/enrollments/` - Enroll in event (Seeker only)
- `GET /api/enrollments/upcoming/` - List upcoming enrollments
- `GET /api/enrollments/past/` - List past enrollments
- `PATCH /api/enrollments/{id}/` - Update enrollment status

## API Documentation

### Request Format
All requests should include:
- `Content-Type: application/json`
- `Authorization: Bearer <access_token>` (for authenticated endpoints)

### Response Format
Success responses follow standard DRF format:
```json
{
  "count": 10,
  "next": "http://api/events/?page=2",
  "previous": null,
  "results": [...]
}
```

Error responses:
```json
{
  "detail": "Error message",
  "code": "error_code"
}
```

## Running the Application - Quick Reference

### Start Both Servers

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```
Backend: http://localhost:8000

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```
Frontend: http://localhost:3000

### First Time Setup Checklist

- [ ] Backend virtual environment created (`python -m venv venv`)
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file exists in `backend/` directory
- [ ] Database migrations run (`python manage.py migrate`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Both servers running successfully

### Common Commands

**Backend:**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver

# Run tests
python manage.py test
```

**Frontend:**
```powershell
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Testing

### Backend Tests
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py test
```

### Frontend Tests
```powershell
cd frontend
npm test
```

## Design Decisions & Tradeoffs

### User Model
- Used Django's default User model with a UserProfile extension
- Email is used as the primary identifier (username field is set to email but not used)
- Roles are stored in UserProfile to maintain separation of concerns

### Authentication
- JWT tokens for stateless authentication
- Email OTP verification with TTL (5 minutes) and attempt limits (5 attempts)
- Access token lifetime: 1 hour
- Refresh token lifetime: 7 days

### Permissions
- Custom permission classes for role-based access control
- Email verification required for all authenticated endpoints
- Ownership checks for update/delete operations

### Email System
- **Development Mode**: Console backend prints emails (including OTP codes) to the backend PowerShell window
- **OTP Codes**: After signing up, check the backend terminal window for your 6-digit OTP code (not sent via email in development)
- **Production**: Configure SMTP settings in `.env` for real email delivery
- Celery tasks for asynchronous email sending (optional, requires Redis)
- Follow-up emails scheduled 1 hour after enrollment
- Reminder emails checked every 5 minutes via Celery Beat
- Console backend used in development (configurable via .env)

### Database
- PostgreSQL for production (SQLite fallback for development)
- Indexes on frequently queried fields (starts_at, language, location)
- Unique constraint on event-seeker enrollment pairs

### Frontend
- Simple React SPA with minimal dependencies
- Axios interceptors for automatic token refresh
- Local storage for token persistence

## Production Considerations

1. **Security**
   - Change SECRET_KEY
   - Set DEBUG=False
   - Configure proper ALLOWED_HOSTS
   - Use HTTPS
   - Configure proper CORS origins

2. **Email**
   - Change `EMAIL_BACKEND` in `.env` from `django.core.mail.backends.console.EmailBackend` to SMTP backend
   - Configure SMTP settings in .env:
     ```env
     EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
     EMAIL_HOST=smtp.gmail.com
     EMAIL_PORT=587
     EMAIL_USE_TLS=True
     EMAIL_HOST_USER=your-email@gmail.com
     EMAIL_HOST_PASSWORD=your-app-password
     DEFAULT_FROM_EMAIL=noreply@eventsplatform.com
     ```
   - Use email service (SendGrid, AWS SES, etc.)

3. **Database**
   - Use PostgreSQL in production
   - Set up database backups
   - Configure connection pooling

4. **Celery**
   - Run workers as separate services
   - Use supervisor/systemd for process management
   - Configure proper Redis persistence

5. **Static Files**
   - Configure static file serving (nginx, AWS S3, etc.)
   - Run `python manage.py collectstatic`

## License

MIT

