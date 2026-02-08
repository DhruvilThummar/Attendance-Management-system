-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 08, 2026 at 09:56 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE
= "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone
= "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `attendance_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `academic_calendar`
--

CREATE TABLE `academic_calendar`
(
  `college_id` int
(11) NOT NULL,
  `event_date` date NOT NULL,
  `description` varchar
(255) DEFAULT NULL,
  `dept_id` int
(11) NOT NULL,
  `event_type_id` int
(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version`
(
  `version_num` varchar
(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance`
(
  `attendance_id` int
(11) NOT NULL,
  `student_id` int
(11) NOT NULL,
  `status_id` int
(11) NOT NULL,
  `marked_at` timestamp NOT NULL DEFAULT current_timestamp
(),
  `lecture_id` int
(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attendance_status`
--

CREATE TABLE `attendance_status`
(
  `status_id` int
(11) NOT NULL,
  `status_name` varchar
(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance_status`
--

INSERT INTO `attendance_status` (`
status_id`,
`status_name
`) VALUES
(2, 'ABSENT'),
(4, 'EXCUSED'),
(3, 'LATE'),
(1, 'PRESENT');

-- --------------------------------------------------------

--
-- Table structure for table `college`
--

CREATE TABLE `college`
(
  `college_id` int
(11) NOT NULL,
  `college_name` varchar
(150) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp
(),
  `address` varchar
(255) DEFAULT NULL,
  `email` varchar
(120) DEFAULT NULL,
  `phone` varchar
(20) DEFAULT NULL,
  `website` varchar
(255) DEFAULT NULL,
  `is_approved` tinyint
(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `college`
--

INSERT INTO `college` (`
college_id`,
`college_name
`, `created_at`, `address`, `email`, `phone`, `website`, `is_approved`) VALUES
(2, 'Demo Engineering College', '2026-02-06 23:22:46', '123 Engineering Road, Tech City', 'admin@college.edu', '+91-9876543210', 'https://demo-college.edu', 1);

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department`
(
  `dept_id` int
(11) NOT NULL,
  `college_id` int
(11) NOT NULL,
  `dept_name` varchar
(100) NOT NULL,
  `hod_faculty_id` int
(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`
dept_id`,
`college_id
`, `dept_name`, `hod_faculty_id`) VALUES
(1, 2, 'Computer Science', 1),
(2, 2, 'Information Technology', NULL),
(3, 2, 'Electronics', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `division`
--

CREATE TABLE `division`
(
  `division_id` int
(11) NOT NULL,
  `dept_id` int
(11) NOT NULL,
  `division_name` varchar
(50) NOT NULL,
  `semester_id` int
(11) DEFAULT NULL,
  `capacity` int
(11) DEFAULT NULL,
  `class_teacher_id` int
(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `division`
--

INSERT INTO `division` (`
division_id`,
`dept_id
`, `division_name`, `semester_id`, `capacity`, `class_teacher_id`) VALUES
(1, 1, 'A', 3, 60, 1),
(2, 1, 'B', 3, 60, NULL),
(3, 2, 'A', 3, 60, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `event_type`
--

CREATE TABLE `event_type`
(
  `event_type_id` int
(11) NOT NULL,
  `event_name` varchar
(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `event_type`
--

INSERT INTO `event_type` (`
event_type_id`,
`event_name
`) VALUES
(2, 'EXAM'),
(3, 'HOLIDAY'),
(1, 'REGULAR');

-- --------------------------------------------------------

--
-- Table structure for table `faculty`
--

CREATE TABLE `faculty`
(
  `faculty_id` int
(11) NOT NULL,
  `user_id` int
(11) NOT NULL,
  `dept_id` int
(11) NOT NULL,
  `short_name` varchar
(50) DEFAULT NULL,
  `designation` varchar
(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `faculty`
--

INSERT INTO `faculty` (`
faculty_id`,
`user_id
`, `dept_id`, `short_name`, `designation`) VALUES
(1, 4, 1, 'FM', 'Assistant Professor');

-- --------------------------------------------------------

--
-- Table structure for table `lecture`
--

CREATE TABLE `lecture`
(
  `lecture_id` int
(11) NOT NULL,
  `timetable_id` int
(11) NOT NULL,
  `lecture_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `parent`
--

CREATE TABLE `parent`
(
  `user_id` int
(11) NOT NULL,
  `student_id` int
(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parent`
--

INSERT INTO `parent` (`
user_id`,
`student_id
`) VALUES
(0, 1),
(6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `proxy_lecture`
--

CREATE TABLE `proxy_lecture`
(
  `proxy_id` int
(11) NOT NULL,
  `lecture_id` int
(11) NOT NULL,
  `original_faculty_id` int
(11) NOT NULL,
  `substitute_faculty_id` int
(11) NOT NULL,
  `subject_id` int
(11) NOT NULL,
  `lecture_date` date NOT NULL,
  `lecture_no` int
(11) NOT NULL,
  `room_no` varchar
(20) DEFAULT NULL,
  `building_block` varchar
(50) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `assigned_at` timestamp NOT NULL DEFAULT current_timestamp
(),
  `status_id` int
(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `proxy_status`
--

CREATE TABLE `proxy_status`
(
  `status_id` int
(11) NOT NULL,
  `status_name` varchar
(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `proxy_status`
--

INSERT INTO `proxy_status` (`
status_id`,
`status_name
`) VALUES
(2, 'ACCEPTED'),
(4, 'COMPLETED'),
(1, 'PENDING'),
(3, 'REJECTED');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role`
(
  `role_id` int
(11) NOT NULL,
  `role_name` varchar
(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`
role_id`,
`role_name
`) VALUES
(37, 'ADMIN'),
(39, 'FACULTY'),
(38, 'HOD'),
(41, 'PARENT'),
(40, 'STUDENT'),
(36, 'SUPERADMIN');

-- --------------------------------------------------------

--
-- Table structure for table `semester`
--

CREATE TABLE `semester`
(
  `semester_id` int
(11) NOT NULL,
  `semester_no` int
(11) NOT NULL,
  `academic_year` varchar
(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `semester`
--

INSERT INTO `semester` (`
semester_id`,
`semester_no
`, `academic_year`) VALUES
(1, 1, '2025-2026'),
(2, 2, '2025-2026'),
(3, 3, '2025-2026'),
(4, 4, '2025-2026'),
(5, 5, '2025-2026'),
(6, 6, '2025-2026');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student`
(
  `student_id` int
(11) NOT NULL,
  `user_id` int
(11) NOT NULL,
  `dept_id` int
(11) NOT NULL,
  `division_id` int
(11) NOT NULL,
  `enrollment_no` varchar
(50) NOT NULL,
  `roll_no` int
(11) NOT NULL,
  `mentor_id` int
(11) DEFAULT NULL,
  `semester_id` int
(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`
student_id`,
`user_id
`, `dept_id`, `division_id`, `enrollment_no`, `roll_no`, `mentor_id`, `semester_id`) VALUES
(1, 5, 1, 1, 'CS2023001', 1, 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `subject`
--

CREATE TABLE `subject`
(
  `subject_id` int
(11) NOT NULL,
  `dept_id` int
(11) NOT NULL,
  `subject_name` varchar
(120) NOT NULL,
  `subject_code` varchar
(20) DEFAULT NULL,
  `semester_id` int
(11) NOT NULL,
  `credits` int
(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subject`
--

INSERT INTO `subject` (`
subject_id`,
`dept_id
`, `subject_name`, `subject_code`, `semester_id`, `credits`) VALUES
(1, 1, 'Data Structures', 'CS301', 3, 4),
(2, 1, 'Database Management Systems', 'CS302', 3, 4),
(3, 1, 'Operating Systems', 'CS303', 3, 4),
(4, 1, 'Computer Networks', 'CS304', 3, 3),
(5, 1, 'Web Development', 'CS305', 3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `timetable`
--

CREATE TABLE `timetable`
(
  `timetable_id` int
(11) NOT NULL,
  `subject_id` int
(11) NOT NULL,
  `faculty_id` int
(11) NOT NULL,
  `division_id` int
(11) NOT NULL,
  `day_of_week` enum
('MON','TUE','WED','THU','FRI','SAT') NOT NULL,
  `lecture_no` int
(11) NOT NULL,
  `room_no` varchar
(20) DEFAULT NULL,
  `building_block` varchar
(50) DEFAULT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `timetable`
--

INSERT INTO `timetable` (`
timetable_id`,
`subject_id
`, `faculty_id`, `division_id`, `day_of_week`, `lecture_no`, `room_no`, `building_block`, `start_time`, `end_time`) VALUES
(0, 2, 1, 1, 'MON', 1, 'B-202', NULL, '11:40:00', '13:43:00'),
(1, 1, 1, 1, 'MON', 1, '101', 'A', '09:00:00', '10:00:00'),
(2, 2, 1, 1, 'MON', 2, '101', 'A', '10:00:00', '11:00:00'),
(3, 3, 1, 1, 'TUE', 1, '101', 'A', '09:00:00', '10:00:00'),
(4, 4, 1, 1, 'TUE', 2, '102', 'A', '10:00:00', '11:00:00'),
(5, 5, 1, 1, 'WED', 1, '103', 'A', '09:00:00', '10:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users`
(
  `user_id` int
(11) NOT NULL,
  `college_id` int
(11) NOT NULL,
  `name` varchar
(100) NOT NULL,
  `email` varchar
(120) NOT NULL,
  `password_hash` varchar
(255) NOT NULL,
  `mobile` varchar
(15) DEFAULT NULL,
  `role_id` int
(11) NOT NULL,
  `is_approved` tinyint
(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp
()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`
user_id`,
`college_id
`, `name`, `email`, `password_hash`, `mobile`, `role_id`, `is_approved`, `created_at`) VALUES
(1, 2, 'System Administrator', 'Admin@edu.com', 'PW-289-09-97-321-67-031-37-421-07-721-76-97-46-26-16-16-85-06END', '+91-9000000001', 36, 1, '2026-02-07 04:48:45'),
(2, 2, 'College Administrator', 'admin@college.edu', 'PW-289-09-97-321-67-031-37-421-07-721-76-97-46-26-16-16-85-06END', '+91-9000000002', 37, 1, '2026-02-07 04:48:45'),
(3, 2, 'Computer Science HOD', 'hod@college.edu', 'PW-477-321-17-821-86-511-56-77-26-06-95-95-65-85END', '+91-9000000003', 38, 1, '2026-02-07 04:48:45'),
(4, 2, 'Faculty Member', 'faculty@college.edu', 'PW-0811-331-78-621-48-621-18-241-87-131-57-731-27-041-96-18-66-46-36-36-06-26END', '+91-9000000004', 39, 1, '2026-02-07 04:48:45'),
(5, 2, 'Student User', 'student@college.edu', 'PW-4812-941-18-841-88-741-58-821-28-721-97-431-67-831-37-48-07-76-76-66-46-56-16-54END', '+91-9000000005', 40, 1, '2026-02-07 04:48:45'),
(6, 2, 'Demo Parent', 'parent@college.edu', 'PW-6810-041-38-321-08-831-77-321-47-031-17-431-86-08-56-36-26-26-95-16END', '9876543210', 41, 1, '2026-02-08 05:27:28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academic_calendar`
--
ALTER TABLE `academic_calendar`
ADD KEY `college_id`
(`college_id`),
ADD KEY `dept_id`
(`dept_id`),
ADD KEY `fk_calendar_event_type`
(`event_type_id`);

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
ADD PRIMARY KEY
(`version_num`);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
ADD PRIMARY KEY
(`attendance_id`),
ADD UNIQUE KEY `student_id`
(`student_id`,`lecture_id`),
ADD KEY `idx_attendance_student`
(`student_id`),
ADD KEY `fk_attendance_status`
(`status_id`),
ADD KEY `fk_attendance_lecture`
(`lecture_id`);

--
-- Indexes for table `attendance_status`
--
ALTER TABLE `attendance_status`
ADD PRIMARY KEY
(`status_id`),
ADD UNIQUE KEY `status_name`
(`status_name`);

--
-- Indexes for table `college`
--
ALTER TABLE `college`
ADD PRIMARY KEY
(`college_id`);

--
-- Indexes for table `department`
--
ALTER TABLE `department`
ADD PRIMARY KEY
(`dept_id`),
ADD UNIQUE KEY `hod_faculty_id`
(`hod_faculty_id`),
ADD KEY `idx_dept_college`
(`college_id`);

--
-- Indexes for table `division`
--
ALTER TABLE `division`
ADD PRIMARY KEY
(`division_id`),
ADD KEY `dept_id`
(`dept_id`),
ADD KEY `fk_division_semester`
(`semester_id`),
ADD KEY `fk_division_class_teacher`
(`class_teacher_id`);

--
-- Indexes for table `event_type`
--
ALTER TABLE `event_type`
ADD PRIMARY KEY
(`event_type_id`),
ADD UNIQUE KEY `event_name`
(`event_name`);

--
-- Indexes for table `faculty`
--
ALTER TABLE `faculty`
ADD PRIMARY KEY
(`faculty_id`),
ADD UNIQUE KEY `user_id`
(`user_id`),
ADD KEY `dept_id`
(`dept_id`);

--
-- Indexes for table `lecture`
--
ALTER TABLE `lecture`
ADD PRIMARY KEY
(`lecture_id`),
ADD UNIQUE KEY `timetable_id`
(`timetable_id`,`lecture_date`);

--
-- Indexes for table `parent`
--
ALTER TABLE `parent`
ADD PRIMARY KEY
(`user_id`,`student_id`),
ADD KEY `student_id`
(`student_id`);

--
-- Indexes for table `proxy_lecture`
--
ALTER TABLE `proxy_lecture`
ADD PRIMARY KEY
(`proxy_id`),
ADD KEY `original_faculty_id`
(`original_faculty_id`),
ADD KEY `substitute_faculty_id`
(`substitute_faculty_id`),
ADD KEY `subject_id`
(`subject_id`),
ADD KEY `fk_proxy_lecture_id`
(`lecture_id`),
ADD KEY `fk_proxy_status`
(`status_id`);

--
-- Indexes for table `proxy_status`
--
ALTER TABLE `proxy_status`
ADD PRIMARY KEY
(`status_id`),
ADD UNIQUE KEY `status_name`
(`status_name`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
ADD PRIMARY KEY
(`role_id`),
ADD UNIQUE KEY `role_name`
(`role_name`);

--
-- Indexes for table `semester`
--
ALTER TABLE `semester`
ADD PRIMARY KEY
(`semester_id`),
ADD UNIQUE KEY `semester_no`
(`semester_no`,`academic_year`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
ADD PRIMARY KEY
(`student_id`),
ADD UNIQUE KEY `user_id`
(`user_id`),
ADD UNIQUE KEY `enrollment_no`
(`enrollment_no`),
ADD KEY `dept_id`
(`dept_id`),
ADD KEY `mentor_id`
(`mentor_id`),
ADD KEY `idx_student_division`
(`division_id`),
ADD KEY `fk_student_semester`
(`semester_id`);

--
-- Indexes for table `subject`
--
ALTER TABLE `subject`
ADD PRIMARY KEY
(`subject_id`),
ADD UNIQUE KEY `subject_code`
(`subject_code`),
ADD KEY `idx_subject_dept`
(`dept_id`),
ADD KEY `fk_subject_semester`
(`semester_id`);

--
-- Indexes for table `timetable`
--
ALTER TABLE `timetable`
ADD PRIMARY KEY
(`timetable_id`),
ADD KEY `subject_id`
(`subject_id`),
ADD KEY `faculty_id`
(`faculty_id`),
ADD KEY `division_id`
(`division_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
ADD PRIMARY KEY
(`user_id`),
ADD UNIQUE KEY `email`
(`email`),
ADD KEY `college_id`
(`college_id`),
ADD KEY `fk_user_role`
(`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `attendance_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attendance_status`
--
ALTER TABLE `attendance_status`
  MODIFY `status_id` int
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `college`
--
ALTER TABLE `college`
  MODIFY `college_id` int
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `department`
  MODIFY `dept_id` int
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `division`
--
ALTER TABLE `division`
  MODIFY `division_id` int
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `event_type`
--
ALTER TABLE `event_type`
  MODIFY `event_type_id` int
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `faculty`
--
ALTER TABLE `faculty`
  MODIFY `faculty_id` int
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `lecture`
--
ALTER TABLE `lecture`
  MODIFY `lecture_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `proxy_lecture`
--
ALTER TABLE `proxy_lecture`
  MODIFY `proxy_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `proxy_status`
--
ALTER TABLE `proxy_status`
  MODIFY `status_id` int
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `role_id` int
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `semester`
--
ALTER TABLE `semester`
  MODIFY `semester_id` int
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `academic_calendar`
--
ALTER TABLE `academic_calendar`
ADD CONSTRAINT `fk_calendar_college` FOREIGN KEY
(`college_id`) REFERENCES `college`
(`college_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `fk_calendar_dept` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `fk_calendar_event_type` FOREIGN KEY
(`event_type_id`) REFERENCES `event_type`
(`event_type_id`);

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
ADD CONSTRAINT `fk_attendance_lecture` FOREIGN KEY
(`lecture_id`) REFERENCES `lecture`
(`lecture_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `fk_attendance_status` FOREIGN KEY
(`status_id`) REFERENCES `attendance_status`
(`status_id`),
ADD CONSTRAINT `fk_attendance_student` FOREIGN KEY
(`student_id`) REFERENCES `student`
(`student_id`) ON
DELETE CASCADE;

--
-- Constraints for table `department`
--
ALTER TABLE `department`
ADD CONSTRAINT `fk_department_college` FOREIGN KEY
(`college_id`) REFERENCES `college`
(`college_id`) ON
DELETE CASCADE;

--
-- Constraints for table `division`
--
ALTER TABLE `division`
ADD CONSTRAINT `fk_division_class_teacher` FOREIGN KEY
(`class_teacher_id`) REFERENCES `faculty`
(`faculty_id`) ON
DELETE
SET NULL
,
ADD CONSTRAINT `fk_division_dept` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `fk_division_semester` FOREIGN KEY
(`semester_id`) REFERENCES `semester`
(`semester_id`) ON
DELETE
SET NULL;

--
-- Constraints for table `faculty`
--
ALTER TABLE `faculty`
ADD CONSTRAINT `fk_faculty_dept` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `fk_faculty_user` FOREIGN KEY
(`user_id`) REFERENCES `users`
(`user_id`) ON
DELETE CASCADE;

--
-- Constraints for table `lecture`
--
ALTER TABLE `lecture`
ADD CONSTRAINT `fk_lecture_timetable` FOREIGN KEY
(`timetable_id`) REFERENCES `timetable`
(`timetable_id`) ON
DELETE CASCADE;

--
-- Constraints for table `proxy_lecture`
--
ALTER TABLE `proxy_lecture`
ADD CONSTRAINT `fk_proxy_lecture` FOREIGN KEY
(`lecture_id`) REFERENCES `lecture`
(`lecture_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `fk_proxy_original_faculty` FOREIGN KEY
(`original_faculty_id`) REFERENCES `faculty`
(`faculty_id`),
ADD CONSTRAINT `fk_proxy_status` FOREIGN KEY
(`status_id`) REFERENCES `proxy_status`
(`status_id`),
ADD CONSTRAINT `fk_proxy_sub_faculty` FOREIGN KEY
(`substitute_faculty_id`) REFERENCES `faculty`
(`faculty_id`),
ADD CONSTRAINT `fk_proxy_subject` FOREIGN KEY
(`subject_id`) REFERENCES `subject`
(`subject_id`);

--
-- Constraints for table `student`
--
ALTER TABLE `student`
ADD CONSTRAINT `fk_student_dept` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`),
ADD CONSTRAINT `fk_student_division` FOREIGN KEY
(`division_id`) REFERENCES `division`
(`division_id`),
ADD CONSTRAINT `fk_student_mentor` FOREIGN KEY
(`mentor_id`) REFERENCES `faculty`
(`faculty_id`) ON
DELETE
SET NULL
,
ADD CONSTRAINT `fk_student_user` FOREIGN KEY
(`user_id`) REFERENCES `users`
(`user_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY
(`mentor_id`) REFERENCES `faculty`
(`faculty_id`);

--
-- Constraints for table `subject`
--
ALTER TABLE `subject`
ADD CONSTRAINT `fk_subject_dept` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`),
ADD CONSTRAINT `fk_subject_semester` FOREIGN KEY
(`semester_id`) REFERENCES `semester`
(`semester_id`);

--
-- Constraints for table `timetable`
--
ALTER TABLE `timetable`
ADD CONSTRAINT `fk_timetable_division` FOREIGN KEY
(`division_id`) REFERENCES `division`
(`division_id`),
ADD CONSTRAINT `fk_timetable_faculty` FOREIGN KEY
(`faculty_id`) REFERENCES `faculty`
(`faculty_id`),
ADD CONSTRAINT `fk_timetable_subject` FOREIGN KEY
(`subject_id`) REFERENCES `subject`
(`subject_id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
ADD CONSTRAINT `fk_user_college` FOREIGN KEY
(`college_id`) REFERENCES `college`
(`college_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `fk_user_role` FOREIGN KEY
(`role_id`) REFERENCES `role`
(`role_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
