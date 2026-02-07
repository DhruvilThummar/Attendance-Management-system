-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 27, 2026 at 03:48 PM
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
-- Database: `databse`
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
  `event_type` enum
('REGULAR','EXAM','HOLIDAY') NOT NULL,
  `description` varchar
(255) DEFAULT NULL,
  `dept_id` int
(11) NOT NULL
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
(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `class_teacher` varchar
(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `status` enum
('PENDING','ACCEPTED','REJECTED','COMPLETED') DEFAULT 'PENDING',
  `assigned_at` timestamp NOT NULL DEFAULT current_timestamp
()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(1, 'ADMIN'),
(3, 'FACULTY'),
(2, 'HOD'),
(5, 'PARENT'),
(4, 'STUDENT');

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
) ;

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
) ;

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
-- Indexes for dumped tables
--

--
-- Indexes for table `academic_calendar`
--
ALTER TABLE `academic_calendar`
ADD KEY `college_id`
(`college_id`),
ADD KEY `dept_id`
(`dept_id`);

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
(`semester_id`);

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
ADD UNIQUE KEY `user_id`
(`user_id`),
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
(`lecture_id`);

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
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `college`
--
ALTER TABLE `college`
  MODIFY `college_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `department`
  MODIFY `dept_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `division`
--
ALTER TABLE `division`
  MODIFY `division_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `faculty`
--
ALTER TABLE `faculty`
  MODIFY `faculty_id` int
(11) NOT NULL AUTO_INCREMENT;

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
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `role_id` int
(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `semester`
--
ALTER TABLE `semester`
  MODIFY `semester_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `student_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `subject`
--
ALTER TABLE `subject`
  MODIFY `subject_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `timetable`
--
ALTER TABLE `timetable`
  MODIFY `timetable_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `academic_calendar`
--
ALTER TABLE `academic_calendar`
ADD CONSTRAINT `academic_calendar_ibfk_1` FOREIGN KEY
(`college_id`) REFERENCES `college`
(`college_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `academic_calendar_ibfk_2` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`);

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY
(`student_id`) REFERENCES `student`
(`student_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `fk_attendance_lecture` FOREIGN KEY
(`lecture_id`) REFERENCES `lecture`
(`lecture_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `fk_attendance_status` FOREIGN KEY
(`status_id`) REFERENCES `attendance_status`
(`status_id`);

--
-- Constraints for table `department`
--
ALTER TABLE `department`
ADD CONSTRAINT `department_ibfk_1` FOREIGN KEY
(`college_id`) REFERENCES `college`
(`college_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `fk_department_hod` FOREIGN KEY
(`hod_faculty_id`) REFERENCES `faculty`
(`faculty_id`) ON
DELETE
SET NULL;

--
-- Constraints for table `division`
--
ALTER TABLE `division`
ADD CONSTRAINT `division_ibfk_1` FOREIGN KEY
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
ADD CONSTRAINT `faculty_ibfk_1` FOREIGN KEY
(`user_id`) REFERENCES `users`
(`user_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `faculty_ibfk_2` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`) ON
DELETE CASCADE;

--
-- Constraints for table `lecture`
--
ALTER TABLE `lecture`
ADD CONSTRAINT `lecture_ibfk_1` FOREIGN KEY
(`timetable_id`) REFERENCES `timetable`
(`timetable_id`) ON
DELETE CASCADE;

--
-- Constraints for table `parent`
--
ALTER TABLE `parent`
ADD CONSTRAINT `parent_ibfk_1` FOREIGN KEY
(`user_id`) REFERENCES `users`
(`user_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `parent_ibfk_2` FOREIGN KEY
(`student_id`) REFERENCES `student`
(`student_id`) ON
DELETE CASCADE;

--
-- Constraints for table `proxy_lecture`
--
ALTER TABLE `proxy_lecture`
ADD CONSTRAINT `fk_proxy_lecture_id` FOREIGN KEY
(`lecture_id`) REFERENCES `lecture`
(`lecture_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `proxy_lecture_ibfk_1` FOREIGN KEY
(`original_faculty_id`) REFERENCES `faculty`
(`faculty_id`),
ADD CONSTRAINT `proxy_lecture_ibfk_2` FOREIGN KEY
(`substitute_faculty_id`) REFERENCES `faculty`
(`faculty_id`),
ADD CONSTRAINT `proxy_lecture_ibfk_3` FOREIGN KEY
(`subject_id`) REFERENCES `subject`
(`subject_id`);

--
-- Constraints for table `student`
--
ALTER TABLE `student`
ADD CONSTRAINT `fk_student_semester` FOREIGN KEY
(`semester_id`) REFERENCES `semester`
(`semester_id`),
ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY
(`user_id`) REFERENCES `users`
(`user_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `student_ibfk_2` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`),
ADD CONSTRAINT `student_ibfk_3` FOREIGN KEY
(`division_id`) REFERENCES `division`
(`division_id`),
ADD CONSTRAINT `student_ibfk_4` FOREIGN KEY
(`mentor_id`) REFERENCES `faculty`
(`faculty_id`);

--
-- Constraints for table `subject`
--
ALTER TABLE `subject`
ADD CONSTRAINT `fk_subject_semester` FOREIGN KEY
(`semester_id`) REFERENCES `semester`
(`semester_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `subject_ibfk_1` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`) ON
DELETE CASCADE;

--
-- Constraints for table `timetable`
--
ALTER TABLE `timetable`
ADD CONSTRAINT `timetable_ibfk_1` FOREIGN KEY
(`subject_id`) REFERENCES `subject`
(`subject_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `timetable_ibfk_2` FOREIGN KEY
(`faculty_id`) REFERENCES `faculty`
(`faculty_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `timetable_ibfk_3` FOREIGN KEY
(`division_id`) REFERENCES `division`
(`division_id`) ON
DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
ADD CONSTRAINT `fk_user_role` FOREIGN KEY
(`role_id`) REFERENCES `role`
(`role_id`),
ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY
(`college_id`) REFERENCES `college`
(`college_id`) ON
DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
