"""Faculty routes - Attendance, Analytics, Reports, Timetable, Profile"""
from flask import Blueprint, render_template, send_file, request, jsonify, session
from models.user import db, User
from models.division import Division
from services.data_helper import DataHelper
from services.export_service import ExportService
from attendance_system.utils.auth_decorators import login_required, faculty_required
from services.chart_helper import (
    generate_attendance_weekly_chart,
    generate_attendance_monthly_chart,
    generate_subject_attendance_chart
)
import csv
import io
from datetime import datetime
import numpy as np

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')


@faculty_bp.route("/dashboard")
@faculty_required
def fdashboard():
    """Faculty dashboard showing assigned subjects and classes"""
    faculty_data = DataHelper.get_faculty()
    
    # Handle case where get_faculty() returns a list or None
    if isinstance(faculty_data, list):
        faculty = faculty_data[0] if faculty_data else None
    else:
        faculty = faculty_data
    
    subjects = DataHelper.get_subjects()
    lectures = DataHelper.get_lectures()
    attendance_data = DataHelper.get_attendance_records()
    
    # Get department info for the faculty
    department = None
    if faculty and faculty.get('dept_id'):
        dept = DataHelper.get_department(faculty.get('dept_id'))
        department = {'dept_name': dept.get('dept_name', 'N/A')} if isinstance(dept, dict) else {'dept_name': 'N/A'}
    else:
        department = {'dept_name': 'N/A'}
    
    # Calculate average attendance from actual data
    attendance_percentages = [a.get('attendance_percentage', 0) for a in (attendance_data or [])]
    avg_attendance = round(DataHelper._np_mean(attendance_percentages), 2) if attendance_percentages else 0.0
    
    # Compute stats for dashboard
    stats = {
        'total_lectures': len(lectures) if lectures else 0,
        'remaining': max(0, (len(lectures) - 1) if lectures else 0),
        'subjects': len(subjects) if subjects else 0,
        'avg_attendance': avg_attendance
    }
    
    # Calculate proxies taken and mentoring count from actual data
    proxy_requests = DataHelper.get_proxy_requests()
    proxy_taken = len([p for p in (proxy_requests or []) if p.get('faculty_id') == faculty.get('faculty_id')]) if faculty else 0
    
    # Count students mentored (based on available data)
    students = DataHelper.get_students()
    mentoring_count = len([s for s in (students or []) if s.get('mentor_id') == faculty.get('faculty_id')]) if faculty else 0
    
    # Teaching stats for template
    teaching_stats = {
        'lectures_conducted': len(lectures) if lectures else 0,
        'total_subjects': len(subjects) if subjects else 0,
        'proxy_taken': proxy_taken,
        'mentoring_count': mentoring_count
    }
    
    return render_template("faculty/dashboard.html", 
                          faculty=faculty, 
                          subjects=subjects, 
                          lectures=lectures,
                          stats=stats,
                          teaching_stats=teaching_stats,
                          department=department,
                          datetime=datetime)


