-- =========================================
-- DATABASE
-- =========================================
CREATE DATABASE IF NOT EXISTS attendance_management;
USE attendance_management;

-- =========================================
-- COLLEGE
-- =========================================
CREATE TABLE College (
    college_id INT AUTO_INCREMENT PRIMARY KEY,
    college_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- USER (AUTH BASE TABLE)
-- =========================================
CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    college_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    mobile VARCHAR(15),
    role ENUM('ADMIN','HOD','FACULTY','STUDENT','PARENT') NOT NULL,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (college_id) REFERENCES College(college_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_user_role ON User(role);

-- =========================================
-- DEPARTMENT
-- =========================================
CREATE TABLE Department (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    college_id INT NOT NULL,
    dept_name VARCHAR(100) NOT NULL,
    
    FOREIGN KEY (college_id) REFERENCES College(college_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_dept_college ON Department(college_id);

-- =========================================
-- DIVISION
-- =========================================
CREATE TABLE Division (
    division_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_id INT NOT NULL,
    division_name VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
        ON DELETE CASCADE
);

-- =========================================
-- FACULTY
-- =========================================
CREATE TABLE Faculty (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    dept_id INT NOT NULL,
    short_name VARCHAR(50),
    
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
        ON DELETE CASCADE
);

-- =========================================
-- HOD (ONE PER DEPARTMENT)
-- =========================================
CREATE TABLE HOD (
    hod_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    dept_id INT UNIQUE NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
        ON DELETE CASCADE
);

-- =========================================
-- SUBJECT
-- =========================================
CREATE TABLE Subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_id INT NOT NULL,
    subject_name VARCHAR(120) NOT NULL,
    subject_code VARCHAR(20) UNIQUE,
    
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_subject_dept ON Subject(dept_id);

-- =========================================
-- STUDENT
-- =========================================
CREATE TABLE Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    dept_id INT NOT NULL,
    division_id INT NOT NULL,
    enrollment_no VARCHAR(50) UNIQUE NOT NULL,
    roll_no INT NOT NULL,
    mentor_id INT,
    
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id),
    FOREIGN KEY (division_id) REFERENCES Division(division_id),
    FOREIGN KEY (mentor_id) REFERENCES Faculty(faculty_id)
);

CREATE INDEX idx_student_division ON Student(division_id);

-- =========================================
-- PARENT
-- =========================================
CREATE TABLE Parent (
    parent_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    student_id INT NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
        ON DELETE CASCADE
);

-- =========================================
-- TIMETABLE
-- =========================================
CREATE TABLE TimeTable (
    timetable_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    faculty_id INT NOT NULL,
    division_id INT NOT NULL,
    lecture_no INT NOT NULL,
    lecture_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
        ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id)
        ON DELETE CASCADE,
    FOREIGN KEY (division_id) REFERENCES Division(division_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_timetable_date ON TimeTable(lecture_date);

-- =========================================
-- ATTENDANCE
-- =========================================
CREATE TABLE Attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    faculty_id INT NOT NULL,
    lecture_date DATE NOT NULL,
    lecture_no INT NOT NULL,
    status ENUM('PRESENT','ABSENT') NOT NULL,
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
        ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id),
    
    UNIQUE(student_id, subject_id, lecture_date, lecture_no)
);

CREATE INDEX idx_attendance_student ON Attendance(student_id);

-- =========================================
-- PROXY LECTURE
-- =========================================
CREATE TABLE ProxyLecture (
    proxy_id INT AUTO_INCREMENT PRIMARY KEY,
    original_faculty_id INT NOT NULL,
    substitute_faculty_id INT NOT NULL,
    subject_id INT NOT NULL,
    lecture_date DATE NOT NULL,
    lecture_no INT NOT NULL,
    reason TEXT,
    
    FOREIGN KEY (original_faculty_id) REFERENCES Faculty(faculty_id),
    FOREIGN KEY (substitute_faculty_id) REFERENCES Faculty(faculty_id),
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
);

-- =========================================
-- ACADEMIC CALENDAR
-- =========================================
CREATE TABLE AcademicCalendar (
    calendar_id INT AUTO_INCREMENT PRIMARY KEY,
    college_id INT NOT NULL,
    event_date DATE NOT NULL,
    event_type ENUM('REGULAR','EXAM','HOLIDAY') NOT NULL,
    description VARCHAR(255),
    
    FOREIGN KEY (college_id) REFERENCES College(college_id)
        ON DELETE CASCADE
);