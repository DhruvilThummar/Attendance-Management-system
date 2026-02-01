# Database Documentation

## Overview

The Attendance Management System uses MySQL (MariaDB) as its database. The schema is defined in `attendance_system/schema.sql`.

**Database Name:** `databse`

## Tables

### 1. users
Primary table for all user accounts.

| Column | Type | Description |
|--------|------|-------------|
| user_id | INT (PK) | Auto-increment primary key |
| college_id | INT (FK) | Reference to college |
| name | VARCHAR(100) | Full name |
| email | VARCHAR(120) | Unique email address |
| password_hash | VARCHAR(255) | Hashed password |
| mobile | VARCHAR(15) | Mobile number |
| role_id | INT (FK) | Reference to role table |
| is_approved | TINYINT(1) | Approval status (0/1) |
| created_at | TIMESTAMP | Account creation timestamp |

### 2. role
Predefined user roles.

| role_id | role_name |
|---------|-----------|
| 1 | ADMIN |
| 2 | HOD |
| 3 | FACULTY |
| 4 | STUDENT |
| 5 | PARENT |

### 3. college
Educational institutions.

| Column | Type | Description |
|--------|------|-------------|
| college_id | INT (PK) | Auto-increment primary key |
| college_name | VARCHAR(150) | College name |
| created_at | TIMESTAMP | Creation timestamp |

### 4. department
Academic departments within colleges.

| Column | Type | Description |
|--------|------|-------------|
| dept_id | INT (PK) | Auto-increment primary key |
| college_id | INT (FK) | Reference to college |
| dept_name | VARCHAR(100) | Department name |
| hod_faculty_id | INT (FK) | Head of Department (faculty reference) |

### 5. division
Student divisions/sections.

| Column | Type | Description |
|--------|------|-------------|
| division_id | INT (PK) | Auto-increment primary key |
| dept_id | INT (FK) | Reference to department |
| division_name | VARCHAR(50) | Division name (A, B, C, etc.) |

### 6. semester
Academic semesters.

| Column | Type | Description |
|--------|------|-------------|
| semester_id | INT (PK) | Auto-increment primary key |
| semester_no | INT | Semester number (1-8) |
| academic_year | VARCHAR(9) | Academic year (e.g., 2025-2026) |

### 7. faculty
Faculty member details.

| Column | Type | Description |
|--------|------|-------------|
| faculty_id | INT (PK) | Auto-increment primary key |
| user_id | INT (FK) | Reference to users table |
| dept_id | INT (FK) | Reference to department |
| short_name | VARCHAR(50) | Faculty short name/initials |

### 8. student
Student details.

| Column | Type | Description |
|--------|------|-------------|
| student_id | INT (PK) | Auto-increment primary key |
| user_id | INT (FK) | Reference to users table |
| dept_id | INT (FK) | Reference to department |
| division_id | INT (FK) | Reference to division |
| enrollment_no | VARCHAR(50) | Unique enrollment number |
| roll_no | INT | Roll number |
| mentor_id | INT (FK) | Reference to faculty (mentor) |
| semester_id | INT (FK) | Reference to semester |

### 9. parent
Parent/guardian accounts.

| Column | Type | Description |
|--------|------|-------------|
| user_id | INT (FK) | Reference to users table |
| student_id | INT (FK) | Reference to student |

### 10. subject
Academic subjects.

| Column | Type | Description |
|--------|------|-------------|
| subject_id | INT (PK) | Auto-increment primary key |
| dept_id | INT (FK) | Reference to department |
| subject_name | VARCHAR(120) | Subject name |
| subject_code | VARCHAR(20) | Unique subject code |
| semester_id | INT (FK) | Reference to semester |

### 11. timetable
Class schedule/timetable.

| Column | Type | Description |
|--------|------|-------------|
| timetable_id | INT (PK) | Auto-increment primary key |
| subject_id | INT (FK) | Reference to subject |
| faculty_id | INT (FK) | Reference to faculty |
| division_id | INT (FK) | Reference to division |
| day_of_week | ENUM | MON, TUE, WED, THU, FRI, SAT |
| lecture_no | INT | Lecture number |
| room_no | VARCHAR(20) | Room number |
| building_block | VARCHAR(50) | Building/block name |
| start_time | TIME | Lecture start time |
| end_time | TIME | Lecture end time |

### 12. lecture
Individual lecture instances.

| Column | Type | Description |
|--------|------|-------------|
| lecture_id | INT (PK) | Auto-increment primary key |
| timetable_id | INT (FK) | Reference to timetable |
| lecture_date | DATE | Date of lecture |

**Unique Constraint:** (timetable_id, lecture_date)

### 13. attendance_status
Attendance status types.

| status_id | status_name |
|-----------|-------------|
| 1 | PRESENT |
| 2 | ABSENT |

### 14. attendance
Student attendance records.

| Column | Type | Description |
|--------|------|-------------|
| attendance_id | INT (PK) | Auto-increment primary key |
| student_id | INT (FK) | Reference to student |
| status_id | INT (FK) | Reference to attendance_status |
| marked_at | TIMESTAMP | When attendance was marked |
| lecture_id | INT (FK) | Reference to lecture |

**Unique Constraint:** (student_id, lecture_id)

### 15. proxy_lecture
Proxy/substitute lecture management.

| Column | Type | Description |
|--------|------|-------------|
| proxy_id | INT (PK) | Auto-increment primary key |
| lecture_id | INT (FK) | Reference to lecture |
| original_faculty_id | INT (FK) | Original faculty |
| substitute_faculty_id | INT (FK) | Substitute faculty |
| subject_id | INT (FK) | Reference to subject |
| lecture_date | DATE | Date of lecture |
| lecture_no | INT | Lecture number |
| room_no | VARCHAR(20) | Room number |
| building_block | VARCHAR(50) | Building/block name |
| reason | TEXT | Reason for proxy |
| status | ENUM | PENDING, ACCEPTED, REJECTED, COMPLETED |
| assigned_at | TIMESTAMP | When proxy was assigned |

### 16. academic_calendar
College academic calendar events.

| Column | Type | Description |
|--------|------|-------------|
| college_id | INT (FK) | Reference to college |
| event_date | DATE | Event date |
| event_type | ENUM | REGULAR, EXAM, HOLIDAY |
| description | VARCHAR(255) | Event description |
| dept_id | INT (FK) | Reference to department |

## Database Setup

### 1. Initialize Database

```bash
python scripts/seed_db.py
```

This will:
- Create the database `databse`
- Create all tables
- Insert default roles and attendance statuses

### 2. Create Admin User

```bash
python scripts/create_admin.py
```

Follow the prompts to create the first admin user and college.

## Environment Variables

Configure in `.env` file:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=databse
```

## Foreign Key Relationships

```
college
  └── department
       ├── division
       ├── subject
       └── faculty
            └── student
                 └── attendance

users
  ├── faculty
  ├── student
  └── parent

timetable → lecture → attendance
```

## Indexes

All foreign keys have indexes for optimal query performance. Additional indexes:
- `idx_attendance_student` on attendance(student_id)
- `idx_dept_college` on department(college_id)
- `idx_student_division` on student(division_id)
- `idx_subject_dept` on subject(dept_id)

## Cascade Rules

- **ON DELETE CASCADE**: Deleting a parent record deletes child records
  - college → department
  - department → division, subject, faculty
  - users → faculty, student, parent
  - timetable → lecture
  - lecture → attendance

- **ON DELETE SET NULL**: Deleting a parent sets child reference to NULL
  - faculty (HOD) → department.hod_faculty_id
