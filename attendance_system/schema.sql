-- Active: 1766585343625@@127.0.0.1@3306

--
-- Database: `attendance_db`
--

CREATE TABLE `academic_calendar` (
    `id` int(11) NOT NULL,
    `college_id` int(11) DEFAULT NULL,
    `title` varchar(255) NOT NULL,
    `start_date` date NOT NULL,
    `end_date` date DEFAULT NULL,
    `type` varchar(50) DEFAULT NULL,
    `description` text DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp ()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
    `id` int(11) NOT NULL,
    `lecture_id` int(11) DEFAULT NULL,
    `student_id` int(11) DEFAULT NULL,
    `status` varchar(10) NOT NULL CHECK (`status` in ('P', 'A')),
    `marked_at` timestamp NOT NULL DEFAULT current_timestamp ()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attendance_audit`
--

CREATE TABLE `attendance_audit` (
    `id` int(11) NOT NULL,
    `attendance_id` int(11) DEFAULT NULL,
    `old_status` varchar(10) DEFAULT NULL,
    `new_status` varchar(10) DEFAULT NULL,
    `edited_by` int(11) DEFAULT NULL,
    `edited_at` timestamp NOT NULL DEFAULT current_timestamp (),
    `reason` text DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `colleges`
--

CREATE TABLE `colleges` (
    `id` int(11) NOT NULL,
    `name` varchar(255) NOT NULL,
    `subscription_status` varchar(50) DEFAULT 'Active',
    `created_at` timestamp NOT NULL DEFAULT current_timestamp (),
    `updated_at` timestamp NOT NULL DEFAULT current_timestamp () ON UPDATE current_timestamp ()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Dumping data for table `colleges`
--

INSERT INTO
    `colleges` (
        `id`,
        `name`,
        `subscription_status`,
        `created_at`,
        `updated_at`
    )
VALUES (
        1,
        'LJKU Institute of Engineering',
        'Active',
        '2026-01-24 11:39:54',
        '2026-01-24 13:09:24'
    );

-- --------------------------------------------------------

--
-- Table structure for table `divisions`
--

CREATE TABLE `divisions` (
    `id` int(11) NOT NULL,
    `college_id` int(11) DEFAULT NULL,
    `name` varchar(50) NOT NULL,
    `semester` int(11) NOT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp ()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Dumping data for table `divisions`
--

INSERT INTO
    `divisions` (
        `id`,
        `college_id`,
        `name`,
        `semester`,
        `created_at`
    )
VALUES (
        1,
        1,
        'Div A',
        3,
        '2026-01-24 13:09:24'
    ),
    (
        2,
        1,
        'Div B',
        3,
        '2026-01-24 13:09:24'
    );

-- --------------------------------------------------------

--
-- Table structure for table `faculties`
--

CREATE TABLE `faculties` (
    `id` int(11) NOT NULL,
    `user_id` int(11) DEFAULT NULL,
    `department` varchar(100) DEFAULT NULL,
    `short_name` varchar(10) DEFAULT NULL,
    `phone_number` varchar(20) DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp ()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Dumping data for table `faculties`
--

INSERT INTO
    `faculties` (
        `id`,
        `user_id`,
        `department`,
        `short_name`,
        `phone_number`,
        `created_at`
    )
VALUES (
        1,
        4,
        'Computer Engineering',
        'RKS',
        '9898989898',
        '2026-01-24 13:09:24'
    );

-- --------------------------------------------------------

--
-- Stand-in structure for view `faculty_teaching_load`
-- (See below for the actual view)
--
CREATE TABLE `faculty_teaching_load` (
    `faculty_id` int(11),
    `faculty_name` varchar(255),
    `short_name` varchar(10),
    `college_id` int(11),
    `timetable_entries` bigint (21),
    `lectures_conducted` bigint (21),
    `subjects_taught` bigint (21)
);

-- --------------------------------------------------------

--
-- Table structure for table `hods`
--

CREATE TABLE `hods` (
    `id` int(11) NOT NULL,
    `user_id` int(11) DEFAULT NULL,
    `department_id` int(11) DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp ()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Dumping data for table `hods`
--

INSERT INTO
    `hods` (
        `id`,
        `user_id`,
        `department_id`,
        `created_at`
    )
VALUES (
        1,
        3,
        101,
        '2026-01-24 13:09:24'
    );

-- --------------------------------------------------------

--
-- Table structure for table `lectures`
--

CREATE TABLE `lectures` (
    `id` int(11) NOT NULL,
    `timetable_id` int(11) DEFAULT NULL,
    `date` date NOT NULL,
    `proxy_faculty_id` int(11) DEFAULT NULL,
    `status` varchar(20) DEFAULT 'Scheduled',
    `created_at` timestamp NOT NULL DEFAULT current_timestamp ()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
    `id` int(11) NOT NULL,
    `user_id` int(11) DEFAULT NULL,
    `message` text NOT NULL,
    `seen` tinyint (1) DEFAULT 0,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp (),
    `type` varchar(20) DEFAULT 'Info'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
    `id` int(11) NOT NULL,
    `user_id` int(11) DEFAULT NULL,
    `enrollment_no` varchar(50) NOT NULL,
    `roll_no` varchar(20) DEFAULT NULL,
    `branch` varchar(100) DEFAULT NULL,
    `phone_number` varchar(20) DEFAULT NULL,
    `mentor_name` varchar(100) DEFAULT NULL,
    `division_id` int(11) DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp ()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO
    `students` (
        `id`,
        `user_id`,
        `enrollment_no`,
        `roll_no`,
        `branch`,
        `phone_number`,
        `mentor_name`,
        `division_id`,
        `created_at`
    )
VALUES (
        1,
        5,
        'E2023001',
        '101',
        'Computer Engineering',
        '9876543210',
        'Prof. Mentor',
        1,
        '2026-01-24 13:09:24'
    );

-- --------------------------------------------------------

--
-- Stand-in structure for view `student_attendance_summary`
-- (See below for the actual view)
--
CREATE TABLE `student_attendance_summary` (
    `student_id` int(11),
    `enrollment_no` varchar(50),
    `student_name` varchar(255),
    `college_id` int(11),
    `division_id` int(11),
    `total_lectures` bigint (21),
    `present_count` decimal(22, 0),
    `absent_count` decimal(22, 0),
    `attendance_percentage` decimal(28, 2)
);

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
    `id` int(11) NOT NULL,
    `college_id` int(11) DEFAULT NULL,
    `code` varchar(20) NOT NULL,
    `name` varchar(255) NOT NULL,
    `branch` varchar(100) DEFAULT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp (),
    `credits` int(11) DEFAULT 4
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `timetable`
--

CREATE TABLE `timetable` (
    `id` int(11) NOT NULL,
    `subject_id` int(11) DEFAULT NULL,
    `faculty_id` int(11) DEFAULT NULL,
    `division_id` int(11) DEFAULT NULL,
    `day` varchar(20) NOT NULL,
    `slot` varchar(50) NOT NULL,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp ()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
    `id` int(11) NOT NULL,
    `college_id` int(11) DEFAULT NULL,
    `email` varchar(255) NOT NULL,
    `name` varchar(255) DEFAULT NULL,
    `password` text NOT NULL,
    `role` varchar(50) NOT NULL CHECK (
        `role` in (
            'SuperAdmin',
            'CollegeAdmin',
            'HOD',
            'Faculty',
            'Student'
        )
    ),
    `is_approved` tinyint (1) DEFAULT 0,
    `created_at` timestamp NOT NULL DEFAULT current_timestamp (),
    `updated_at` timestamp NOT NULL DEFAULT current_timestamp () ON UPDATE current_timestamp ()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO
    `users` (
        `id`,
        `college_id`,
        `email`,
        `name`,
        `password`,
        `role`,
        `is_approved`,
        `created_at`,
        `updated_at`
    )
VALUES (
        1,
        1,
        'Admin@edu.com',
        'Super Admin',
        'AdminPassword123!',
        'SuperAdmin',
        1,
        '2026-01-24 13:09:24',
        '2026-01-24 13:09:24'
    ),
    (
        2,
        1,
        'admin@college.edu',
        'College Admin',
        'AdminPassword123!',
        'CollegeAdmin',
        1,
        '2026-01-24 13:09:24',
        '2026-01-24 13:09:24'
    ),
    (
        3,
        1,
        'hod@college.edu',
        'Dr. HOD',
        'HODPassword123!',
        'HOD',
        1,
        '2026-01-24 13:09:24',
        '2026-01-24 13:09:24'
    ),
    (
        4,
        1,
        'faculty@college.edu',
        'Ravi Kumar Sharma',
        'FacultyPassword123!',
        'Faculty',
        1,
        '2026-01-24 13:09:24',
        '2026-01-24 13:09:24'
    ),
    (
        5,
        1,
        'student@college.edu',
        'Student Name',
        'StudentPassword123!',
        'Student',
        1,
        '2026-01-24 13:09:24',
        '2026-01-24 13:09:24'
    );

-- --------------------------------------------------------

--
-- Structure for view `faculty_teaching_load`
--
DROP TABLE IF EXISTS `faculty_teaching_load`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `faculty_teaching_load`  AS SELECT `f`.`id` AS `faculty_id`, `u`.`name` AS `faculty_name`, `f`.`short_name` AS `short_name`, `u`.`college_id` AS `college_id`, count(distinct `t`.`id`) AS `timetable_entries`, count(distinct `l`.`id`) AS `lectures_conducted`, count(distinct `sub`.`id`) AS `subjects_taught` FROM ((((`faculties` `f` join `users` `u` on(`f`.`user_id` = `u`.`id`)) left join `timetable` `t` on(`f`.`id` = `t`.`faculty_id`)) left join `lectures` `l` on(`t`.`id` = `l`.`timetable_id`)) left join `subjects` `sub` on(`t`.`subject_id` = `sub`.`id`)) GROUP BY `f`.`id`, `u`.`name`, `f`.`short_name`, `u`.`college_id` ;

-- --------------------------------------------------------

--
-- Structure for view `student_attendance_summary`
--
DROP TABLE IF EXISTS `student_attendance_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `student_attendance_summary`  AS SELECT `s`.`id` AS `student_id`, `s`.`enrollment_no` AS `enrollment_no`, `u`.`name` AS `student_name`, `u`.`college_id` AS `college_id`, `s`.`division_id` AS `division_id`, count(`a`.`id`) AS `total_lectures`, sum(case when `a`.`status` in ('Present','P','Late') then 1 else 0 end) AS `present_count`, sum(case when `a`.`status` in ('Absent','A') then 1 else 0 end) AS `absent_count`, round(sum(case when `a`.`status` in ('Present','P','Late') then 1 else 0 end) * 100.0 / nullif(count(`a`.`id`),0),2) AS `attendance_percentage` FROM ((`students` `s` join `users` `u` on(`s`.`user_id` = `u`.`id`)) left join `attendance` `a` on(`s`.`id` = `a`.`student_id`)) GROUP BY `s`.`id`, `s`.`enrollment_no`, `u`.`name`, `u`.`college_id`, `s`.`division_id` ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academic_calendar`
--
ALTER TABLE `academic_calendar`
ADD PRIMARY KEY (`id`),
ADD KEY `idx_calendar_college_dates` (
    `college_id`,
    `start_date`,
    `end_date`
),
ADD KEY `idx_calendar_type` (`type`),
ADD KEY `idx_calendar_start_date` (`start_date`);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `lecture_id` (`lecture_id`, `student_id`),
ADD KEY `idx_attendance_lecture` (`lecture_id`),
ADD KEY `idx_attendance_student` (`student_id`),
ADD KEY `idx_attendance_status` (`status`),
ADD KEY `idx_attendance_student_status` (`student_id`, `status`);

--
-- Indexes for table `attendance_audit`
--
ALTER TABLE `attendance_audit`
ADD PRIMARY KEY (`id`),
ADD KEY `idx_audit_attendance` (`attendance_id`),
ADD KEY `idx_audit_edited_by` (`edited_by`),
ADD KEY `idx_audit_edited_at` (`edited_at`);

--
-- Indexes for table `colleges`
--
ALTER TABLE `colleges`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `divisions`
--
ALTER TABLE `divisions`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `unique_division` (
    `college_id`,
    `name`,
    `semester`
),
ADD KEY `idx_divisions_college_semester` (`college_id`, `semester`);

--
-- Indexes for table `faculties`
--
ALTER TABLE `faculties`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `user_id` (`user_id`),
ADD KEY `idx_faculties_department` (`department`),
ADD KEY `idx_faculties_short_name` (`short_name`);

--
-- Indexes for table `hods`
--
ALTER TABLE `hods`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `user_id` (`user_id`),
ADD KEY `idx_hods_department` (`department_id`);

--
-- Indexes for table `lectures`
--
ALTER TABLE `lectures`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `unique_lecture` (`timetable_id`, `date`),
ADD KEY `idx_lectures_date` (`date`),
ADD KEY `idx_lectures_status` (`status`),
ADD KEY `idx_lectures_proxy` (`proxy_faculty_id`),
ADD KEY `idx_lectures_date_status` (`date`, `status`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
ADD PRIMARY KEY (`id`),
ADD KEY `idx_notifications_user_seen` (`user_id`, `seen`),
ADD KEY `idx_notifications_created` (`created_at`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `enrollment_no` (`enrollment_no`),
ADD UNIQUE KEY `user_id` (`user_id`),
ADD KEY `idx_students_enrollment` (`enrollment_no`),
ADD KEY `idx_students_division` (`division_id`),
ADD KEY `idx_students_branch` (`branch`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `college_id` (`college_id`, `code`),
ADD KEY `idx_subjects_college_branch` (`college_id`, `branch`),
ADD KEY `idx_subjects_code` (`code`);

--
-- Indexes for table `timetable`
--
ALTER TABLE `timetable`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `unique_slot` (`division_id`, `day`, `slot`),
ADD KEY `idx_timetable_faculty` (`faculty_id`),
ADD KEY `idx_timetable_subject` (`subject_id`),
ADD KEY `idx_timetable_division_day` (`division_id`, `day`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `email` (`email`),
ADD KEY `idx_users_college_role` (`college_id`, `role`),
ADD KEY `idx_users_email` (`email`),
ADD KEY `idx_users_approval` (`is_approved`, `role`),
ADD KEY `idx_users_college_approved` (`college_id`, `is_approved`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `academic_calendar`
--
ALTER TABLE `academic_calendar` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attendance_audit`
--
ALTER TABLE `attendance_audit` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `colleges`
--
ALTER TABLE `colleges` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 2;

--
-- AUTO_INCREMENT for table `divisions`
--
ALTER TABLE `divisions` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 3;

--
-- AUTO_INCREMENT for table `faculties`
--
ALTER TABLE `faculties` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 2;

--
-- AUTO_INCREMENT for table `hods`
--
ALTER TABLE `hods` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 2;

--
-- AUTO_INCREMENT for table `lectures`
--
ALTER TABLE `lectures` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 3;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 2;

--
-- AUTO_INCREMENT for table `subjects`
--
ALTER TABLE `subjects` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 75;

--
-- AUTO_INCREMENT for table `timetable`
--
ALTER TABLE `timetable` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 632;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `academic_calendar`
--
ALTER TABLE `academic_calendar`
ADD CONSTRAINT `academic_calendar_ibfk_1` FOREIGN KEY (`college_id`) REFERENCES `colleges` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`lecture_id`) REFERENCES `lectures` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `attendance_audit`
--
ALTER TABLE `attendance_audit`
ADD CONSTRAINT `attendance_audit_ibfk_1` FOREIGN KEY (`attendance_id`) REFERENCES `attendance` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `attendance_audit_ibfk_2` FOREIGN KEY (`edited_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `divisions`
--
ALTER TABLE `divisions`
ADD CONSTRAINT `divisions_ibfk_1` FOREIGN KEY (`college_id`) REFERENCES `colleges` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `faculties`
--
ALTER TABLE `faculties`
ADD CONSTRAINT `faculties_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `hods`
--
ALTER TABLE `hods`
ADD CONSTRAINT `hods_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `lectures`
--
ALTER TABLE `lectures`
ADD CONSTRAINT `lectures_ibfk_1` FOREIGN KEY (`timetable_id`) REFERENCES `timetable` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `lectures_ibfk_2` FOREIGN KEY (`proxy_faculty_id`) REFERENCES `faculties` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `students`
--
ALTER TABLE `students`
ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `students_ibfk_2` FOREIGN KEY (`division_id`) REFERENCES `divisions` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `subjects`
--
ALTER TABLE `subjects`
ADD CONSTRAINT `subjects_ibfk_1` FOREIGN KEY (`college_id`) REFERENCES `colleges` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `timetable`
--
ALTER TABLE `timetable`
ADD CONSTRAINT `timetable_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `timetable_ibfk_2` FOREIGN KEY (`faculty_id`) REFERENCES `faculties` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `timetable_ibfk_3` FOREIGN KEY (`division_id`) REFERENCES `divisions` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`college_id`) REFERENCES `colleges` (`id`) ON DELETE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;