@faculty_bp.route("/attendance")
@faculty_required
def fattendance():
    """Record attendance for lectures - only show lectures from timetable"""
    from datetime import datetime as dt, timedelta
    
    # Get faculty from session
    faculty_user_id = session.get('user_id')
    from models.faculty import Faculty
    from models.timetable import Timetable
    from models.subject import Subject
    from models.academic_calendar import AcademicCalendar
    
    faculty = Faculty.query.filter_by(user_id=faculty_user_id).first()
    
    if not faculty:
        return render_template("faculty/attendance.html", divisions=[], datetime=dt, error="Faculty not found")
    
    # Get divisions where this faculty teaches
    divisions = DataHelper.get_divisions()
    
    # For each division, add subjects that this faculty teaches
    for division in divisions:
        # Initialize subjects array
        division['subjects'] = []
        
        # Get subjects the faculty teaches for this division
        timetable_entries = Timetable.query.filter_by(
            faculty_id=faculty.faculty_id,
            division_id=division['div_id']
        ).all()
        
        # Get unique subjects with next lecture dates
        subjects_data = []
        for timetable in timetable_entries:
            subject = timetable.subject
            
            # Find next scheduled lecture date (based on timetable day of week)
            today = dt.now().date()
            next_lecture = None
            
            for days_ahead in range(30):  # Check next 30 days
                check_date = today + timedelta(days=days_ahead)
                day_name = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'][check_date.weekday()]
                
                # Check if this is a scheduled day and not a holiday
                if timetable.day_of_week == day_name:
                    # Check academic calendar for holidays
                    is_holiday = AcademicCalendar.query.filter_by(
                        event_date=check_date,
                        dept_id=division['dept_id']
                    ).first()
                    
                    if not is_holiday:
                        next_lecture = check_date
                        break
            
            subjects_data.append({
                'id': subject.subject_id,
                'name': subject.subject_name,
                'code': subject.subject_code,
                'next_lecture': next_lecture.strftime('%Y-%m-%d') if next_lecture else 'No schedule'
            })
        
        division['subjects'] = subjects_data
    
    # Filter out divisions where faculty teaches no subjects
    divisions = [d for d in divisions if d.get('subjects')]
    
    return render_template("faculty/attendance.html", 
                          divisions=divisions, 
                          datetime=dt)


@faculty_bp.route("/attendance/students/<int:division_id>")
@faculty_required
def get_students_by_division(division_id):
    """Get all students in a division for attendance marking"""
    try:
        students = DataHelper.get_students(division_id=division_id)
        return jsonify({'students': students})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@faculty_bp.route("/attendance/mark", methods=['POST'])
