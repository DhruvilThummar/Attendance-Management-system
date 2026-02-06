"""
Mock Data Service

This module provides mock data for development/testing.
When transitioning to a real database, replace these functions with actual database queries.
"""

from datetime import datetime, timedelta


class MockDataService:
    """Service to provide mock data matching the database models"""

    _college = {
        'college_id': 1,
        'college_name': 'ABC Engineering College',
        'created_at': datetime(2020, 1, 1)
    }

    _departments = [
        {
            'dept_id': 1,
            'college_id': 1,
            'dept_name': 'Computer Science & Engineering',
            'hod_faculty_id': 1,
            'code': 'CSE'
        },
        {
            'dept_id': 2,
            'college_id': 1,
            'dept_name': 'Electronics & Communication',
            'hod_faculty_id': None,
            'code': 'ECE'
        },
        {
            'dept_id': 3,
            'college_id': 1,
            'dept_name': 'Mechanical Engineering',
            'hod_faculty_id': None,
            'code': 'ME'
        }
    ]

    _divisions = [
        {
            'division_id': 1,
            'dept_id': 1,
            'division_name': 'CSE-A',
            'semester_id': 3,
            'capacity': 60,
            'class_teacher': 2
        },
        {
            'division_id': 2,
            'dept_id': 1,
            'division_name': 'CSE-B',
            'semester_id': 3,
            'capacity': 58,
            'class_teacher': 3
        },
        {
            'division_id': 3,
            'dept_id': 1,
            'division_name': 'CSE-C',
            'semester_id': 3,
            'capacity': 55,
            'class_teacher': None
        },
        {
            'division_id': 4,
            'dept_id': 2,
            'division_name': 'ECE-A',
            'semester_id': 3,
            'capacity': 60,
            'class_teacher': None
        },
        {
            'division_id': 5,
            'dept_id': 2,
            'division_name': 'ECE-B',
            'semester_id': 3,
            'capacity': 58,
            'class_teacher': None
        },
        {
            'division_id': 6,
            'dept_id': 3,
            'division_name': 'ME-A',
            'semester_id': 3,
            'capacity': 60,
            'class_teacher': None
        },
        {
            'division_id': 7,
            'dept_id': 3,
            'division_name': 'ME-B',
            'semester_id': 3,
            'capacity': 58,
            'class_teacher': None
        }
    ]

    _semesters = [
        {'semester_id': 1, 'semester_no': 1, 'academic_year': '2024-2025'},
        {'semester_id': 2, 'semester_no': 2, 'academic_year': '2024-2025'},
        {'semester_id': 3, 'semester_no': 3, 'academic_year': '2024-2025'},
        {'semester_id': 4, 'semester_no': 4, 'academic_year': '2024-2025'}
    ]

    _users = {
        'superadmin': {
            'user_id': 1,
            'college_id': 1,
            'name': 'Super Admin',
            'email': 'admin@attendance.system',
            'mobile': '9999999999',
            'role_id': 1,
            'is_approved': True,
            'created_at': datetime(2020, 1, 1)
        },
        'college_admin': {
            'user_id': 2,
            'college_id': 1,
            'name': 'Ms. Neha Singh',
            'email': 'neha.singh@college.edu',
            'mobile': '9876543213',
            'role_id': 1,
            'is_approved': True,
            'created_at': datetime(2021, 1, 20)
        },
        'hod': {
            'user_id': 3,
            'college_id': 1,
            'name': 'Prof. Amit Patel',
            'email': 'amit.patel@college.edu',
            'mobile': '9876543212',
            'role_id': 2,
            'is_approved': True,
            'created_at': datetime(2020, 3, 5)
        },
        'faculty': {
            'user_id': 4,
            'college_id': 1,
            'name': 'Dr. Priya Sharma',
            'email': 'priya.sharma@college.edu',
            'mobile': '9876543211',
            'role_id': 3,
            'is_approved': True,
            'created_at': datetime(2022, 6, 10)
        },
        'student': {
            'user_id': 5,
            'college_id': 1,
            'name': 'Raj Kumar',
            'email': 'raj.kumar@college.edu',
            'mobile': '9876543210',
            'role_id': 4,
            'is_approved': True,
            'created_at': datetime(2023, 8, 15)
        },
        'parent': {
            'user_id': 6,
            'college_id': 1,
            'name': 'Shyam Kumar',
            'email': 'shyam.kumar@email.com',
            'mobile': '9876543214',
            'role_id': 5,
            'is_approved': True,
            'created_at': datetime(2023, 9, 1)
        },
        'faculty_backup': {
            'user_id': 7,
            'college_id': 1,
            'name': 'Mr. Rahul Agarwal',
            'email': 'rahul.agarwal@college.edu',
            'mobile': '9876543215',
            'role_id': 3,
            'is_approved': True,
            'created_at': datetime(2022, 7, 15)
        }
    }

    _faculty = [
        {
            'faculty_id': 1,
            'user_id': 3,
            'dept_id': 1,
            'short_name': 'AP',
            'full_name': 'Prof. Amit Patel',
            'designation': 'Head of Department'
        },
        {
            'faculty_id': 2,
            'user_id': 4,
            'dept_id': 1,
            'short_name': 'PS',
            'full_name': 'Dr. Priya Sharma',
            'designation': 'Senior Lecturer'
        },
        {
            'faculty_id': 3,
            'user_id': 7,
            'dept_id': 1,
            'short_name': 'RA',
            'full_name': 'Mr. Rahul Agarwal',
            'designation': 'Assistant Professor'
        }
    ]

    _students = [
        {
            'student_id': 1,
            'user_id': 5,
            'dept_id': 1,
            'division_id': 1,
            'enrollment_no': 'EN2023001',
            'roll_no': 101,
            'mentor_id': 2,
            'semester_id': 3
        },
        {
            'student_id': 2,
            'user_id': 5,
            'dept_id': 1,
            'division_id': 2,
            'enrollment_no': 'EN2023002',
            'roll_no': 102,
            'mentor_id': 3,
            'semester_id': 3
        },
        {
            'student_id': 3,
            'user_id': 5,
            'dept_id': 1,
            'division_id': 3,
            'enrollment_no': 'EN2023003',
            'roll_no': 103,
            'mentor_id': 2,
            'semester_id': 3
        }
    ]

    _parents = [
        {
            'user_id': 6,
            'student_id': 1
        }
    ]

    _subjects = [
        {
            'subject_id': 1,
            'dept_id': 1,
            'subject_name': 'Data Structures',
            'subject_code': 'CS301',
            'semester_id': 3,
            'credits': 4
        },
        {
            'subject_id': 2,
            'dept_id': 1,
            'subject_name': 'Database Management',
            'subject_code': 'CS302',
            'semester_id': 3,
            'credits': 3
        },
        {
            'subject_id': 3,
            'dept_id': 1,
            'subject_name': 'Operating Systems',
            'subject_code': 'CS303',
            'semester_id': 3,
            'credits': 4
        },
        {
            'subject_id': 4,
            'dept_id': 1,
            'subject_name': 'Software Engineering',
            'subject_code': 'CS304',
            'semester_id': 3,
            'credits': 3
        }
    ]

    _timetable_entries = [
        {
            'entry_id': 1,
            'dept_id': 1,
            'division_id': 1,
            'division_name': 'CSE-A',
            'day': 'Monday',
            'start_time': '09:00',
            'end_time': '10:00',
            'subject_id': 1,
            'subject_name': 'Data Structures',
            'subject_code': 'CS301',
            'faculty_id': 2,
            'faculty_name': 'Dr. Priya Sharma',
            'room_no': 'B-201',
            'mode': 'Lecture',
            'semester_id': 3
        },
        {
            'entry_id': 2,
            'dept_id': 1,
            'division_id': 1,
            'division_name': 'CSE-A',
            'day': 'Monday',
            'start_time': '10:15',
            'end_time': '11:15',
            'subject_id': 2,
            'subject_name': 'Database Management',
            'subject_code': 'CS302',
            'faculty_id': 3,
            'faculty_name': 'Mr. Rahul Agarwal',
            'room_no': 'B-203',
            'mode': 'Lecture',
            'semester_id': 3
        },
        {
            'entry_id': 3,
            'dept_id': 1,
            'division_id': 2,
            'division_name': 'CSE-B',
            'day': 'Monday',
            'start_time': '09:00',
            'end_time': '10:00',
            'subject_id': 3,
            'subject_name': 'Operating Systems',
            'subject_code': 'CS303',
            'faculty_id': 2,
            'faculty_name': 'Dr. Priya Sharma',
            'room_no': 'B-301',
            'mode': 'Lecture',
            'semester_id': 3
        },
        {
            'entry_id': 4,
            'dept_id': 1,
            'division_id': 2,
            'division_name': 'CSE-B',
            'day': 'Wednesday',
            'start_time': '11:30',
            'end_time': '12:30',
            'subject_id': 1,
            'subject_name': 'Data Structures',
            'subject_code': 'CS301',
            'faculty_id': 2,
            'faculty_name': 'Dr. Priya Sharma',
            'room_no': 'B-205',
            'mode': 'Practical',
            'semester_id': 3
        }
    ]

    _attendance_records = [
        {
            'record_id': 1,
            'dept_id': 1,
            'division_id': 1,
            'division_name': 'CSE-A',
            'subject_id': 1,
            'subject_name': 'Data Structures',
            'subject_code': 'CS301',
            'student_id': 1,
            'student_name': 'Raj Kumar',
            'total_lectures': 42,
            'attended_lectures': 38,
            'attendance_percentage': 90.48,
            'status': 'Good',
            'last_updated': datetime.now() - timedelta(days=1)
        },
        {
            'record_id': 2,
            'dept_id': 1,
            'division_id': 1,
            'division_name': 'CSE-A',
            'subject_id': 2,
            'subject_name': 'Database Management',
            'subject_code': 'CS302',
            'student_id': 1,
            'student_name': 'Raj Kumar',
            'total_lectures': 40,
            'attended_lectures': 34,
            'attendance_percentage': 85.0,
            'status': 'Average',
            'last_updated': datetime.now() - timedelta(days=2)
        },
        {
            'record_id': 3,
            'dept_id': 1,
            'division_id': 2,
            'division_name': 'CSE-B',
            'subject_id': 1,
            'subject_name': 'Data Structures',
            'subject_code': 'CS301',
            'student_id': 2,
            'student_name': 'Anita Singh',
            'total_lectures': 42,
            'attended_lectures': 36,
            'attendance_percentage': 85.71,
            'status': 'Average',
            'last_updated': datetime.now() - timedelta(days=3)
        },
        {
            'record_id': 4,
            'dept_id': 1,
            'division_id': 2,
            'division_name': 'CSE-B',
            'subject_id': 3,
            'subject_name': 'Operating Systems',
            'student_id': 2,
            'student_name': 'Anita Singh',
            'total_lectures': 38,
            'attended_lectures': 28,
            'attendance_percentage': 73.68,
            'status': 'Warning',
            'last_updated': datetime.now() - timedelta(days=4)
        }
    ]

    _lectures = [
        {
            'lecture_id': 1,
            'dept_id': 1,
            'division_id': 1,
            'division_name': 'CSE-A',
            'subject_id': 1,
            'subject_name': 'Data Structures',
            'subject_code': 'CS301',
            'faculty_id': 2,
            'start_time': '09:00 AM',
            'end_time': '10:00 AM',
            'room_no': 'B-201',
            'is_completed': False,
            'day': 'Monday'
        },
        {
            'lecture_id': 2,
            'dept_id': 1,
            'division_id': 1,
            'division_name': 'CSE-A',
            'subject_id': 2,
            'subject_name': 'Database Management',
            'subject_code': 'CS302',
            'faculty_id': 3,
            'start_time': '10:15 AM',
            'end_time': '11:15 AM',
            'room_no': 'B-203',
            'is_completed': False,
            'day': 'Monday'
        },
        {
            'lecture_id': 3,
            'dept_id': 1,
            'division_id': 2,
            'division_name': 'CSE-B',
            'subject_id': 3,
            'subject_name': 'Operating Systems',
            'subject_code': 'CS303',
            'faculty_id': 2,
            'start_time': '11:30 AM',
            'end_time': '12:30 PM',
            'room_no': 'B-205',
            'is_completed': True,
            'day': 'Wednesday'
        }
    ]

    _proxy_requests = [
        {
            'proxy_id': 1,
            'subject_name': 'Database Management',
            'division_name': 'CSE-A',
            'status': 'Pending',
            'original_faculty': 'Dr. Priya Sharma',
            'lecture_no': 12
        }
    ]

    _id_counters = {
        'timetable': 4
    }

    @staticmethod
    def _clone_list(items):
        return [dict(item) for item in items]

    @staticmethod
    def _clone_dict(item):
        return dict(item)

    @classmethod
    def _next_id(cls, counter_key):
        cls._id_counters[counter_key] += 1
        return cls._id_counters[counter_key]

    @staticmethod
    def get_college():
        """Get mock college data"""
        return MockDataService._clone_dict(MockDataService._college)

    @staticmethod
    def get_departments():
        """Get mock departments"""
        return MockDataService._clone_list(MockDataService._departments)

    @staticmethod
    def get_divisions():
        """Get mock divisions"""
        return MockDataService._clone_list(MockDataService._divisions)

    @staticmethod
    def get_semesters():
        """Get mock semesters"""
        return MockDataService._clone_list(MockDataService._semesters)

    @staticmethod
    def get_users():
        """Get mock users"""
        return {key: MockDataService._clone_dict(value) for key, value in MockDataService._users.items()}

    @staticmethod
    def get_faculty():
        """Get mock faculty members"""
        return MockDataService._clone_list(MockDataService._faculty)

    @staticmethod
    def get_students():
        """Get mock students"""
        return MockDataService._clone_list(MockDataService._students)

    @staticmethod
    def get_parents():
        """Get mock parents"""
        return MockDataService._clone_list(MockDataService._parents)

    @staticmethod
    def get_subjects():
        """Get mock subjects"""
        return MockDataService._clone_list(MockDataService._subjects)

    @staticmethod
    def get_timetable(dept_id=None, division_id=None, day=None):
        """Get mock timetable entries filtered by department, division, or day"""
        entries = MockDataService._timetable_entries
        if dept_id:
            entries = [e for e in entries if e['dept_id'] == dept_id]
        if division_id:
            entries = [e for e in entries if e['division_id'] == division_id]
        if day:
            entries = [e for e in entries if e['day'].lower() == day.lower()]
        return MockDataService._clone_list(entries)

    @staticmethod
    def save_timetable_entry(entry_data):
        """Create or update a timetable entry"""
        if entry_data.get('entry_id'):
            for idx, entry in enumerate(MockDataService._timetable_entries):
                if entry['entry_id'] == entry_data['entry_id']:
                    MockDataService._timetable_entries[idx] = dict(entry_data)
                    return MockDataService._clone_dict(entry_data)
        new_id = MockDataService._next_id('timetable')
        entry_data['entry_id'] = new_id
        MockDataService._timetable_entries.append(dict(entry_data))
        return MockDataService._clone_dict(entry_data)

    @staticmethod
    def delete_timetable_entry(entry_id):
        """Delete a timetable entry"""
        for idx, entry in enumerate(MockDataService._timetable_entries):
            if entry['entry_id'] == entry_id:
                MockDataService._timetable_entries.pop(idx)
                return True
        return False

    @staticmethod
    def get_lectures(dept_id=None, faculty_id=None, day=None):
        """Get lectures filtered by department, faculty, or day"""
        lectures = MockDataService._lectures
        if dept_id:
            lectures = [l for l in lectures if l['dept_id'] == dept_id]
        if faculty_id:
            lectures = [l for l in lectures if l['faculty_id'] == faculty_id]
        if day:
            lectures = [l for l in lectures if l['day'].lower() == day.lower()]
        return MockDataService._clone_list(lectures)

    @staticmethod
    def get_attendance_records(dept_id=None, division_id=None, subject_id=None):
        """Get attendance records filtered by dept/division/subject"""
        records = MockDataService._attendance_records
        if dept_id:
            records = [r for r in records if r['dept_id'] == dept_id]
        if division_id:
            records = [r for r in records if r['division_id'] == division_id]
        if subject_id:
            records = [r for r in records if r['subject_id'] == subject_id]
        return MockDataService._clone_list(records)

    @staticmethod
    def get_proxy_requests():
        """Get proxy lecture requests"""
        return MockDataService._clone_list(MockDataService._proxy_requests)

    @staticmethod
    def get_all_data():
        """Get all mock data at once"""
        return {
            'college': MockDataService.get_college(),
            'departments': MockDataService.get_departments(),
            'divisions': MockDataService.get_divisions(),
            'semesters': MockDataService.get_semesters(),
            'users': MockDataService.get_users(),
            'faculty': MockDataService.get_faculty(),
            'students': MockDataService.get_students(),
            'parents': MockDataService.get_parents(),
            'subjects': MockDataService.get_subjects(),
            'timetable': MockDataService.get_timetable(),
            'attendance_records': MockDataService.get_attendance_records()
        }
