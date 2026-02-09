"""
Database Query Helper

This module provides helper functions for routes to query data.
"""

import base64
import io
from collections import defaultdict
from datetime import datetime
from functools import lru_cache

import matplotlib
import numpy as np
from sqlalchemy import case, func
from flask import session

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from models import (
    AcademicCalendar,
    Attendance,
    AttendanceStatus,
    College,
    Department,
    Division,
    Faculty,
    Lecture,
    Parent,
    ProxyLecture,
    Role,
    Semester,
    Student,
    Subject,
    Timetable,
    User,
)
from models.user import db


class DataHelper:
    """Helper class to get data from the database"""

    DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    DAY_MAP = {
        'MON': 'Monday',
        'TUE': 'Tuesday',
        'WED': 'Wednesday',
        'THU': 'Thursday',
        'FRI': 'Friday',
        'SAT': 'Saturday'
    }
    DAY_REVERSE_MAP = {value: key for key, value in DAY_MAP.items()}
    ROLE_MAP = {
        'superadmin': 'ADMIN',
        'college_admin': 'ADMIN',
        'hod': 'HOD',
        'faculty': 'FACULTY',
        'student': 'STUDENT',
        'parent': 'PARENT'
    }

    @staticmethod
    def _np_mean(values):
        if not values:
            return 0.0
        clean_values = [DataHelper._to_float(value) for value in values]
        return float(np.mean(np.array(clean_values, dtype=float)))

    @staticmethod
    def _to_float(value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _plot_to_base64(fig):
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=140)
        plt.close(fig)
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode('ascii')

    @staticmethod
    @lru_cache(maxsize=64)
    def _render_bar_chart_cached(labels, values, title, y_label, color):
        fig, ax = plt.subplots(figsize=(6.4, 4.0))
        x = np.arange(len(labels))
        ax.bar(x, values, color=color)
        ax.set_title(title)
        ax.set_ylabel(y_label)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=25, ha='right')
        ax.set_ylim(0, 100)
        fig.tight_layout()
        return DataHelper._plot_to_base64(fig)

    @staticmethod
    @lru_cache(maxsize=64)
    def _render_line_chart_cached(labels, values, title, y_label, color):
        fig, ax = plt.subplots(figsize=(6.4, 4.0))
        x = np.arange(len(labels))
        ax.plot(x, values, color=color, marker='o')
        ax.set_title(title)
        ax.set_ylabel(y_label)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=25, ha='right')
        ax.set_ylim(0, 100)
        fig.tight_layout()
        return DataHelper._plot_to_base64(fig)

    @staticmethod
    @lru_cache(maxsize=64)
    def _render_donut_chart_cached(labels, values, title, colors):
        fig, ax = plt.subplots(figsize=(5.5, 4.0))
        safe_values = np.array(values, dtype=float)
        if np.sum(safe_values) <= 0:
            safe_values = np.array([1.0])
            labels = ("No data",)
            colors = ("#cbd5f5",)
        wedges, _ = ax.pie(
            safe_values,
            labels=labels,
            colors=colors,
            startangle=90,
            wedgeprops={'width': 0.45, 'edgecolor': 'white'}
        )
        ax.set_title(title)
        ax.axis('equal')
        fig.tight_layout()
        return DataHelper._plot_to_base64(fig)

    @staticmethod
    def _render_bar_chart(labels, values, title, y_label, color):
        return DataHelper._render_bar_chart_cached(tuple(labels), tuple(values), title, y_label, color)

    @staticmethod
    def _render_line_chart(labels, values, title, y_label, color):
        return DataHelper._render_line_chart_cached(tuple(labels), tuple(values), title, y_label, color)

    @staticmethod
    def _render_donut_chart(labels, values, title, colors):
        return DataHelper._render_donut_chart_cached(tuple(labels), tuple(values), title, tuple(colors))

    @staticmethod
    def _safe_attr(obj, attr_name, default=''):
        value = getattr(obj, attr_name, default)
        return value if value is not None else default

    @staticmethod
    def _dept_code(dept_name):
        if not dept_name:
            return ''
        cleaned = dept_name.replace('&', ' ').replace('-', ' ')
        tokens = [token for token in cleaned.split() if token.strip()]
        return ''.join(token[0] for token in tokens).upper()

    @staticmethod
    def _format_time(value):
        if not value:
            return ''
        if hasattr(value, 'strftime'):
            return value.strftime('%H:%M')
        return str(value)

    @staticmethod
    def _user_dict(user):
        if not user:
            return None
        return {
            'user_id': user.user_id,
            'college_id': user.college_id,
            'name': user.name,
            'email': user.email,
            'mobile': user.mobile,
            'role_id': user.role_id,
            'role_name': user.role.role_name if user.role else None,
            'is_approved': user.is_approved,
            'created_at': user.created_at
        }

    @staticmethod
    def _college_dict(college):
        if not college:
            return None
        return {
            'college_id': college.college_id,
            'college_name': college.college_name,
            'created_at': college.created_at,
            'address': DataHelper._safe_attr(college, 'address', ''),
            'email': DataHelper._safe_attr(college, 'email', ''),
            'phone': DataHelper._safe_attr(college, 'phone', ''),
            'website': DataHelper._safe_attr(college, 'website', '')
        }

    @staticmethod
    def _department_dict(dept):
        if not dept:
            return None
        hod_name = dept.hod_faculty.short_name if dept.hod_faculty and dept.hod_faculty.short_name else (
            dept.hod_faculty.user.name if dept.hod_faculty and dept.hod_faculty.user else 'Not Assigned')
        
        from models.student import Student
        student_count = Student.query.filter_by(dept_id=dept.dept_id).count()
        
        return {
            'dept_id': dept.dept_id,
            'college_id': dept.college_id,
            'dept_name': dept.dept_name,
            'dept_code': DataHelper._dept_code(dept.dept_name),
            'hod_faculty_id': dept.hod_faculty_id,
            'hod_name': hod_name,
            'student_count': student_count
        }

    @staticmethod
    def _division_dict(division):
        if not division:
            return None
        class_teacher_name = None
        if division.class_teacher:
            class_teacher_name = division.class_teacher.short_name or (
                division.class_teacher.user.name if division.class_teacher.user else None)
        
        from models.student import Student
        student_count = Student.query.filter_by(division_id=division.division_id).count()
        
        return {
            'division_id': division.division_id,
            'div_id': division.division_id,  # Alias for template compatibility
            'dept_id': division.dept_id,
            'division_name': division.division_name,
            'division_code': division.division_name,  # Use division name as code if no separate field
            'semester_id': DataHelper._safe_attr(division, 'semester_id', None),
            'capacity': DataHelper._safe_attr(division, 'capacity', 60),
            'student_count': student_count,
            'class_teacher_id': DataHelper._safe_attr(division, 'class_teacher_id', None),
            'class_teacher_name': class_teacher_name,
            'class_teacher': class_teacher_name  # Alias for template compatibility
        }

    @staticmethod
    def _faculty_dict(faculty):
        if not faculty:
            return None
        user = faculty.user
        
        # Check if this faculty is a HOD
        from models.department import Department
        is_hod = Department.query.filter_by(hod_faculty_id=faculty.faculty_id).first() is not None
        
        # Get subjects taught by this faculty
        from models.timetable import Timetable
        subject_ids = db.session.query(Timetable.subject_id).filter_by(faculty_id=faculty.faculty_id).distinct().all()
        subjects = []
        if subject_ids:
            from models.subject import Subject
            subjects_objs = Subject.query.filter(Subject.subject_id.in_([s[0] for s in subject_ids])).all()
            subjects = [s.subject_name for s in subjects_objs]
        
        return {
            'faculty_id': faculty.faculty_id,
            'user_id': faculty.user_id,
            'dept_id': faculty.dept_id,
            'college_id': faculty.department.college_id if faculty.department else None,
            'short_name': faculty.short_name,
            'full_name': user.name if user else '',
            'designation': DataHelper._safe_attr(faculty, 'designation', 'Faculty'),
            'name': user.name if user else '',
            'email': user.email if user else '',
            'mobile': user.mobile if user else '',
            'phone': user.mobile if user else '',
            'dept_name': faculty.department.dept_name if faculty.department else '',
            'is_hod': is_hod,
            'specialization': DataHelper._safe_attr(faculty, 'designation', None),
            'subjects': subjects,
            'appointed_date': None
        }

    @staticmethod
    def _student_dict(student):
        if not student:
            return None
        user = student.user
        semester_no = student.semester.semester_no if student.semester else None
        
        # Extract division short name (last character or full name if no pattern)
        division_name = student.division.division_name if student.division else ''
        division_short = division_name[-1] if division_name else ''  # Get last char as short name (A, B, C, etc.)
        
        return {
            'student_id': student.student_id,
            'user_id': student.user_id,
            'dept_id': student.dept_id,
            'college_id': student.department.college_id if student.department else None,
            'division_id': student.division_id,
            'div_id': student.division_id,  # Alias for compatibility
            'enrollment_no': student.enrollment_no,
            'roll_no': student.roll_no,
            'roll_number': student.roll_no,  # Alias for template compatibility
            'mentor_id': student.mentor_id,
            'semester_id': student.semester_id,
            'name': user.name if user else '',
            'email': user.email if user else '',
            'mobile': user.mobile if user else '',
            'phone': user.mobile if user else '',  # Alias for compatibility
            'dept_name': student.department.dept_name if student.department else '',
            'division_name': student.division.division_name if student.division else '',
            'division_short': division_short,
            'semester': semester_no
        }

    @staticmethod
    def _subject_dict(subject):
        if not subject:
            return None
        return {
            'subject_id': subject.subject_id,
            'dept_id': subject.dept_id,
            'subject_name': subject.subject_name,
            'subject_code': subject.subject_code,
            'semester_id': subject.semester_id,
            'credits': DataHelper._safe_attr(subject, 'credits', None)
        }

    @staticmethod
    def get_user(user_type='student'):
        """Get user by type"""
        role_name = DataHelper.ROLE_MAP.get(user_type, 'STUDENT')
        user = None
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user and user.role and user.role.role_name != role_name:
                user = None

        if not user:
            user = User.query.join(Role).filter(Role.role_name == role_name).order_by(User.user_id.asc()).first()
        return DataHelper._user_dict(user)

    @staticmethod
    def get_hod_user():
        """Get the default HOD user"""
        return DataHelper.get_user('hod')

    @staticmethod
    def get_college():
        """Get college data"""
        college = College.query.order_by(College.college_id.asc()).first()
        return DataHelper._college_dict(college)

    @staticmethod
    def get_departments():
        """Get all departments"""
        departments = Department.query.order_by(Department.dept_name.asc()).all()
        return [DataHelper._department_dict(dept) for dept in departments]

    @staticmethod
    def get_department(dept_id):
        """Get specific department"""
        dept = Department.query.get(dept_id)
        return DataHelper._department_dict(dept)

    @staticmethod
    def get_department_by_hod(faculty_id):
        """Get department managed by the given HOD faculty"""
        dept = Department.query.filter_by(hod_faculty_id=faculty_id).first()
        return DataHelper._department_dict(dept)

    @staticmethod
    def get_divisions(dept_id=None):
        """Get divisions, optionally filtered by department"""
        query = Division.query
        if dept_id:
            query = query.filter_by(dept_id=dept_id)
        divisions = query.order_by(Division.division_name.asc()).all()
        return [DataHelper._division_dict(division) for division in divisions]

    @staticmethod
    def get_division(division_id):
        """Get specific division"""
        division = Division.query.get(division_id)
        return DataHelper._division_dict(division)

    @staticmethod
    def get_faculty(dept_id=None):
        """Get faculty members, optionally filtered by department"""
        query = Faculty.query
        if dept_id:
            query = query.filter_by(dept_id=dept_id)
        faculty_members = query.order_by(Faculty.faculty_id.asc()).all()
        return [DataHelper._faculty_dict(member) for member in faculty_members]

    @staticmethod
    def get_faculty_members():
        """Get all faculty members"""
        return DataHelper.get_faculty()

    @staticmethod
    def get_faculty_member(faculty_id=None, user_id=None):
        """Get a specific faculty member by faculty or user id"""
        if faculty_id is not None:
            member = Faculty.query.get(faculty_id)
            return DataHelper._faculty_dict(member)
        if user_id is not None:
            member = Faculty.query.filter_by(user_id=user_id).first()
            return DataHelper._faculty_dict(member)
        return None

    @staticmethod
    def get_students(division_id=None, dept_id=None):
        """Get students with optional filters"""
        query = Student.query
        if division_id:
            query = query.filter_by(division_id=division_id)
        if dept_id:
            query = query.filter_by(dept_id=dept_id)
        students = query.order_by(Student.student_id.asc()).all()
        return [DataHelper._student_dict(student) for student in students]

    @staticmethod
    def get_student(student_id):
        """Get specific student"""
        student = Student.query.get(student_id)
        return DataHelper._student_dict(student)

    @staticmethod
    def get_subjects(dept_id=None, semester_id=None):
        """Get subjects with optional filters"""
        query = Subject.query
        if dept_id:
            query = query.filter_by(dept_id=dept_id)
        if semester_id:
            query = query.filter_by(semester_id=semester_id)
        subjects = query.order_by(Subject.subject_name.asc()).all()
        return [DataHelper._subject_dict(subject) for subject in subjects]

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
        semesters = Semester.query.order_by(Semester.semester_no.asc()).all()
        return [
            {
                'semester_id': semester.semester_id,
                'semester_no': semester.semester_no,
                'academic_year': semester.academic_year
            }
            for semester in semesters
        ]

    @staticmethod
    def get_lectures(dept_id=None, faculty_id=None, day=None):
        """Get lecture schedule"""
        query = Timetable.query
        if dept_id:
            query = query.join(Subject).filter(Subject.dept_id == dept_id)
        if faculty_id:
            query = query.filter(Timetable.faculty_id == faculty_id)
        if day:
            day_code = DataHelper.DAY_REVERSE_MAP.get(day, day)
            query = query.filter(Timetable.day_of_week == day_code)

        entries = []
        for entry in query.all():
            entries.append({
                'lecture_id': entry.timetable_id,
                'dept_id': entry.subject.dept_id if entry.subject else None,
                'division_id': entry.division_id,
                'division_name': entry.division.division_name if entry.division else '',
                'subject_id': entry.subject_id,
                'subject_name': entry.subject.subject_name if entry.subject else '',
                'subject_code': entry.subject.subject_code if entry.subject else '',
                'faculty_id': entry.faculty_id,
                'start_time': DataHelper._format_time(entry.start_time),
                'end_time': DataHelper._format_time(entry.end_time),
                'room_no': entry.room_no,
                'is_completed': False,
                'day': DataHelper.DAY_MAP.get(entry.day_of_week, entry.day_of_week)
            })
        return entries

    @staticmethod
    def get_proxy_requests():
        """Get proxy lecture requests"""
        proxies = ProxyLecture.query.order_by(ProxyLecture.assigned_at.desc()).all()
        requests = []
        for proxy in proxies:
            requests.append({
                'proxy_id': proxy.proxy_id,
                'subject_name': proxy.subject.subject_name if proxy.subject else '',
                'division_name': proxy.lecture.timetable.division.division_name
                if proxy.lecture and proxy.lecture.timetable and proxy.lecture.timetable.division else '',
                'status': proxy.status.status_name if proxy.status else 'PENDING',
                'original_faculty': proxy.original_faculty.short_name if proxy.original_faculty and proxy.original_faculty.short_name else (
                    proxy.original_faculty.user.name if proxy.original_faculty and proxy.original_faculty.user else ''),
                'faculty_id': proxy.substitute_faculty_id,
                'lecture_no': proxy.lecture_no
            })
        return requests

    @staticmethod
    def get_attendance_records(dept_id=None, division_id=None, subject_id=None, college_id=None):
        """Get attendance records with college filtering"""
        total_case = func.count(Attendance.attendance_id)
        present_case = func.sum(case((Attendance.status_id == 1, 1), else_=0))
        last_updated = func.max(Attendance.marked_at)

        query = db.session.query(
            Student.student_id,
            User.name.label('student_name'),
            Student.dept_id,
            Department.dept_name.label('dept_name'),
            Department.college_id,
            Student.division_id,
            Division.division_name,
            Subject.subject_id,
            Subject.subject_name,
            Subject.subject_code,
            Lecture.lecture_id,
            Lecture.lecture_date,
            total_case.label('total_lectures'),
            present_case.label('attended_lectures'),
            last_updated.label('last_updated')
        ).join(Student, Attendance.student_id == Student.student_id) \
            .join(User, Student.user_id == User.user_id) \
            .join(Lecture, Attendance.lecture_id == Lecture.lecture_id) \
            .join(Timetable, Lecture.timetable_id == Timetable.timetable_id) \
            .join(Subject, Timetable.subject_id == Subject.subject_id) \
            .join(Division, Student.division_id == Division.division_id) \
            .join(Department, Student.dept_id == Department.dept_id) \
            .group_by(
                Student.student_id,
                User.name,
                Student.dept_id,
                Department.dept_name,
                Department.college_id,
                Student.division_id,
                Division.division_name,
                Subject.subject_id,
                Subject.subject_name,
                Subject.subject_code,
                Lecture.lecture_id,
                Lecture.lecture_date
            )

        if college_id:
            query = query.filter(Department.college_id == college_id)
        if dept_id:
            query = query.filter(Student.dept_id == dept_id)
        if division_id:
            query = query.filter(Student.division_id == division_id)
        if subject_id:
            query = query.filter(Subject.subject_id == subject_id)

        records = []
        for idx, row in enumerate(query.all(), start=1):
            total_lectures = row.total_lectures or 0
            attended_lectures = row.attended_lectures or 0
            percentage = round((attended_lectures / total_lectures) * 100, 2) if total_lectures else 0.0
            status = 'Good' if percentage >= 85 else 'Average' if percentage >= 75 else 'Warning'

            records.append({
                'record_id': idx,
                'college_id': row.college_id,
                'dept_id': row.dept_id,
                'division_id': row.division_id,
                'division_name': row.division_name,
                'subject_id': row.subject_id,
                'subject_name': row.subject_name,
                'subject_code': row.subject_code,
                'lecture_id': row.lecture_id,
                'lecture_date': row.lecture_date,
                'student_id': row.student_id,
                'student_name': row.student_name,
                'total_lectures': total_lectures,
                'attended_lectures': attended_lectures,
                'attendance_percentage': percentage,
                'status': status,
                'last_updated': row.last_updated,
                'date': row.lecture_date  # For compatibility with existing code
            })
        return records

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
            percentage = DataHelper._to_float(record['attendance_percentage'])
            division['total_percentage'] += percentage
            if percentage < 75:
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
            subject_meta['total_percentage'] += percentage
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
            DataHelper._np_mean([record['attendance_percentage'] for record in attendance_records]),
            2
        )

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
        query = Timetable.query
        if dept_id:
            query = query.join(Subject).filter(Subject.dept_id == dept_id)
        if division_id:
            query = query.filter(Timetable.division_id == division_id)
        if day:
            day_code = DataHelper.DAY_REVERSE_MAP.get(day, day)
            query = query.filter(Timetable.day_of_week == day_code)

        entries = []
        for entry in query.all():
            entries.append({
                'entry_id': entry.timetable_id,
                'dept_id': entry.subject.dept_id if entry.subject else None,
                'division_id': entry.division_id,
                'division_name': entry.division.division_name if entry.division else '',
                'day': DataHelper.DAY_MAP.get(entry.day_of_week, entry.day_of_week),
                'start_time': DataHelper._format_time(entry.start_time),
                'end_time': DataHelper._format_time(entry.end_time),
                'subject_id': entry.subject_id,
                'subject_name': entry.subject.subject_name if entry.subject else '',
                'subject_code': entry.subject.subject_code if entry.subject else '',
                'faculty_id': entry.faculty_id,
                'faculty_name': entry.faculty.short_name if entry.faculty and entry.faculty.short_name else (
                    entry.faculty.user.name if entry.faculty and entry.faculty.user else ''),
                'room_no': entry.room_no or '',
                'mode': 'Lecture',
                'semester_id': entry.subject.semester_id if entry.subject else None
            })

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

        day_code = DataHelper.DAY_REVERSE_MAP.get(entry_data['day'], entry_data['day'])
        start_time = datetime.strptime(entry_data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(entry_data['end_time'], '%H:%M').time()

        if entry_data.get('entry_id'):
            timetable_entry = Timetable.query.get(entry_data['entry_id'])
            if not timetable_entry:
                raise ValueError('Invalid timetable entry')
        else:
            timetable_entry = Timetable()

        timetable_entry.subject_id = subject['subject_id']
        timetable_entry.faculty_id = faculty['faculty_id']
        timetable_entry.division_id = division['division_id']
        timetable_entry.day_of_week = day_code
        timetable_entry.lecture_no = entry_data.get('lecture_no', timetable_entry.lecture_no or 1)
        timetable_entry.room_no = entry_data.get('room_no')
        timetable_entry.start_time = start_time
        timetable_entry.end_time = end_time
        timetable_entry.building_block = entry_data.get('building_block')

        db.session.add(timetable_entry)
        db.session.commit()

        return {
            'entry_id': timetable_entry.timetable_id,
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
            'faculty_name': faculty.get('short_name') or faculty.get('full_name'),
            'room_no': entry_data.get('room_no', ''),
            'mode': entry_data.get('mode', 'Lecture'),
            'semester_id': subject.get('semester_id')
        }

    @staticmethod
    def delete_timetable_entry(entry_id):
        """Delete a timetable entry"""
        timetable_entry = Timetable.query.get(entry_id)
        if not timetable_entry:
            return False
        db.session.delete(timetable_entry)
        db.session.commit()
        return True

    @staticmethod
    def get_parent_children(user_id):
        """Get all children (students) for a parent with full details"""
        parent_records = Parent.query.filter_by(user_id=user_id).all()
        
        # Get full student details for each child
        children_details = []
        for record in parent_records:
            student_id = record.student_id
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
                    avg_pct = DataHelper._np_mean([r['attendance_percentage'] for r in week_filtered])
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
                    avg_pct = DataHelper._np_mean([r['attendance_percentage'] for r in month_filtered])
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
        colleges = College.query.order_by(College.college_name.asc()).all()
        return [DataHelper._college_dict(college) for college in colleges]

    @staticmethod
    def get_total_students_count():
        """Get total count of all students"""
        return Student.query.count()

    @staticmethod
    def get_total_faculty_count():
        """Get total count of all faculty members"""
        return Faculty.query.count()

    @staticmethod
    def get_total_departments_count():
        """Get total count of all departments"""
        return Department.query.count()
    
    @staticmethod
    def get_total_colleges_count():
        """Get total count of all colleges"""
        return College.query.count()
    
    @staticmethod
    def get_total_users_count():
        """Get total count of all users"""
        return User.query.count()
    
    @staticmethod
    def get_active_admins_count():
        """Get count of active admin users"""
        return User.query.join(Role).filter(Role.role_name == 'ADMIN').count()

    @staticmethod
    def get_recent_users(limit=5):
        """Get recently registered users"""
        users = User.query.order_by(User.created_at.desc()).limit(limit).all()
        return [DataHelper._user_dict(user) for user in users]

    @staticmethod
    def get_college_statistics(college_id):
        """Get statistics for a specific college"""
        total_students = Student.query.join(Department).filter(Department.college_id == college_id).count()
        # Explicit join needed because Department has foreign key to Faculty (hod_faculty_id) as well
        total_faculty = Faculty.query.join(Department, Faculty.dept_id == Department.dept_id).filter(Department.college_id == college_id).count()
        total_departments = Department.query.filter_by(college_id=college_id).count()
        total_divisions = Division.query.join(Department).filter(Department.college_id == college_id).count()

        attendance_records = [
            record for record in DataHelper.get_attendance_records()
            if record.get('dept_id') in {
                dept.dept_id for dept in Department.query.filter_by(college_id=college_id).all()
            }
        ]
        if attendance_records:
            avg_attendance = DataHelper._np_mean([r['attendance_percentage'] for r in attendance_records])
        else:
            avg_attendance = 0

        return {
            'total_students': total_students,
            'total_faculty': total_faculty,
            'total_departments': total_departments,
            'total_divisions': total_divisions,
            'average_attendance': round(avg_attendance, 2)
        }

    @staticmethod
    def get_all_users_list():
        """Get all users as a list"""
        users = User.query.order_by(User.user_id.asc()).all()
        return [DataHelper._user_dict(user) for user in users]

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
        
        avg_attendance = DataHelper._np_mean([r['attendance_percentage'] for r in records])
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
                avg_attendance = DataHelper._np_mean([r['attendance_percentage'] for r in dept_records])
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

    @staticmethod
    def get_day_wise_attendance():
        """Aggregate attendance percentages by day of week"""
        lecture_stats = db.session.query(
            Lecture.lecture_date.label('lecture_date'),
            func.count(Attendance.attendance_id).label('total'),
            func.sum(case((Attendance.status_id == 1, 1), else_=0)).label('present')
        ).join(Attendance, Attendance.lecture_id == Lecture.lecture_id) \
            .group_by(Lecture.lecture_date).all()

        day_map = defaultdict(list)
        for row in lecture_stats:
            total = row.total or 0
            present = row.present or 0
            percentage = (present / total) * 100 if total else 0.0
            day_name = row.lecture_date.strftime('%A')
            day_map[day_name].append(percentage)

        day_stats = []
        for day_name in DataHelper.DAY_ORDER:
            day_values = day_map.get(day_name, [])
            day_stats.append({
                'day': day_name,
                'percentage': round(DataHelper._np_mean(day_values), 2)
            })

        return day_stats

    @staticmethod
    def get_class_wise_attendance():
        """Aggregate attendance by division"""
        records = DataHelper.get_attendance_records()
        divisions = defaultdict(list)
        for record in records:
            divisions[record['division_name']].append(record['attendance_percentage'])

        class_stats = []
        for division_name, values in divisions.items():
            class_stats.append({
                'division': division_name,
                'percentage': round(DataHelper._np_mean(values), 2)
            })

        return sorted(class_stats, key=lambda item: item['division'])

    @staticmethod
    def get_faculty_analytics_payload():
        """Return analytics data and charts for faculty analytics view"""
        class_stats = DataHelper.get_class_wise_attendance()
        day_stats = DataHelper.get_day_wise_attendance()

        class_labels = [item['division'] for item in class_stats]
        class_values = [item['percentage'] for item in class_stats]
        day_labels = [item['day'] for item in day_stats]
        day_values = [item['percentage'] for item in day_stats]

        charts = {
            'class_chart': DataHelper._render_bar_chart(
                class_labels,
                class_values,
                'Class-wise Attendance Overview',
                'Attendance %',
                '#667eea'
            ),
            'day_chart': DataHelper._render_line_chart(
                day_labels,
                day_values,
                'Day-wise Attendance (Weekly Trend)',
                'Attendance %',
                '#ed8936'
            )
        }

        return {
            'class_stats': class_stats,
            'day_stats': day_stats,
            'charts': charts
        }

    @staticmethod
    def get_attendance_trend():
        """Attendance trend over time based on lecture dates"""
        lecture_stats = db.session.query(
            Lecture.lecture_date.label('lecture_date'),
            func.count(Attendance.attendance_id).label('total'),
            func.sum(case((Attendance.status_id == 1, 1), else_=0)).label('present')
        ).join(Attendance, Attendance.lecture_id == Lecture.lecture_id) \
            .group_by(Lecture.lecture_date) \
            .order_by(Lecture.lecture_date.asc())

        dates = []
        values = []
        for row in lecture_stats:
            total = row.total or 0
            present = row.present or 0
            percentage = (present / total) * 100 if total else 0.0
            dates.append(row.lecture_date.strftime('%Y-%m-%d'))
            values.append(round(percentage, 2))

        return dates, values

    @staticmethod
    def get_college_attendance_records():
        """Detailed attendance records for college analytics"""
        rows = db.session.query(
            Lecture.lecture_date.label('lecture_date'),
            Department.dept_id.label('dept_id'),
            Department.dept_name.label('dept_name'),
            Division.division_id.label('div_id'),
            Division.division_name.label('div_name'),
            func.count(Attendance.attendance_id).label('total'),
            func.sum(case((Attendance.status_id == 1, 1), else_=0)).label('present'),
            func.sum(case((Attendance.status_id == 2, 1), else_=0)).label('absent')
        ).join(Attendance, Attendance.lecture_id == Lecture.lecture_id) \
            .join(Student, Attendance.student_id == Student.student_id) \
            .join(Division, Student.division_id == Division.division_id) \
            .join(Department, Student.dept_id == Department.dept_id) \
            .group_by(
                Lecture.lecture_date,
                Department.dept_id,
                Department.dept_name,
                Division.division_id,
                Division.division_name
            ).order_by(Lecture.lecture_date.desc()).all()

        records = []
        for row in rows:
            total = row.total or 0
            present = row.present or 0
            absent = row.absent or 0
            present_percentage = (present / total) * 100 if total else 0.0
            records.append({
                'date': row.lecture_date.strftime('%Y-%m-%d'),
                'dept_id': row.dept_id,
                'dept_name': row.dept_name,
                'div_id': row.div_id,
                'div_name': row.div_name,
                'present': present,
                'absent': absent,
                'late': 0,
                'total': total,
                'present_percentage': round(present_percentage, 2)
            })

        return records

    @staticmethod
    def get_college_attendance_stats():
        """Summary stats for college analytics"""
        total_present = Attendance.query.filter(Attendance.status_id == 1).count()
        total_absent = Attendance.query.filter(Attendance.status_id == 2).count()
        total = total_present + total_absent
        total_days = db.session.query(func.count(func.distinct(Lecture.lecture_date))).scalar() or 0

        present_pct = (total_present / total) * 100 if total else 0.0
        absent_pct = (total_absent / total) * 100 if total else 0.0

        return {
            'present_count': total_present,
            'absent_count': total_absent,
            'late_count': 0,
            'total_days': total_days,
            'present_percentage': round(present_pct, 2),
            'absent_percentage': round(absent_pct, 2),
            'late_percentage': 0.0
        }

    @staticmethod
    def get_college_attendance_analytics():
        """Analytics payload for college attendance page"""
        stats = DataHelper.get_college_attendance_stats()
        attendance_records = DataHelper.get_college_attendance_records()
        dept_stats = DataHelper.get_department_performance()

        div_groups = defaultdict(list)
        for record in DataHelper.get_attendance_records():
            div_groups[record['division_name']].append(record['attendance_percentage'])
        div_labels = list(div_groups.keys())
        div_values = [round(DataHelper._np_mean(values), 2) for values in div_groups.values()]

        trend_dates, trend_values = DataHelper.get_attendance_trend()

        charts = {
            'attendance_distribution': DataHelper._render_donut_chart(
                ['Present', 'Absent', 'Late'],
                [stats['present_count'], stats['absent_count'], stats['late_count']],
                'Attendance Distribution',
                ['#51cf66', '#ff6b6b', '#ffd93d']
            ),
            'dept_attendance': DataHelper._render_bar_chart(
                [d['dept_name'] for d in dept_stats],
                [d['average_attendance'] for d in dept_stats],
                'Department-wise Attendance',
                'Attendance %',
                '#51cf66'
            ),
            'div_attendance': DataHelper._render_bar_chart(
                div_labels,
                div_values,
                'Division-wise Attendance',
                'Attendance %',
                '#4dabf7'
            ),
            'trend': DataHelper._render_line_chart(
                trend_dates,
                trend_values,
                'Daily Attendance Trend',
                'Attendance %',
                '#667eea'
            )
        }

        return {
            'stats': stats,
            'attendance_records': attendance_records,
            'charts': charts
        }

    @staticmethod
    def get_superadmin_charts(dept_performance):
        """Charts for superadmin analytics"""
        trend_dates, trend_values = DataHelper.get_attendance_trend()

        return {
            'attendance_trend': DataHelper._render_line_chart(
                trend_dates,
                trend_values,
                'Attendance Trend',
                'Attendance %',
                '#2563eb'
            ),
            'department_comparison': DataHelper._render_bar_chart(
                [d['dept_name'] for d in dept_performance],
                [d['average_attendance'] for d in dept_performance],
                'Department Comparison',
                'Attendance %',
                '#38bdf8'
            )
        }

    @staticmethod
    def get_compiled_attendance_report(dept_id, semester_id=None, division_id=None):
        """Generate compiled attendance report by student and subject
        
        Returns student attendance data aggregated by subject with faculty names.
        Used for generating attendance sheets like the compiled reports.
        """
        query = Student.query.filter_by(dept_id=dept_id)
        
        if division_id:
            query = query.filter_by(division_id=division_id)
        
        if semester_id:
            query = query.filter_by(semester_id=semester_id)
        
        students = query.all()
        subjects = Subject.query.all()
        
        if semester_id:
            subjects = [s for s in subjects if s.semester_id == semester_id]
        
        report_data = []
        
        for student in students:
            student_record = {
                'roll_no': student.roll_no,
                'enrollment_no': student.enrollment_no,
                'name': student.user.name if student.user else 'N/A',
                'division': student.division.division_name if student.division else 'N/A',
                'branch': student.department.dept_name if student.department else 'N/A',
                'mentor': student.mentor.faculty_short_name if student.mentor else 'N/A',
                'subjects': {},
                'total_attended': 0,
                'total_lectures': 0,
                'overall_percentage': 0.0
            }
            
            for subject in subjects:
                # Get all lectures for this subject and student's division
                lectures = Lecture.query.filter(
                    Lecture.division_id == student.division_id,
                    Lecture.subject_id == subject.subject_id
                ).all()
                
                if not lectures:
                    continue
                
                total_lectures_count = len(lectures)
                
                # Count attended lectures
                attended_count = Attendance.query.filter(
                    Attendance.student_id == student.student_id,
                    Attendance.lecture_id.in_([l.lecture_id for l in lectures]),
                    Attendance.status_id == 1  # PRESENT
                ).count()
                
                percentage = (attended_count / total_lectures_count * 100) if total_lectures_count > 0 else 0
                
                # Get faculty name
                faculty_name = ''
                if lectures and lectures[0].timetable:
                    faculty = lectures[0].timetable.faculty
                    faculty_name = faculty.faculty_short_name if faculty else ''
                
                student_record['subjects'][subject.subject_id] = {
                    'subject_name': subject.subject_name,
                    'subject_code': subject.subject_code,
                    'faculty_name': faculty_name,
                    'attended': attended_count,
                    'total': total_lectures_count,
                    'percentage': round(percentage, 2)
                }
                
                student_record['total_attended'] += attended_count
                student_record['total_lectures'] += total_lectures_count
            
            # Calculate overall percentage
            if student_record['total_lectures'] > 0:
                student_record['overall_percentage'] = round(
                    (student_record['total_attended'] / student_record['total_lectures'] * 100), 2
                )
            
            report_data.append(student_record)
        
        return report_data