@faculty_required
def mark_attendance():
    """Mark attendance for a lecture - validates against academic calendar"""
    try:
        data = request.get_json()
        division_id = data.get('division_id')
        subject_id = data.get('subject_id')
        lecture_date = data.get('lecture_date')
        attendance_data = data.get('attendance')  # List of {student_id, status}
        
        if not all([division_id, subject_id, lecture_date, attendance_data]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        from models.timetable import Timetable
        from models.lecture import Lecture
        from models.attendance import Attendance, AttendanceStatus
        from models.academic_calendar import AcademicCalendar
        from models.student import Student
        from datetime import datetime as dt
        
        # Get faculty from session
        faculty_user_id = session.get('user_id')
        from models.faculty import Faculty
        faculty = Faculty.query.filter_by(user_id=faculty_user_id).first()
        if not faculty:
            return jsonify({'error': 'Faculty not found'}), 404
        
        # Parse lecture date
        try:
            lecture_date_obj = dt.strptime(lecture_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
        
        # Get department ID from division
        division = db.session.query(Division).get(division_id)
        if not division:
            return jsonify({'error': 'Division not found'}), 404
        
        # Check if this date is a holiday/on the academic calendar
        is_holiday = AcademicCalendar.query.filter_by(
            event_date=lecture_date_obj,
            dept_id=division.dept_id
        ).first()
        
        if is_holiday:
            return jsonify({'error': f'Cannot mark attendance on {is_holiday.description or "holiday"}'}), 400
        
        # Check if it's a weekend or timetable doesn't have class
        timetable = Timetable.query.filter_by(
            subject_id=subject_id,
            faculty_id=faculty.faculty_id,
            division_id=division_id
        ).first()
        
        if not timetable:
            return jsonify({'error': 'Timetable entry not found for this subject and division'}), 404
        
        # Verify the date matches the timetable day
        day_of_week = lecture_date_obj.strftime('%A')
        timetable_day_map = {'Monday': 'MON', 'Tuesday': 'TUE', 'Wednesday': 'WED', 'Thursday': 'THU', 'Friday': 'FRI', 'Saturday': 'SAT', 'Sunday': 'SUN'}
        expected_day = timetable_day_map.get(day_of_week, '')
        
        if expected_day != timetable.day_of_week:
            return jsonify({'error': f'No class scheduled on {day_of_week} for this subject'}), 400
        
        # Create lecture record if it doesn't exist
        lecture = Lecture.query.filter_by(
            timetable_id=timetable.timetable_id,
            lecture_date=lecture_date_obj
        ).first()
        
        if not lecture:
            lecture = Lecture(
                timetable_id=timetable.timetable_id,
                lecture_date=lecture_date_obj
            )
            db.session.add(lecture)
            db.session.flush()
        
        # Get status IDs
        present_status = AttendanceStatus.query.filter_by(status_name='PRESENT').first()
        absent_status = AttendanceStatus.query.filter_by(status_name='ABSENT').first()
        
        if not present_status or not absent_status:
            return jsonify({'error': 'Attendance status not configured'}), 500
        
        # Mark attendance for each student (only if they exist in division)
        marked_count = 0
        for record in attendance_data:
            student_id = record.get('student_id')
            status = record.get('status', 'PRESENT')
            
            # Verify student belongs to this division
            student = Student.query.get(student_id)
            if not student or student.division_id != division_id:
                continue
            
            # Check if attendance already exists
            existing = Attendance.query.filter_by(
                student_id=student_id,
                lecture_id=lecture.lecture_id
            ).first()
            
            status_id = present_status.status_id if status == 'PRESENT' else absent_status.status_id
            
            if existing:
                # Update existing attendance
                existing.status_id = status_id
                existing.marked_at = dt.utcnow()
            else:
                # Create new attendance record
                new_attendance = Attendance(
                    student_id=student_id,
                    lecture_id=lecture.lecture_id,
                    status_id=status_id,
                    marked_at=dt.utcnow()
                )
                db.session.add(new_attendance)
            
            marked_count += 1
        
        db.session.commit()
        return jsonify({'message': f'Attendance marked successfully for {marked_count} students'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@faculty_bp.route("/attendance/get", methods=['GET'])
@faculty_required
def get_attendance():
    """Get existing attendance for a lecture to enable editing"""
    try:
        division_id = request.args.get('division_id', type=int)
        subject_id = request.args.get('subject_id', type=int)
        lecture_date = request.args.get('lecture_date')
        
        if not all([division_id, subject_id, lecture_date]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        from models.timetable import Timetable
        from models.lecture import Lecture
        from models.attendance import Attendance, AttendanceStatus
        from datetime import datetime as dt
        
        # Get faculty from session
        faculty_user_id = session.get('user_id')
        from models.faculty import Faculty
        faculty = Faculty.query.filter_by(user_id=faculty_user_id).first()
        if not faculty:
            return jsonify({'error': 'Faculty not found'}), 404
        
        # Find timetable entry
        timetable = Timetable.query.filter_by(
            subject_id=subject_id,
            faculty_id=faculty.faculty_id,
            division_id=division_id
        ).first()
        
        if not timetable:
            return jsonify({'exists': False, 'attendance': []})
        
        # Find lecture
        lecture_date_obj = dt.strptime(lecture_date, '%Y-%m-%d').date()
        lecture = Lecture.query.filter_by(
            timetable_id=timetable.timetable_id,
            lecture_date=lecture_date_obj
        ).first()
        
        if not lecture:
            return jsonify({'exists': False, 'attendance': []})
        
        # Get attendance records
        attendance_records = Attendance.query.filter_by(lecture_id=lecture.lecture_id).all()
        
        attendance_data = [
            {
                'student_id': record.student_id,
                'status': record.status.status_name
            }
            for record in attendance_records
        ]
        
        return jsonify({
            'exists': True,
            'attendance': attendance_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@faculty_bp.route("/analytics")
def fanalytics():
    """View attendance analytics and statistics"""
    # Get current faculty from session
    faculty_user_id = session.get('user_id')
    from models.faculty import Faculty
    current_faculty = Faculty.query.filter_by(user_id=faculty_user_id).first()
    
    faculty = DataHelper.get_faculty()
    
    # Filter attendance records by current faculty's college
    college_id = current_faculty.department.college_id if current_faculty and current_faculty.department else None
    attendance_data = DataHelper.get_attendance_records(college_id=college_id)

    total_lectures = len(DataHelper.get_lectures())
    avg_attendance = DataHelper._np_mean([a.get('attendance_percentage', 0) for a in attendance_data])

    analytics_payload = DataHelper.get_faculty_analytics_payload()
    class_stats = analytics_payload['class_stats']
    day_stats = analytics_payload['day_stats']

    best_class = max(class_stats, key=lambda item: item['percentage']) if class_stats else None
    lowest_day = min(day_stats, key=lambda item: item['percentage']) if day_stats else None

    # Generate charts
    charts = {}
    
    # Weekly attendance chart - calculate from actual data
    weekly_data = {}
    if attendance_data:
        days_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
        day_attendance = {}
        for record in attendance_data:
            if 'date' in record:
                try:
                    date_obj = datetime.fromisoformat(str(record['date'])) if isinstance(record['date'], str) else record['date']
                    day_name = days_map.get(date_obj.weekday(), 'Unknown')
                    if day_name not in day_attendance:
                        day_attendance[day_name] = []
                    day_attendance[day_name].append(record.get('attendance_percentage', 0))
                except:
                    pass
        # Calculate average for each day
        for day, percentages in day_attendance.items():
            float_percentages = [float(p) for p in percentages]
            weekly_data[day] = round(float(np.mean(float_percentages)), 1) if float_percentages else 0.0
    # Add missing days with zero
    for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']:
        if day not in weekly_data:
            weekly_data[day] = 0.0
    charts['weekly_attendance'] = generate_attendance_weekly_chart(weekly_data)
    
    # Monthly trend chart - calculate from actual data grouped by week
    monthly_data = {}
    if attendance_data:
        week_attendance = {}
        for record in attendance_data:
            if 'date' in record:
                try:
                    date_obj = datetime.fromisoformat(str(record['date'])) if isinstance(record['date'], str) else record['date']
                    week_num = date_obj.isocalendar()[1]
                    week_key = f'Week {week_num % 4 if week_num % 4 > 0 else 4}'
                    if week_key not in week_attendance:
                        week_attendance[week_key] = []
                    week_attendance[week_key].append(record.get('attendance_percentage', 0))
                except:
                    pass
        # Calculate average for each week
        for week, percentages in sorted(week_attendance.items()):
            float_percentages = [float(p) for p in percentages]
            monthly_data[week] = round(float(np.mean(float_percentages)), 1) if float_percentages else 0.0
    # Add default weeks if needed
    if not monthly_data:
        for i in range(1, 5):
            monthly_data[f'Week {i}'] = 0.0
    charts['monthly_trend'] = generate_attendance_monthly_chart(monthly_data)
    
    # Subject attendance chart - calculate actual averages per subject
    subject_data = {}
    subjects = DataHelper.get_subjects()
    if attendance_data and subjects:
        for subject in subjects:
            subject_id = subject.get('subject_id')
            subject_name = subject.get('subject_name', 'Unknown')
            subject_records = [a for a in attendance_data if a.get('subject_id') == subject_id]
            if subject_records:
                percentages = [a.get('attendance_percentage', 0) for a in subject_records]
                float_percentages = [float(p) for p in percentages]
                subject_data[subject_name] = round(float(np.mean(float_percentages)), 1) if float_percentages else 0.0
            else:
                subject_data[subject_name] = 0.0
    else:
        # Fallback: ensure all subjects have an entry
        for subject in (subjects or []):
            subject_name = subject.get('subject_name', 'Unknown')
            subject_data[subject_name] = 0.0
    
    if subject_data:
        charts['subject_attendance'] = generate_subject_attendance_chart(subject_data)

    return render_template(
        "faculty/analytics.html",
        faculty=faculty,
        attendance_data=attendance_data,
        total_lectures=total_lectures,
        avg_attendance=round(avg_attendance, 2),
        class_stats=class_stats,
        day_stats=day_stats,
        charts=charts,
        best_class=best_class,
        lowest_day=lowest_day
    )


@faculty_bp.route("/reports")
@faculty_bp.route("/reports")
def freports():
    """View and manage attendance reports with detailed subjectwise attendance"""
    from models.lecture import Lecture
    from models.timetable import Timetable
    from models.faculty import Faculty
    
    # Get current faculty and their college
    faculty_user_id = session.get('user_id')
    current_faculty = Faculty.query.filter_by(user_id=faculty_user_id).first()
    faculty_college_id = current_faculty.department.college_id if current_faculty and current_faculty.department else None
    faculty_dept_id = current_faculty.dept_id if current_faculty else None
    
    # Get faculty data (filtered by college if needed)
    faculty = DataHelper.get_faculty(dept_id=faculty_dept_id)
    
    # Get students and attendance data for current college only
    students = DataHelper.get_students()
    attendance_data = DataHelper.get_attendance_records(college_id=faculty_college_id)
    subjects = DataHelper.get_subjects()
    
    # Filter students to only those in the same college
    filtered_students = [
        s for s in students 
        if s.get('college_id') == faculty_college_id
    ] if students else []
    
    # Build comprehensive attendance report with numpy calculations
    student_reports = {}
    
    if filtered_students:
        for student in filtered_students:
            student_id = student.get('student_id')
            mentor_name = None
            mentor_short_name = None
            
            # Get mentor name and short name if assigned
            if student.get('mentor_id'):
                mentor = DataHelper.get_faculty_member(faculty_id=student.get('mentor_id'))
                if mentor:
                    mentor_name = mentor.get('name', 'N/A')
                    mentor_short_name = mentor.get('short_name', 'N/A')
            
            student_reports[student_id] = {
                'student_id': student_id,
                'roll_no': student.get('roll_no', ''),
                'name': student.get('name', ''),
                'enrollment_no': student.get('enrollment_no', ''),
                'division_name': student.get('division_name', ''),
                'division_short': student.get('division_short', ''),
                'dept_name': student.get('dept_name', ''),
                'college_id': student.get('college_id'),
                'mentor_name': mentor_name or 'N/A',
                'mentor_short_name': mentor_short_name or 'N/A',
                'subjectwise_attendance': {},
                'overall_attendance': 0,
                'total_lectures': 0,
                'attended_lectures': 0
            }
    
    # Calculate subjectwise attendance using numpy
    if attendance_data:
        for record in attendance_data:
            student_id = record.get('student_id')
            subject_name = record.get('subject_name', 'Unknown')
            subject_code = record.get('subject_code', '')
            attendance_pct = record.get('attendance_percentage', 0)
            total_lectures = record.get('total_lectures', 0)
            attended_lectures = record.get('attended_lectures', 0)
            
            if student_id in student_reports:
                student_reports[student_id]['subjectwise_attendance'][subject_name] = {
                    'subject_code': subject_code,
                    'attendance_percentage': round(float(attendance_pct), 2),
                    'total_lectures': total_lectures,
                    'attended_lectures': attended_lectures,
                    'status': 'PASS' if float(attendance_pct) >= 75 else 'FAIL'
                }
    
    # Calculate overall attendance using numpy
    for student_id, report in student_reports.items():
        if report['subjectwise_attendance']:
            percentages = np.array([
                v['attendance_percentage'] 
                for v in report['subjectwise_attendance'].values()
            ], dtype=float)
            
            total_lecs = np.array([
                v['total_lectures'] 
                for v in report['subjectwise_attendance'].values()
            ], dtype=int)
            
            attended_lecs = np.array([
                v['attended_lectures'] 
                for v in report['subjectwise_attendance'].values()
            ], dtype=int)
            
            # Use numpy for calculations
            report['overall_attendance'] = float(np.mean(percentages))
            report['total_lectures'] = int(np.sum(total_lecs))
            report['attended_lectures'] = int(np.sum(attended_lecs))
            
            # Round the overall percentage
            report['overall_attendance'] = round(report['overall_attendance'], 2)
    
    # Convert to list and sort by roll_no
    student_reports_list = sorted(
        student_reports.values(),
        key=lambda x: int(x.get('roll_no', 0)) if str(x.get('roll_no', '0')).isdigit() else 0
    )
    
    # Get unique subjects sorted
    unique_subjects = sorted(set(
        subject_name 
        for record in attendance_data or []
        for subject_name in [record.get('subject_name', 'Unknown')]
    )) if attendance_data else []
    
    return render_template("faculty/reports.html",
                          faculty=faculty,
                          subjects=unique_subjects,
                          students=student_reports_list,
                          attendance_data=attendance_data,
                          college_id=faculty_college_id,
                          datetime=datetime)



@faculty_bp.route("/timetable")
def ftimetable():
    """View faculty timetable"""
    faculty = DataHelper.get_faculty()
    timetable = DataHelper.get_timetable()
    subjects = DataHelper.get_subjects()
    
    return render_template("faculty/timetable.html",
                          faculty=faculty,
                          timetable=timetable,
                          subjects=subjects)


@faculty_bp.route("/profile")
@faculty_required
def fprofile():
    """View and edit faculty profile"""
    from models.user import User
    from models.college import College
    from models.department import Department
    from models.faculty import Faculty
    
    # Get current user
    user_data = DataHelper.get_user('faculty')
    if not user_data:
        return render_template("faculty/profile.html",
                             user=None,
                             faculty=None,
                             college=None,
                             department=None,
                             teaching_stats={})
    
    # Get faculty record
    faculty_record = Faculty.query.filter_by(user_id=user_data['user_id']).first()
    faculty = DataHelper._faculty_dict(faculty_record) if faculty_record else None
    
    # Get college
    college = College.query.get(user_data['college_id']) if user_data.get('college_id') else None
    
    # Get department
    department = None
    if faculty and faculty.get('dept_id'):
        department = Department.query.get(faculty.get('dept_id'))
    
    # Compute teaching statistics from actual data
    subjects = DataHelper.get_subjects(dept_id=faculty.get('dept_id') if faculty else None)
    lectures = DataHelper.get_lectures()
    
    # Calculate proxies taken
    proxy_requests = DataHelper.get_proxy_requests()
    proxy_taken = len([p for p in (proxy_requests or []) if p.get('faculty_id') == (faculty.get('faculty_id') if faculty else None)]) if faculty else 0
    
    # Count students mentored
    students = DataHelper.get_students()
    mentoring_count = len([s for s in (students or []) if s.get('mentor_id') == (faculty.get('faculty_id') if faculty else None)]) if faculty else 0
    
    teaching_stats = {
        'total_subjects': len(subjects) if subjects else 0,
        'lectures_conducted': len(lectures) if lectures else 0,
        'proxy_taken': proxy_taken,
        'mentoring_count': mentoring_count
    }
    
    return render_template("faculty/profile.html",
                          user=user_data,
                          faculty=faculty,
                          college=college,
                          department=department,
                          teaching_stats=teaching_stats)


@faculty_bp.route("/download-report", methods=['GET', 'POST'])
def download_report():
    """Download attendance report as CSV"""
    attendance_data = DataHelper.get_attendance_records()
    students = DataHelper.get_students()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Student ID', 'Student Name', 'Subject', 'Attendance Percentage', 'Status'])
    
    # Write data
    for record in attendance_data:
        writer.writerow([
            record.get('student_id', ''),
            record.get('student_name', ''),
            record.get('subject', ''),
            f"{record.get('attendance_percentage', 0):.2f}%",
            record.get('status', '')
        ])
    
    # Convert to bytes
    output.seek(0)
    bytes_io = io.BytesIO()
    bytes_io.write(output.getvalue().encode('utf-8'))
    bytes_io.seek(0)
    
    return send_file(
        bytes_io,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'attendance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )


@faculty_bp.route("/approvals")
def faculty_approvals():
    """View pending student and parent approvals"""
    faculty = DataHelper.get_faculty()
    
    # Get pending students and parents
    pending_users = User.query.filter(
        User.is_approved == False,
        User.role_id.in_([5, 6])  # STUDENT=5, PARENT=6
    ).all()
    
    return render_template("faculty/approvals.html",
                          title="Pending Approvals",
                          faculty=faculty,
                          pending_users=pending_users)


@faculty_bp.route("/approve/user/<int:user_id>", methods=['POST'])
def faculty_approve_user(user_id):
    """Approve a student or parent"""
    try:
        user = User.query.get(user_id)
        if user and user.role_id in [5, 6]:  # STUDENT, PARENT
            user.is_approved = True
            db.session.commit()
            return jsonify({'success': True, 'message': f'{user.role.role_name} "{user.name}" approved successfully'})
        return jsonify({'success': False, 'message': 'User not found or invalid role'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@faculty_bp.route("/reject/user/<int:user_id>", methods=['POST'])
def faculty_reject_user(user_id):
    """Reject/Delete a user"""
    try:
        user = User.query.get(user_id)
        if user:
            user_name = user.name
            user_role = user.role.role_name
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': True, 'message': f'{user_role} "{user_name}" rejected and removed'})
        return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@faculty_bp.route("/profile/update", methods=['POST'])
@faculty_required
def faculty_update_profile():
    """Update faculty profile information"""
    from models.faculty import Faculty
    
    try:
        data = request.get_json()
        
        # Get current user
        user_data = DataHelper.get_user('faculty')
        if not user_data:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Get user and faculty records
        user = User.query.get(user_data['user_id'])
        faculty = Faculty.query.filter_by(user_id=user_data['user_id']).first()
        
        if not user or not faculty:
            return jsonify({'success': False, 'message': 'User or faculty record not found'}), 404
        
        # Update user information
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.mobile = data.get('mobile', user.mobile)
        
        # Update faculty information
        faculty.short_name = data.get('short_name', faculty.short_name)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error updating profile: {str(e)}'}), 500


@faculty_bp.route("/profile/change-password", methods=['POST'])
@faculty_required
def faculty_change_password():
    """Change faculty password"""
    try:
        data = request.get_json()
        
        # Get current user
        user_data = DataHelper.get_user('faculty')
        if not user_data:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        user = User.query.get(user_data['user_id'])
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Verify current password
        if not user.check_password(data.get('current_password')):
            return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
        
        # Update password
        user.set_password(data.get('new_password'))
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Password changed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error changing password: {str(e)}'}), 500


@faculty_bp.route("/export/csv")
@faculty_required
def export_attendance_csv():
    """Export compiled attendance report as CSV"""
    try:
        csv_output = ExportService.export_csv()
        return send_file(
            io.BytesIO(csv_output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'compiled_attendance_week12_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@faculty_bp.route("/export/pdf")
@faculty_required
def export_attendance_pdf():
    """Export compiled attendance report as PDF"""
    try:
        pdf_output = ExportService.export_pdf()
        return send_file(
            pdf_output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'compiled_attendance_week12_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
    except RuntimeError as e:
        return jsonify({'error': str(e), 'message': 'reportlab library required'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

