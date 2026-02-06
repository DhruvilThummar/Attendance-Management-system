"""
Database Query Helper

This module provides helper functions for routes to query data.
Currently uses mock data, can be easily switched to real database queries.
"""

from collections import defaultdict

from services.mock_data import MockDataService


class DataHelper:
    """Helper class to get data - works with both mock and real database"""

    DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    @staticmethod
    def get_user(user_type='student'):
        """Get user by type"""
        users = MockDataService.get_users()
        return users.get(user_type)

    @staticmethod
    def get_hod_user():
        """Get the default HOD user"""
        return DataHelper.get_user('hod')

    @staticmethod
    def get_college():
        """Get college data"""
        return MockDataService.get_college()

    @staticmethod
    def get_departments():
        """Get all departments"""
        return MockDataService.get_departments()

    @staticmethod
    def get_department(dept_id):
        """Get specific department"""
        departments = MockDataService.get_departments()
        return next((d for d in departments if d['dept_id'] == dept_id), None)

    @staticmethod
    def get_department_by_hod(faculty_id):
        """Get department managed by the given HOD faculty"""
        departments = MockDataService.get_departments()
        return next((d for d in departments if d.get('hod_faculty_id') == faculty_id), None)

    @staticmethod
    def get_divisions(dept_id=None):
        """Get divisions, optionally filtered by department"""
        divisions = MockDataService.get_divisions()
        if dept_id:
            return [d for d in divisions if d['dept_id'] == dept_id]
        return divisions

    @staticmethod
    def get_division(division_id):
        """Get specific division"""
        divisions = MockDataService.get_divisions()
        return next((d for d in divisions if d['division_id'] == division_id), None)

    @staticmethod
    def get_faculty(dept_id=None):
        """Get faculty members, optionally filtered by department"""
        faculty = MockDataService.get_faculty()
        if dept_id:
            return [f for f in faculty if f['dept_id'] == dept_id]
        return faculty

    @staticmethod
    def get_faculty_member(faculty_id=None, user_id=None):
        """Get a specific faculty member by faculty or user id"""
        faculty = MockDataService.get_faculty()
        if faculty_id is not None:
            return next((f for f in faculty if f['faculty_id'] == faculty_id), None)
        if user_id is not None:
            return next((f for f in faculty if f['user_id'] == user_id), None)
        return None

    @staticmethod
    def get_students(division_id=None, dept_id=None):
        """Get students with optional filters"""
        students = MockDataService.get_students()

        if division_id:
            students = [s for s in students if s['division_id'] == division_id]
        if dept_id:
            students = [s for s in students if s['dept_id'] == dept_id]

        return students

    @staticmethod
    def get_student(student_id):
        """Get specific student"""
        students = MockDataService.get_students()
        return next((s for s in students if s['student_id'] == student_id), None)

    @staticmethod
    def get_subjects(dept_id=None, semester_id=None):
        """Get subjects with optional filters"""
        subjects = MockDataService.get_subjects()

        if dept_id:
            subjects = [s for s in subjects if s['dept_id'] == dept_id]
        if semester_id:
            subjects = [s for s in subjects if s['semester_id'] == semester_id]

        return subjects

    @staticmethod
    def get_subjects_grouped_by_semester(dept_id):
        """Group subjects by semester for the given department"""
        subjects = DataHelper.get_subjects(dept_id=dept_id)
        semesters = {s['semester_id']: s for s in DataHelper.get_semesters()}
        grouped = {}

        for subject in subjects:
            semester_id = subject['semester_id']
            semester_info = semesters.get(semester_id, {})
            if semester_id not in grouped:
                grouped[semester_id] = {
                    'semester_id': semester_id,
                    'semester_no': semester_info.get('semester_no'),
                    'academic_year': semester_info.get('academic_year'),
                    'subjects': []
                }
            grouped[semester_id]['subjects'].append(subject)

        return sorted(grouped.values(), key=lambda item: (item['semester_no'] or 0))

    @staticmethod
    def get_semesters():
        """Get all semesters"""
        return MockDataService.get_semesters()

    @staticmethod
    def get_lectures(dept_id=None, faculty_id=None, day=None):
        """Get lecture schedule"""
        return MockDataService.get_lectures(dept_id=dept_id, faculty_id=faculty_id, day=day)

    @staticmethod
    def get_proxy_requests():
        """Get proxy lecture requests"""
        return MockDataService.get_proxy_requests()

    @staticmethod
    def get_attendance_records(dept_id=None, division_id=None, subject_id=None):
        """Get attendance records"""
        return MockDataService.get_attendance_records(dept_id=dept_id, division_id=division_id, subject_id=subject_id)

    @staticmethod
    def get_division_attendance_summary(dept_id):
        """Build summary data for division level attendance"""
        records = DataHelper.get_attendance_records(dept_id=dept_id)
        summary = {}

        for record in records:
            division_id = record['division_id']
            division = summary.setdefault(
                division_id,
                {
                    'division_id': division_id,
                    'division_name': record['division_name'],
                    'records': 0,
                    'total_percentage': 0.0,
                    'low_attendance': 0,
                    'last_updated': record['last_updated'],
                    'subjects': {}
                }
            )

            division['records'] += 1
            division['total_percentage'] += record['attendance_percentage']
            if record['attendance_percentage'] < 75:
                division['low_attendance'] += 1
            if record['last_updated'] > division['last_updated']:
                division['last_updated'] = record['last_updated']

            subject_meta = division['subjects'].setdefault(
                record['subject_id'],
                {
                    'subject_id': record['subject_id'],
                    'subject_name': record['subject_name'],
                    'total_percentage': 0.0,
                    'count': 0
                }
            )
            subject_meta['total_percentage'] += record['attendance_percentage']
            subject_meta['count'] += 1

        for division in summary.values():
            division['student_count'] = len(DataHelper.get_students(division_id=division['division_id']))
            division['average_percentage'] = round(
                division['total_percentage'] / division['records'],
                2
            ) if division['records'] else 0.0

            subject_breakdown = []
            for subject in division['subjects'].values():
                subject_breakdown.append(
                    {
                        'subject_id': subject['subject_id'],
                        'subject_name': subject['subject_name'],
                        'average_percentage': round(
                            subject['total_percentage'] / subject['count'],
                            2
                        ) if subject['count'] else 0.0
                    }
                )
            subject_breakdown.sort(key=lambda item: item['subject_name'])
            division['subject_breakdown'] = subject_breakdown
            division.pop('subjects', None)
            division.pop('total_percentage', None)

        return sorted(summary.values(), key=lambda item: item['division_name'])

    @staticmethod
    def get_department_stats(dept_id):
        """Collect aggregate statistics for a department"""
        faculty = DataHelper.get_faculty(dept_id=dept_id)
        students = DataHelper.get_students(dept_id=dept_id)
        subjects = DataHelper.get_subjects(dept_id=dept_id)
        divisions = DataHelper.get_divisions(dept_id=dept_id)
        attendance_records = DataHelper.get_attendance_records(dept_id=dept_id)

        avg_attendance = round(
            sum(record['attendance_percentage'] for record in attendance_records) / len(attendance_records),
            2
        ) if attendance_records else 0.0

        return {
            'total_faculty': len(faculty),
            'total_students': len(students),
            'total_subjects': len(subjects),
            'total_divisions': len(divisions),
            'avg_attendance': avg_attendance
        }

    @staticmethod
    def get_timetable(dept_id=None, division_id=None, day=None):
        """Get timetable entries"""
        entries = MockDataService.get_timetable(dept_id=dept_id, division_id=division_id, day=day)
        day_priority = {day_name: idx for idx, day_name in enumerate(DataHelper.DAY_ORDER)}
        return sorted(
            entries,
            key=lambda entry: (
                day_priority.get(entry['day'], len(DataHelper.DAY_ORDER)),
                entry['start_time'],
                entry['division_id']
            )
        )

    @staticmethod
    def get_timetable_overview(dept_id):
        """Group timetable entries by division with day sorting"""
        entries = DataHelper.get_timetable(dept_id=dept_id)
        day_priority = {day_name: idx for idx, day_name in enumerate(DataHelper.DAY_ORDER)}
        overview = defaultdict(lambda: {'division_id': None, 'division_name': None, 'entries': []})

        for entry in entries:
            bucket = overview[entry['division_id']]
            bucket['division_id'] = entry['division_id']
            bucket['division_name'] = entry['division_name']
            bucket['entries'].append(entry)

        for bucket in overview.values():
            bucket['entries'].sort(
                key=lambda entry: (
                    day_priority.get(entry['day'], len(DataHelper.DAY_ORDER)),
                    entry['start_time']
                )
            )

        return sorted(overview.values(), key=lambda item: item['division_name'] or '')

    @staticmethod
    def get_timetable_days(dept_id):
        """Return ordered list of days present in timetable"""
        entries = DataHelper.get_timetable(dept_id=dept_id)
        seen = []
        for day_name in DataHelper.DAY_ORDER:
            if any(entry['day'] == day_name for entry in entries):
                seen.append(day_name)
        return seen

    @staticmethod
    def save_timetable_entry(entry_data):
        """Normalize and persist timetable entry"""
        division = DataHelper.get_division(entry_data['division_id'])
        if not division:
            raise ValueError('Invalid division')

        subject = next((s for s in DataHelper.get_subjects(dept_id=division['dept_id']) if s['subject_id'] == entry_data['subject_id']), None)
        if not subject:
            raise ValueError('Invalid subject')

        faculty = DataHelper.get_faculty_member(faculty_id=entry_data['faculty_id'])
        if not faculty:
            raise ValueError('Invalid faculty')

        normalized = {
            'entry_id': entry_data.get('entry_id'),
            'dept_id': division['dept_id'],
            'division_id': division['division_id'],
            'division_name': division['division_name'],
            'day': entry_data['day'],
            'start_time': entry_data['start_time'],
            'end_time': entry_data['end_time'],
            'subject_id': subject['subject_id'],
            'subject_name': subject['subject_name'],
            'subject_code': subject['subject_code'],
            'faculty_id': faculty['faculty_id'],
            'faculty_name': faculty.get('full_name') or faculty.get('short_name'),
            'room_no': entry_data.get('room_no', ''),
            'mode': entry_data.get('mode', 'Lecture'),
            'semester_id': subject.get('semester_id')
        }

        return MockDataService.save_timetable_entry(normalized)

    @staticmethod
    def delete_timetable_entry(entry_id):
        """Delete a timetable entry"""
        return MockDataService.delete_timetable_entry(entry_id)

    @staticmethod
    def get_parent_children(user_id):
        """Get all children (students) for a parent with full details"""
        parents = MockDataService.get_parents()
        parent_records = [p for p in parents if p.get('user_id') == user_id]
        
        # Get full student details for each child
        children_details = []
        for record in parent_records:
            student_id = record.get('student_id')
            student = DataHelper.get_student(student_id)
            if student:
                children_details.append({
                    'student_id': student_id,
                    **student  # Include all student details
                })
        
        return children_details

    @staticmethod
    def get_child_attendance(student_id, subject_id=None):
        """Get overall attendance records for a child"""
        records = DataHelper.get_attendance_records()
        child_records = [r for r in records if r['student_id'] == student_id]
        
        if subject_id:
            child_records = [r for r in child_records if r['subject_id'] == subject_id]
        
        return child_records

    @staticmethod
    def get_child_attendance_by_period(student_id, period='weekly', subject_id=None):
        """Get attendance filtered by time period (weekly, monthly)"""
        records = DataHelper.get_child_attendance(student_id, subject_id)
        
        if period == 'weekly':
            # Group by week (last 7 days, current week, etc.)
            from datetime import datetime, timedelta
            today = datetime.now()
            week_ago = today - timedelta(days=7)
            
            weekly_data = []
            for week_num in range(4):  # Last 4 weeks
                week_start = today - timedelta(days=7 * (4 - week_num))
                week_filtered = [r for r in records if r.get('last_updated', today) >= week_start]
                
                if week_filtered:
                    avg_pct = sum(r['attendance_percentage'] for r in week_filtered) / len(week_filtered)
                    weekly_data.append({
                        'week': f'Week {4 - week_num}',
                        'start_date': week_start.strftime('%Y-%m-%d'),
                        'average_percentage': round(avg_pct, 2),
                        'records_count': len(week_filtered),
                        'records': week_filtered
                    })
            return weekly_data
        
        elif period == 'monthly':
            # Group by month (current month, last month, etc.)
            from datetime import datetime, timedelta
            today = datetime.now()
            
            monthly_data = []
            for month_num in range(3):  # Last 3 months
                month_start = today - timedelta(days=30 * month_num)
                month_start = month_start.replace(day=1)
                
                month_filtered = [r for r in records if r.get('last_updated', today) >= month_start]
                
                if month_filtered:
                    avg_pct = sum(r['attendance_percentage'] for r in month_filtered) / len(month_filtered)
                    monthly_data.append({
                        'month': month_start.strftime('%B %Y'),
                        'average_percentage': round(avg_pct, 2),
                        'records_count': len(month_filtered),
                        'records': month_filtered
                    })
            return monthly_data
        
        return records

    @staticmethod
    def get_child_subject_wise_attendance(student_id):
        """Get subject-wise attendance breakdown for a child"""
        records = DataHelper.get_child_attendance(student_id)
        subject_summary = {}
        
        for record in records:
            subject_id = record['subject_id']
            subject_name = record['subject_name']
            subject_code = record.get('subject_code', '')
            
            if subject_id not in subject_summary:
                subject_summary[subject_id] = {
                    'subject_id': subject_id,
                    'subject_name': subject_name,
                    'subject_code': subject_code,
                    'total_lectures': 0,
                    'attended_lectures': 0,
                    'records': []
                }
            
            subject_summary[subject_id]['total_lectures'] += record.get('total_lectures', 0)
            subject_summary[subject_id]['attended_lectures'] += record.get('attended_lectures', 0)
            subject_summary[subject_id]['records'].append(record)
        
        # Calculate percentage for each subject
        for subject in subject_summary.values():
            if subject['total_lectures'] > 0:
                subject['attendance_percentage'] = round(
                    (subject['attended_lectures'] / subject['total_lectures']) * 100,
                    2
                )
            else:
                subject['attendance_percentage'] = 0.0
            
            subject['status'] = 'Good' if subject['attendance_percentage'] >= 85 else \
                               'Average' if subject['attendance_percentage'] >= 75 else 'Warning'
        
        return sorted(subject_summary.values(), key=lambda x: x['subject_name'])

    @staticmethod
    def get_child_alerts(student_id):
        """Get attendance alerts for a child (low attendance warnings)"""
        records = DataHelper.get_child_attendance(student_id)
        alerts = []
        
        for record in records:
            if record['attendance_percentage'] < 75:
                alerts.append({
                    'subject_name': record['subject_name'],
                    'subject_code': record.get('subject_code', ''),
                    'attendance_percentage': record['attendance_percentage'],
                    'message': f"Low attendance in {record['subject_name']}: {record['attendance_percentage']}%",
                    'severity': 'critical' if record['attendance_percentage'] < 75 else 'warning'
                })
        
        return alerts

    # ========== SUPERADMIN METHODS ==========

    @staticmethod
    def get_all_colleges():
        """Get all colleges in the system"""
        # For now returns single college, will be multiple in database
        college = DataHelper.get_college()
        return [college] if college else []

    @staticmethod
    def get_total_students_count():
        """Get total count of all students"""
        students = MockDataService.get_students()
        return len(students)

    @staticmethod
    def get_total_faculty_count():
        """Get total count of all faculty members"""
        faculty = MockDataService.get_faculty_members()
        return len(faculty)

    @staticmethod
    def get_total_departments_count():
        """Get total count of all departments"""
        departments = MockDataService.get_departments()
        return len(departments)

    @staticmethod
    def get_recent_users(limit=5):
        """Get recently registered users"""
        users_dict = MockDataService.get_users()
        users_list = list(users_dict.values())
        # Sort by created_at if available
        sorted_users = sorted(users_list, key=lambda x: x.get('created_at', datetime.min), reverse=True)
        return sorted_users[:limit]

    @staticmethod
    def get_college_statistics(college_id):
        """Get statistics for a specific college"""
        students = MockDataService.get_students()
        faculty = MockDataService.get_faculty_members()
        departments = MockDataService.get_departments()
        divisions = MockDataService.get_divisions()
        
        # Filter by college_id (all mock data is college_id=1)
        college_students = [s for s in students if s.get('college_id', 1) == college_id]
        college_faculty = [f for f in faculty if f.get('college_id', 1) == college_id]
        college_depts = [d for d in departments if d.get('college_id', 1) == college_id]
        college_divisions = [div for div in divisions if div.get('college_id', 1) == college_id]
        
        # Calculate average attendance
        attendance_records = DataHelper.get_attendance_records()
        if attendance_records:
            avg_attendance = sum(r['attendance_percentage'] for r in attendance_records) / len(attendance_records)
        else:
            avg_attendance = 0
        
        return {
            'total_students': len(college_students),
            'total_faculty': len(college_faculty),
            'total_departments': len(college_depts),
            'total_divisions': len(college_divisions),
            'average_attendance': round(avg_attendance, 2)
        }

    @staticmethod
    def get_all_users_list():
        """Get all users as a list"""
        users_dict = MockDataService.get_users()
        return list(users_dict.values())

    @staticmethod
    def get_system_attendance_overview():
        """Get system-wide attendance overview"""
        records = DataHelper.get_attendance_records()
        
        if not records:
            return {
                'average_attendance': 0,
                'total_lectures': 0,
                'good_attendance_count': 0,
                'poor_attendance_count': 0
            }
        
        avg_attendance = sum(r['attendance_percentage'] for r in records) / len(records)
        total_lectures = sum(r.get('total_lectures', 0) for r in records)
        good_count = sum(1 for r in records if r['attendance_percentage'] >= 85)
        poor_count = sum(1 for r in records if r['attendance_percentage'] < 75)
        
        return {
            'average_attendance': round(avg_attendance, 2),
            'total_lectures': total_lectures,
            'good_attendance_count': good_count,
            'poor_attendance_count': poor_count,
            'total_records': len(records)
        }

    @staticmethod
    def get_department_performance():
        """Get performance metrics by department"""
        departments = DataHelper.get_departments()
        attendance_records = DataHelper.get_attendance_records()
        
        dept_performance = []
        for dept in departments:
            dept_records = [r for r in attendance_records if r['dept_id'] == dept['dept_id']]
            
            if dept_records:
                avg_attendance = sum(r['attendance_percentage'] for r in dept_records) / len(dept_records)
            else:
                avg_attendance = 0
            
            dept_students = [s for s in DataHelper.get_students() if s.get('dept_id') == dept['dept_id']]
            dept_faculty = [f for f in DataHelper.get_faculty_members() if f.get('dept_id') == dept['dept_id']]
            
            dept_performance.append({
                'dept_name': dept['dept_name'],
                'dept_code': dept.get('dept_code', ''),
                'average_attendance': round(avg_attendance, 2),
                'student_count': len(dept_students),
                'faculty_count': len(dept_faculty),
                'records_count': len(dept_records)
            })
        
        return sorted(dept_performance, key=lambda x: x['average_attendance'], reverse=True)


# Transition helper comments for database migration
MIGRATION_NOTES = """
To migrate from mock data to real database:

1. In routes, replace:
   from services.mock_data import MockDataService
   mock_data = MockDataService.get_data()
   
   With:
   from models import User, Student, Faculty, etc.
   user = User.query.get(user_id)

2. Replace DataHelper calls:
   department = DataHelper.get_department(1)
   
   With:
   from models import Department
   department = Department.query.get(1)

3. Update any mock data filtering to use SQLAlchemy queries:
   students = DataHelper.get_students(div_id=1)
   
   With:
   students = Student.query.filter_by(division_id=1).all()

4. Test each route after migration to ensure data is correctly retrieved.
"""
