# Routing Documentation
# Attendance Management System

## Complete Route Map

This document provides a comprehensive overview of all routes in the Attendance Management System.

---

## Table of Contents
1. [Core Routes](#core-routes)
2. [Dashboard Routes](#dashboard-routes)
3. [Academic Routes](#academic-routes)
4. [Attendance Routes](#attendance-routes)
5. [API Routes](#api-routes)
6. [Role-Based Dashboard Routes](#role-based-dashboard-routes)

---

## Core Routes
**Blueprint**: `core` (no prefix)
**File**: `attendance_system/routes/core.py`

| Route | Method | Description | Template |
|-------|--------|-------------|----------|
| `/` | GET | Home page | home.html |
| `/about` | GET | About page | about.html |
| `/contact` | GET | Contact page | contact.html |

---

## Dashboard Routes
**Blueprint**: `dashboard` (no prefix)
**File**: `attendance_system/routes/dashboard.py`

| Route | Method | Description | Template | Auth Required |
|-------|--------|-------------|----------|---------------|
| `/dashboard` | GET | Main dashboard page | dashboard.html | Yes |
| `/settings` | GET | Settings page | settings.html | Yes |
| `/profile` | GET | User profile page | profile.html | Yes |
| `/reports` | GET | Reports page | reports.html | Yes |

---

## Academic Routes
**Blueprint**: `academic` (no prefix)
**File**: `attendance_system/routes/academic.py`

| Route | Method | Description | Template | Auth Required |
|-------|--------|-------------|----------|---------------|
| `/faculty` | GET | Faculty management page | faculty.html | Yes |
| `/students` | GET | Students management page | students.html | Yes |
| `/timetable` | GET | Timetable management page | timetable.html | Yes |
| `/subjects` | GET | Subjects management page | subjects.html | Yes |
| `/departments` | GET | Departments page | departments.html | Yes |

---

## Attendance Routes
**Blueprint**: `attendance` (no prefix)
**File**: `attendance_system/routes/pages.py`

| Route | Method | Description | Template | Auth Required |
|-------|--------|-------------|----------|---------------|
| `/mark-attendance` | GET | Mark attendance page | attendance.html | Yes (Faculty) |
| `/student-attendance` | GET | Student attendance view | student-attendance.html | Yes |

---

## API Routes
**Blueprint**: `api` (prefix: `/api`)

### Authentication Routes
**File**: `attendance_system/routes/login.py`

| Route | Method | Description | Returns |
|-------|--------|-------------|---------|
| `/api/login` | GET | Login page | login.html |
| `/api/login` | POST | Process login | JSON |
| `/api/logout` | POST | Logout user | JSON |

### Registration Routes
**File**: `attendance_system/routes/registration.py`

| Route | Method | Description | Returns |
|-------|--------|-------------|---------|
| `/api/registration` | GET | Registration page | register.html |
| `/api/registration` | POST | Create new user | JSON |

### Reports Routes
**File**: `attendance_system/routes/reports.py`

| Route | Method | Description | Returns | Auth Required |
|-------|--------|-------------|---------|---------------|
| `/api/reports` | GET | Reports page | reports.html | Yes |
| `/api/reports/generate` | POST | Generate report | JSON/File | Yes |
| `/api/reports/analytics` | GET | Get analytics data | JSON | Yes |

**POST /api/reports/generate Parameters:**
```json
{
  "report_type": "student|class|faculty|department",
  "format": "pdf|csv|json",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "filters": {}
}
```

**GET /api/reports/analytics Query Parameters:**
- `type`: overview|trends|comparison
- `period`: week|month|semester|year

### Departments Routes
**File**: `attendance_system/routes/departments.py`

| Route | Method | Description | Returns | Auth Required |
|-------|--------|-------------|---------|---------------|
| `/api/departments` | GET | Departments page | departments.html | Yes |
| `/api/departments/list` | GET | Get all departments | JSON | Yes |
| `/api/departments/create` | POST | Create department | JSON | Yes (Admin) |
| `/api/departments/<id>` | GET | Get department details | JSON | Yes |
| `/api/departments/<id>` | PUT | Update department | JSON | Yes (Admin) |
| `/api/departments/<id>` | DELETE | Delete department | JSON | Yes (Admin) |

### Attendance API Routes
**File**: `attendance_system/routes/attendance_api.py`

| Route | Method | Description | Returns | Auth Required |
|-------|--------|-------------|---------|---------------|
| `/api/attendance/mark` | POST | Mark attendance | JSON | Yes (Faculty) |
| `/api/attendance/student/<id>` | GET | Get student attendance | JSON | Yes |
| `/api/attendance/lecture/<id>` | GET | Get lecture attendance | JSON | Yes |
| `/api/attendance/update/<id>` | PUT | Update attendance record | JSON | Yes (Faculty) |
| `/api/attendance/bulk-mark` | POST | Bulk mark attendance | JSON | Yes (Faculty) |
| `/api/attendance/statistics` | GET | Get statistics | JSON | Yes |

**POST /api/attendance/mark Parameters:**
```json
{
  "lecture_id": 123,
  "student_ids": [1, 2, 3],
  "date": "YYYY-MM-DD",
  "remarks": "Optional"
}
```

**POST /api/attendance/bulk-mark Parameters:**
```json
{
  "lecture_id": 123,
  "date": "YYYY-MM-DD",
  "attendance_data": [
    {
      "student_id": 1,
      "status": "present|absent|late|excused",
      "remarks": "Optional"
    }
  ]
}
```

---

## Role-Based Dashboard Routes
**Blueprint**: `dashboards` (prefix: `/dashboard`)
**File**: `attendance_system/blueprints/dashboards.py`

### Student Routes

| Route | Method | Description | Auth Required |
|-------|--------|-------------|---------------|
| `/dashboard/student` | GET | Student dashboard | Student role |
| `/dashboard/student/attendance` | GET | Student attendance details | Student role |

### Faculty Routes

| Route | Method | Description | Auth Required |
|-------|--------|-------------|---------------|
| `/dashboard/faculty` | GET | Faculty dashboard | Faculty role |
| `/dashboard/faculty/mark-attendance` | GET, POST | Mark attendance | Faculty role |
| `/dashboard/faculty/classes` | GET | View classes | Faculty role |
| `/dashboard/faculty/reports` | GET | Generate reports | Faculty role |

### HOD Routes

| Route | Method | Description | Auth Required |
|-------|--------|-------------|---------------|
| `/dashboard/hod` | GET | HOD dashboard | HOD role |
| `/dashboard/hod/timetable` | GET, POST | Manage timetable | HOD role |
| `/dashboard/hod/reports` | GET | Department reports | HOD role |
| `/dashboard/hod/faculty` | GET | Manage faculty | HOD role |

### Parent Routes

| Route | Method | Description | Auth Required |
|-------|--------|-------------|---------------|
| `/dashboard/parent` | GET | Parent dashboard | Parent role |
| `/dashboard/parent/children` | GET | View children | Parent role |
| `/dashboard/parent/attendance/<id>` | GET | Child attendance | Parent role |

### College Admin Routes

| Route | Method | Description | Auth Required |
|-------|--------|-------------|---------------|
| `/dashboard/college` | GET | College admin dashboard | College role |
| `/dashboard/college/overview` | GET | System overview | College role |
| `/dashboard/college/departments` | GET | Manage departments | College role |
| `/dashboard/college/analytics` | GET | College analytics | College role |

### System Admin Routes

| Route | Method | Description | Auth Required |
|-------|--------|-------------|---------------|
| `/dashboard/admin` | GET | Admin dashboard | Admin role |
| `/dashboard/admin/users` | GET, POST | Manage users | Admin role |
| `/dashboard/admin/settings` | GET, POST | System settings | Admin role |
| `/dashboard/admin/logs` | GET | View system logs | Admin role |

---

## Error Handlers

| Status Code | Template | Description |
|-------------|----------|-------------|
| 404 | 404.html | Page not found |
| 500 | 500.html | Internal server error |

---

## Blueprint Registration Order

The blueprints are registered in the following order in `app.py`:

1. **dashboards** - Role-based dashboards (prefix: `/dashboard`)
2. **core** - Public pages (no prefix)
3. **dashboard** - User dashboard pages (no prefix)
4. **academic** - Academic management (no prefix)
5. **attendance** - Attendance pages (no prefix)
6. **api** - API endpoints (prefix: `/api`)

---

## Authentication & Authorization

### Decorators Available:
- `@login_required` - Requires user to be logged in
- `@faculty_only` - Requires Faculty role
- `@student_only` - Requires Student role
- `@hod_only` - Requires HOD role
- `@parent_only` - Requires Parent role
- `@college_only` - Requires College Admin role
- `@admin_only` - Requires System Admin role

**Location**: `attendance_system/decorators/rbac.py`

---

## Session Variables

When a user logs in, the following session variables are set:
- `user_id` - User's ID
- `username` - User's username
- `role` - User's role (student, faculty, hod, parent, college, admin)

---

## API Response Format

### Success Response:
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {}
}
```

### Error Response:
```json
{
  "success": false,
  "message": "Error description"
}
```

---

## Common HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET request |
| 201 | Created | Successfully created resource |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication required/failed |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 500 | Internal Server Error | Server error |

---

## How to Add New Routes

### Adding a Page Route:

1. Choose appropriate blueprint (core, dashboard, academic, attendance)
2. Add route to corresponding file in `attendance_system/routes/`
3. Create template in `attendance_system/templates/`

Example:
```python
@academic.route("/courses")
def courses():
    """Courses management page."""
    return render_template("courses.html")
```

### Adding an API Route:

1. Add route to `api` blueprint
2. Import in `attendance_system/routes/__init__.py`
3. Apply appropriate decorators for auth

Example:
```python
@api.route("/courses/list", methods=["GET"])
@login_required
def list_courses():
    """Get all courses."""
    # Implementation
    return jsonify({"success": True, "courses": courses})
```

---

## Testing Routes

To test if routes are properly connected:

```python
from attendance_system.app import create_app

app = create_app()

# List all routes
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.rule} [{','.join(rule.methods)}]")
```

---

## Notes

- All API routes return JSON responses
- All page routes return HTML templates
- Authentication is handled via Flask sessions
- RBAC decorators enforce role-based access control
- Database connections are managed via connection pool
- Error handlers provide user-friendly error pages

---

**Last Updated**: February 2026
**Version**: 1.0
