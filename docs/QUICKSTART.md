# Quick Start Guide
# Attendance Management System

## Overview

All routes and files are now properly connected! This guide will help you get started with the system.

## Project Structure

```
attendance_system/
├── app.py                 # Main application factory
├── config.py             # Configuration
├── db_manager.py         # Database connection pool
├── blueprints/           # Role-based dashboard routes
│   └── dashboards.py
├── routes/               # All route definitions
│   ├── __init__.py       # Blueprint registration
│   ├── core.py           # Public pages (/, /about, /contact)
│   ├── dashboard.py      # Dashboard pages
│   ├── academic.py       # Academic management pages
│   ├── pages.py          # Attendance pages
│   ├── login.py          # Login API
│   ├── registration.py   # Registration API
│   ├── reports.py        # Reports API
│   ├── departments.py    # Departments API
│   └── attendance_api.py # Attendance API
├── models/               # Database models
├── services/             # Business logic services
├── decorators/           # RBAC decorators
├── templates/            # HTML templates
└── static/              # CSS, JS, images
```

## Running the Application

### 1. Install Dependencies

```bash
pip install -r requirements.txt
# or if using pyproject.toml:
pip install -e .
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://username:password@localhost:3306/databse
```

### 3. Initialize Database

```bash
# Run schema to create tables
python seed_db.py
```

### 4. Create Admin User (Optional)

```bash
python scripts/create_admin.py
```

### 5. Verify Routes

```bash
python scripts/verify_routes.py
```

This will display all registered routes and check for any conflicts.

### 6. Run the Application

```bash
# Development mode
python -m flask --app attendance_system.app:create_app run --debug

# Or
python -c "from attendance_system.app import create_app; create_app().run(debug=True)"
```

The application will be available at: `http://localhost:5000`

## Route Structure

### Public Routes (No Authentication)
- `GET /` - Home page
- `GET /about` - About page
- `GET /contact` - Contact page
- `GET /api/login` - Login page
- `POST /api/login` - Login submission
- `GET /api/registration` - Registration page
- `POST /api/registration` - Registration submission

### Protected Routes (Authentication Required)

#### Dashboard Pages
- `GET /dashboard` - Main dashboard
- `GET /settings` - Settings
- `GET /profile` - User profile
- `GET /reports` - Reports page

#### Academic Pages
- `GET /faculty` - Faculty management
- `GET /students` - Students management
- `GET /timetable` - Timetable
- `GET /subjects` - Subjects
- `GET /departments` - Departments

#### Attendance Pages
- `GET /mark-attendance` - Mark attendance (Faculty only)
- `GET /student-attendance` - View attendance

#### Role-Based Dashboards (prefix: /dashboard)
- `GET /dashboard/student` - Student dashboard
- `GET /dashboard/faculty` - Faculty dashboard
- `GET /dashboard/hod` - HOD dashboard
- `GET /dashboard/parent` - Parent dashboard
- `GET /dashboard/college` - College admin dashboard
- `GET /dashboard/admin` - System admin dashboard

#### API Endpoints (prefix: /api)

**Authentication:**
- `POST /api/login` - User login
- `POST /api/logout` - User logout

**Departments:**
- `GET /api/departments/list` - List all departments
- `POST /api/departments/create` - Create department
- `GET /api/departments/<id>` - Get department
- `PUT /api/departments/<id>` - Update department
- `DELETE /api/departments/<id>` - Delete department

**Attendance:**
- `POST /api/attendance/mark` - Mark attendance
- `GET /api/attendance/student/<id>` - Get student attendance
- `GET /api/attendance/lecture/<id>` - Get lecture attendance
- `PUT /api/attendance/update/<id>` - Update attendance
- `POST /api/attendance/bulk-mark` - Bulk mark attendance
- `GET /api/attendance/statistics` - Get statistics

**Reports:**
- `POST /api/reports/generate` - Generate report
- `GET /api/reports/analytics` - Get analytics

## Testing the Routes

### Using cURL

```bash
# Test home page
curl http://localhost:5000/

# Test login page
curl http://localhost:5000/api/login

# Test login (POST)
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# Test departments list (requires auth)
curl http://localhost:5000/api/departments/list \
  -H "Cookie: session=your-session-cookie"
```

### Using Python

```python
from attendance_system.app import create_app

app = create_app()

# Test client
with app.test_client() as client:
    # Test home page
    response = client.get('/')
    print(response.status_code)  # Should be 200
    
    # Test login
    response = client.post('/api/login', json={
        'username': 'admin',
        'password': 'password'
    })
    print(response.json)
```

## User Roles

The system supports 6 user roles:

1. **Student** - View personal attendance, track progress
2. **Faculty** - Mark attendance, manage classes, generate reports
3. **HOD** - Department management, timetables, faculty oversight
4. **Parent** - View children's attendance
5. **College** - Institution-wide management and analytics
6. **Admin** - System administration, user management

## Key Features

✅ **Properly Connected Routes** - All blueprints registered correctly
✅ **Role-Based Access Control** - RBAC decorators enforce permissions
✅ **RESTful API** - JSON-based API for programmatic access
✅ **Comprehensive Templates** - All required HTML templates created
✅ **Error Handling** - 404 and 500 error pages
✅ **Session Management** - Secure session handling
✅ **Database Connection Pool** - Efficient database connections

## API Request/Response Examples

### Mark Attendance

**Request:**
```http
POST /api/attendance/mark
Content-Type: application/json

{
  "lecture_id": 123,
  "student_ids": [1, 2, 3, 4],
  "date": "2026-02-01",
  "remarks": "Regular class"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Attendance marked for 4 students"
}
```

### Generate Report

**Request:**
```http
POST /api/reports/generate
Content-Type: application/json

{
  "report_type": "student",
  "format": "json",
  "start_date": "2026-01-01",
  "end_date": "2026-01-31",
  "filters": {
    "student_id": 101
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "student_id": 101,
    "total_classes": 20,
    "attended": 18,
    "percentage": 90.0,
    "records": [...]
  }
}
```

## Troubleshooting

### Routes Not Found (404)
1. Run `python scripts/verify_routes.py` to check route registration
2. Check blueprint imports in `routes/__init__.py`
3. Verify blueprint registration in `app.py`

### Database Connection Errors
1. Check `DATABASE_URL` in `.env` file
2. Ensure MySQL server is running
3. Verify database name matches schema (default: `databse`)

### Authentication Issues
1. Check `SECRET_KEY` is set in `.env`
2. Verify session configuration
3. Check decorator imports in route files

## Next Steps

1. **Customize Templates** - Update HTML templates with your design
2. **Add Services** - Implement business logic in service classes
3. **Configure Database** - Set up production database
4. **Add Tests** - Write unit and integration tests
5. **Deploy** - Deploy to production server

## Documentation

- [Complete Route Documentation](ROUTES.md)
- [Database Schema](DATABASE.md)
- [API Documentation](api.md)

## Support

For issues or questions:
- Check documentation in `docs/` folder
- Run verification scripts in `scripts/` folder
- Review error logs in application output

---

**Status**: ✅ All routes properly connected and configured!
**Last Updated**: February 2026
