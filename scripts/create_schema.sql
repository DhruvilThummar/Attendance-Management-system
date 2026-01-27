-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 27, 2026 at 12:47 PM
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
-- Table structure for table `academiccalendar`
--

CREATE TABLE `academiccalendar`
(
  `calendar_id` int
(11) NOT NULL,
  `college_id` int
(11) NOT NULL,
  `event_date` date NOT NULL,
  `event_type` enum
('REGULAR','EXAM','HOLIDAY') NOT NULL,
  `description` varchar
(255) DEFAULT NULL
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
  `subject_id` int
(11) NOT NULL,
  `faculty_id` int
(11) NOT NULL,
  `lecture_date` date NOT NULL,
  `lecture_no` int
(11) NOT NULL,
  `status` enum
('PRESENT','ABSENT') NOT NULL,
  `marked_at` timestamp NOT NULL DEFAULT current_timestamp
()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
()
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
(100) NOT NULL
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
(50) NOT NULL
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
(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `hod`
--

CREATE TABLE `hod`
(
  `hod_id` int
(11) NOT NULL,
  `user_id` int
(11) NOT NULL,
  `dept_id` int
(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `parent`
--

CREATE TABLE `parent`
(
  `parent_id` int
(11) NOT NULL,
  `user_id` int
(11) NOT NULL,
  `student_id` int
(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `proxylecture`
--

CREATE TABLE `proxylecture`
(
  `proxy_id` int
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
  `reason` text DEFAULT NULL
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
(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(20) DEFAULT NULL
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
  `lecture_no` int
(11) NOT NULL,
  `lecture_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user`
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
  `role` enum
('ADMIN','HOD','FACULTY','STUDENT','PARENT') NOT NULL,
  `is_approved` tinyint
(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp
()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academiccalendar`
--
ALTER TABLE `academiccalendar`
ADD PRIMARY KEY
(`calendar_id`),
ADD KEY `college_id`
(`college_id`);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
ADD PRIMARY KEY
(`attendance_id`),
ADD UNIQUE KEY `student_id`
(`student_id`,`subject_id`,`lecture_date`,`lecture_no`),
ADD KEY `subject_id`
(`subject_id`),
ADD KEY `faculty_id`
(`faculty_id`),
ADD KEY `idx_attendance_student`
(`student_id`);

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
ADD KEY `idx_dept_college`
(`college_id`);

--
-- Indexes for table `division`
--
ALTER TABLE `division`
ADD PRIMARY KEY
(`division_id`),
ADD KEY `dept_id`
(`dept_id`);

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
-- Indexes for table `hod`
--
ALTER TABLE `hod`
ADD PRIMARY KEY
(`hod_id`),
ADD UNIQUE KEY `user_id`
(`user_id`),
ADD UNIQUE KEY `dept_id`
(`dept_id`);

--
-- Indexes for table `parent`
--
ALTER TABLE `parent`
ADD PRIMARY KEY
(`parent_id`),
ADD UNIQUE KEY `user_id`
(`user_id`),
ADD KEY `student_id`
(`student_id`);

--
-- Indexes for table `proxylecture`
--
ALTER TABLE `proxylecture`
ADD PRIMARY KEY
(`proxy_id`),
ADD KEY `original_faculty_id`
(`original_faculty_id`),
ADD KEY `substitute_faculty_id`
(`substitute_faculty_id`),
ADD KEY `subject_id`
(`subject_id`);

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
(`division_id`);

--
-- Indexes for table `subject`
--
ALTER TABLE `subject`
ADD PRIMARY KEY
(`subject_id`),
ADD UNIQUE KEY `subject_code`
(`subject_code`),
ADD KEY `idx_subject_dept`
(`dept_id`);

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
(`division_id`),
ADD KEY `idx_timetable_date`
(`lecture_date`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
ADD PRIMARY KEY
(`user_id`),
ADD UNIQUE KEY `email`
(`email`),
ADD KEY `college_id`
(`college_id`),
ADD KEY `idx_user_role`
(`role`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `academiccalendar`
--
ALTER TABLE `academiccalendar`
  MODIFY `calendar_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `attendance_id` int
(11) NOT NULL AUTO_INCREMENT;

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
-- AUTO_INCREMENT for table `hod`
--
ALTER TABLE `hod`
  MODIFY `hod_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `parent`
--
ALTER TABLE `parent`
  MODIFY `parent_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `proxylecture`
--
ALTER TABLE `proxylecture`
  MODIFY `proxy_id` int
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
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int
(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `academiccalendar`
--
ALTER TABLE `academiccalendar`
ADD CONSTRAINT `academiccalendar_ibfk_1` FOREIGN KEY
(`college_id`) REFERENCES `college`
(`college_id`) ON
DELETE CASCADE;

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY
(`student_id`) REFERENCES `student`
(`student_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `attendance_ibfk_2` FOREIGN KEY
(`subject_id`) REFERENCES `subject`
(`subject_id`),
ADD CONSTRAINT `attendance_ibfk_3` FOREIGN KEY
(`faculty_id`) REFERENCES `faculty`
(`faculty_id`);

--
-- Constraints for table `department`
--
ALTER TABLE `department`
ADD CONSTRAINT `department_ibfk_1` FOREIGN KEY
(`college_id`) REFERENCES `college`
(`college_id`) ON
DELETE CASCADE;

--
-- Constraints for table `division`
--
ALTER TABLE `division`
ADD CONSTRAINT `division_ibfk_1` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`) ON
DELETE CASCADE;

--
-- Constraints for table `faculty`
--
ALTER TABLE `faculty`
ADD CONSTRAINT `faculty_ibfk_1` FOREIGN KEY
(`user_id`) REFERENCES `user`
(`user_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `faculty_ibfk_2` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`) ON
DELETE CASCADE;

--
-- Constraints for table `hod`
--
ALTER TABLE `hod`
ADD CONSTRAINT `hod_ibfk_1` FOREIGN KEY
(`user_id`) REFERENCES `user`
(`user_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `hod_ibfk_2` FOREIGN KEY
(`dept_id`) REFERENCES `department`
(`dept_id`) ON
DELETE CASCADE;

--
-- Constraints for table `parent`
--
ALTER TABLE `parent`
ADD CONSTRAINT `parent_ibfk_1` FOREIGN KEY
(`user_id`) REFERENCES `user`
(`user_id`) ON
DELETE CASCADE,
ADD CONSTRAINT `parent_ibfk_2` FOREIGN KEY
(`student_id`) REFERENCES `student`
(`student_id`) ON
DELETE CASCADE;

--
-- Constraints for table `proxylecture`
--
ALTER TABLE `proxylecture`
ADD CONSTRAINT `proxylecture_ibfk_1` FOREIGN KEY
(`original_faculty_id`) REFERENCES `faculty`
(`faculty_id`),
ADD CONSTRAINT `proxylecture_ibfk_2` FOREIGN KEY
(`substitute_faculty_id`) REFERENCES `faculty`
(`faculty_id`),
ADD CONSTRAINT `proxylecture_ibfk_3` FOREIGN KEY
(`subject_id`) REFERENCES `subject`
(`subject_id`);

--
-- Constraints for table `student`
--
ALTER TABLE `student`
ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY
(`user_id`) REFERENCES `user`
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
-- Constraints for table `user`
--
ALTER TABLE `user`
ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY
(`college_id`) REFERENCES `college`
(`college_id`) ON
DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
