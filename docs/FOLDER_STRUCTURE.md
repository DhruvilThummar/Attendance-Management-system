# Attendance System - Improved Folder Structure

## Updated Static Files Organization

### CSS Files Structure:
```
static/css/
├── main.css              # Core application styles (variables, utilities)
├── home.css              # Landing page styles
├── login.css             # Login page styles
├── register.css          # Registration page styles
├── dashboard.css         # Dashboard layout and components
├── attendance.css        # Attendance marking interface
├── reports.css           # Reports page styles
├── timetable.css         # Timetable grid and components
└── pages/               # Future page-specific styles
```

### JavaScript Files Structure:
```
static/js/
├── app.js               # Core application logic (auth, navigation, utilities)
├── auth.js              # Login and registration
├── dashboard.js         # Role-based dashboards
├── students.js          # Student management
├── faculty.js           # Faculty management
├── attendance.js        # Attendance marking
├── timetable.js         # Timetable management
├── reports.js           # Reports generation
├── profile.js           # User profile management
└── pages/              # Future page-specific modules
```

### Templates Organization:
```
templates/
├── base.html           # Base template
├── home.html           # Landing page
├── auth/
│   ├── login.html
│   └── register.html
├── admin/
│   ├── dashboard.html
│   ├── students.html
│   ├── faculty.html
│   └── departments.html
├── faculty/
│   ├── dashboard.html
│   └── mark_attendance.html
├── student/
│   ├── dashboard.html
│   └── attendance.html
├── hod/
│   └── dashboard.html
├── components/
│   ├── navbar.html
│   ├── footer.html
│   └── sidebar.html
├── timetable.html
├── reports.html
├── profile.html
└── settings.html
```

## File Mapping

Each HTML page now has dedicated CSS and JS files:

| Page | HTML Template | CSS File | JS File |
|------|--------------|----------|---------|
| Landing Page | home.html | home.css | - |
| Login | auth/login.html | login.css | auth.js |
| Register | auth/register.html | register.css | auth.js |
| Dashboard | admin/dashboard.html | dashboard.css | dashboard.js |
| Students | admin/students.html | dashboard.css | students.js |
| Faculty | admin/faculty.html | dashboard.css | faculty.js |
| Mark Attendance | faculty/mark_attendance.html | attendance.css | attendance.js |
| Student Attendance | student/attendance.html | dashboard.css | app.js |
| Timetable | timetable.html | timetable.css | timetable.js |
| Reports | reports.html | reports.css | reports.js |
| Profile | profile.html | dashboard.css | profile.js |

## How to Use

### In HTML Templates:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.min.css" rel="stylesheet">
    
    <!-- Core CSS -->
    <link href="{{ url_for('static', filename='css/main.css') }}" rel="stylesheet">
    
    <!-- Page-specific CSS -->
    <link href="{{ url_for('static', filename='css/login.css') }}" rel="stylesheet">
</head>
<body>
    <!-- Content -->
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Chart.js (if needed) -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    
    <!-- Core App JS (always load first) -->
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    
    <!-- Page-specific JS -->
    <script src="{{ url_for('static', filename='js/auth.js') }}"></script>
</body>
</html>
```

## Benefits of This Structure:

1. **Separation of Concerns**: Each page has its own dedicated styles and logic
2. **Better Performance**: Load only the CSS/JS needed for each page
3. **Easier Maintenance**: Find and update code faster
4. **Code Reusability**: Common utilities in app.js used across all pages
5. **Scalability**: Easy to add new pages with consistent structure
6. **Clear Dependencies**: main.css + app.js loaded on all pages, page-specific files loaded as needed

## Navigation Components:

The enhanced navbar (`components/navbar.html`) provides:
- Role-based menu items
- User profile dropdown
- Notifications
- Search functionality
- Responsive mobile design
- Active page highlighting

Include it in templates with:
```jinja2
{% include 'components/navbar.html' %}
```
