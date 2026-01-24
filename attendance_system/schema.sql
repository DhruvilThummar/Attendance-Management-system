-- Optimized Database Schema for Attendance System (MySQL)
-- Includes indexes and performance improvements

CREATE TABLE IF NOT EXISTS colleges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    subscription_status VARCHAR(50) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_subscription (subscription_status)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id INT,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    password TEXT NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (
        role IN (
            'SuperAdmin',
            'CollegeAdmin',
            'HOD',
            'Faculty',
            'Student'
        )
    ),
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges (id) ON DELETE CASCADE,
    UNIQUE (email),
    INDEX idx_college_role (college_id, role),
    INDEX idx_approval (is_approved, role),
    INDEX idx_college_approved (college_id, is_approved)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS divisions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id INT,
    name VARCHAR(50) NOT NULL,
    semester INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges (id) ON DELETE CASCADE,
    INDEX idx_college_semester (college_id, semester)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id INT,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(255) NOT NULL,
    branch VARCHAR(100),
    credits INT DEFAULT 4,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges (id) ON DELETE CASCADE,
    UNIQUE (college_id, code),
    INDEX idx_college_branch (college_id, branch),
    INDEX idx_code (code)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    enrollment_no VARCHAR(50) UNIQUE NOT NULL,
    roll_no VARCHAR(20),
    branch VARCHAR(100),
    phone_number VARCHAR(20),
    mentor_name VARCHAR(100),
    division_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (division_id) REFERENCES divisions (id) ON DELETE SET NULL,
    INDEX idx_enrollment (enrollment_no),
    INDEX idx_division (division_id),
    INDEX idx_branch (branch)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS faculties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    department VARCHAR(100),
    short_name VARCHAR(10),
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_department (department),
    INDEX idx_short_name (short_name)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS hods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    department_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_department (department_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS timetable (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT,
    faculty_id INT,
    division_id INT,
    day VARCHAR(20) NOT NULL,
    slot VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES faculties (id) ON DELETE CASCADE,
    FOREIGN KEY (division_id) REFERENCES divisions (id) ON DELETE CASCADE,
    INDEX idx_faculty (faculty_id),
    INDEX idx_subject (subject_id),
    INDEX idx_division_day (division_id, day)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS lectures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timetable_id INT,
    date DATE NOT NULL,
    proxy_faculty_id INT,
    status VARCHAR(20) DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (timetable_id) REFERENCES timetable (id) ON DELETE CASCADE,
    FOREIGN KEY (proxy_faculty_id) REFERENCES faculties (id) ON DELETE SET NULL,
    INDEX idx_date (date),
    INDEX idx_status (status),
    INDEX idx_proxy (proxy_faculty_id),
    INDEX idx_date_status (date, status)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS academic_calendar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_id INT,
    title VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    type VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges (id) ON DELETE CASCADE,
    INDEX idx_college_dates (
        college_id,
        start_date,
        end_date
    ),
    INDEX idx_type (type),
    INDEX idx_start_date (start_date)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lecture_id INT,
    student_id INT,
    status VARCHAR(10) NOT NULL CHECK (
        status IN (
            'P',
            'A',
            'Present',
            'Absent',
            'Late',
            'Excused'
        )
    ),
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (lecture_id, student_id),
    FOREIGN KEY (lecture_id) REFERENCES lectures (id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
    INDEX idx_lecture (lecture_id),
    INDEX idx_student (student_id),
    INDEX idx_status (status),
    INDEX idx_student_status (student_id, status)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS attendance_audit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attendance_id INT,
    old_status VARCHAR(10),
    new_status VARCHAR(10),
    edited_by INT,
    reason TEXT,
    edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (attendance_id) REFERENCES attendance (id) ON DELETE CASCADE,
    FOREIGN KEY (edited_by) REFERENCES users (id),
    INDEX idx_attendance (attendance_id),
    INDEX idx_edited_by (edited_by),
    INDEX idx_edited_at (edited_at)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT NOT NULL,
    type VARCHAR(20) DEFAULT 'Info',
    seen BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    INDEX idx_user_seen (user_id, seen),
    INDEX idx_created (created_at)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;