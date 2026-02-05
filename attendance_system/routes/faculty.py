"""
Faculty routes - Attendance, Analytics, Reports, Timetable, Profile
"""
from flask import Blueprint, render_template, send_file, request
from datetime import datetime, timedelta
import csv
import io
from calendar import monthcalendar, month_name
import random

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

def get_mock_data():
    from app import mock_users, mock_faculty, mock_college, mock_department, mock_teaching_stats
    return mock_users, mock_faculty, mock_college, mock_department, mock_teaching_stats


@faculty_bp.route("/dashboard")
def fdashboard():
    """Faculty Dashboard with timetable and proxy requests"""
    mock_users, mock_faculty, mock_college, mock_department, mock_teaching_stats = get_mock_data()
    
    # Today's Timetable Mock Data
    today = datetime.now().strftime('%A').upper()[:3]
    timetable = [
        {
            'timetable_id': 1,
            'subject_name': 'Web Technologies',
            'subject_code': 'CS301',
            'division_name': 'CSE-A',
            'start_time': '09:00 AM',
            'end_time': '10:00 AM',
            'room_no': '401',
            'is_completed': True
        },
        {
            'timetable_id': 2,
            'subject_name': 'Database Management',
            'subject_code': 'CS302',
            'division_name': 'CSE-B',
            'start_time': '10:00 AM',
            'end_time': '11:00 AM',
            'room_no': '402',
            'is_completed': False
        },
        {
            'timetable_id': 3,
            'subject_name': 'Operating Systems',
            'subject_code': 'CS303',
            'division_name': 'CSE-A',
            'start_time': '11:15 AM',
            'end_time': '12:15 PM',
            'room_no': '401',
            'is_completed': False
        }
    ]

    # Proxy Lectures Mock Data
    proxies = [
        {
            'proxy_id': 1,
            'subject_name': 'Data Structures',
            'division_name': 'ECE-A',
            'lecture_date': datetime.now().strftime('%Y-%m-%d'),
            'lecture_no': 4,
            'original_faculty': 'Dr. Rajesh Kumar',
            'status': 'PENDING'
        }
    ]

    stats = {
        'total_lectures': 4,
        'completed': 1,
        'remaining': 3,
        'proxy_pending': 1
    }

    return render_template("faculty/dashboard.html",
                         title="Faculty Dashboard",
                         user=mock_users['faculty'],
                         faculty=mock_faculty,
                         department=mock_department,
                         teaching_stats=mock_teaching_stats,
                         timetable=timetable,
                         proxies=proxies,
                         stats=stats,
                         datetime=datetime)


@faculty_bp.route("/attendance")
def faculty_attendance():
    """Faculty Attendance Management"""
    divisions = [
        {'div_id': 1, 'division_name': 'CSE-A', 'subjects': [{'id': 1, 'name': 'Web Technologies'}, {'id': 2, 'name': 'Operating Systems'}]},
        {'div_id': 2, 'division_name': 'CSE-B', 'subjects': [{'id': 3, 'name': 'Database Management'}]}
    ]
    mock_users, _, _, _, _ = get_mock_data()
    return render_template("faculty/attendance.html",
                         title="Attendance Management",
                         user=mock_users['faculty'],
                         divisions=divisions,
                         datetime=datetime)


@faculty_bp.route("/analytics")
def faculty_analytics():
    """Faculty Attendance Analytics"""
    mock_users, _, _, _, _ = get_mock_data()
    class_wise_attendance = [
        {'division': 'CSE-A', 'percentage': 85},
        {'division': 'CSE-B', 'percentage': 78},
        {'division': 'ECE-A', 'percentage': 92},
    ]
    day_wise_attendance = [
        {'day': 'Monday', 'percentage': 88},
        {'day': 'Tuesday', 'percentage': 82},
        {'day': 'Wednesday', 'percentage': 85},
        {'day': 'Thursday', 'percentage': 80},
        {'day': 'Friday', 'percentage': 84},
        {'day': 'Saturday', 'percentage': 75},
    ]
    return render_template("faculty/analytics.html",
                         title="Attendance Analytics",
                         user=mock_users['faculty'],
                         class_stats=class_wise_attendance,
                         day_stats=day_wise_attendance)


@faculty_bp.route("/reports")
def faculty_reports():
    """Faculty Attendance Reports"""
    mock_users, _, _, _, _ = get_mock_data()
    students = [
        {'id': 1, 'roll_no': '101', 'name': 'Raj Kumar', 'attendance': 92},
        {'id': 2, 'roll_no': '102', 'name': 'Priya Singh', 'attendance': 88},
        {'id': 3, 'roll_no': '103', 'name': 'Amit Verma', 'attendance': 75},
    ]
    return render_template("faculty/reports.html",
                         title="Attendance Reports",
                         user=mock_users['faculty'],
                         students=students,
                         datetime=datetime)


@faculty_bp.route("/timetable")
def faculty_timetable():
    """Faculty Weekly Timetable"""
    mock_users, _, _, _, _ = get_mock_data()
    return render_template("faculty/timetable.html",
                         title="Weekly Timetable",
                         user=mock_users['faculty'])


@faculty_bp.route("/profile")
def faculty_profile():
    """Faculty Profile"""
    mock_users, mock_faculty, mock_college, mock_department, mock_teaching_stats = get_mock_data()
    return render_template("faculty/profile.html",
                         title="Faculty Profile",
                         user=mock_users['faculty'],
                         faculty=mock_faculty,
                         college=mock_college,
                         department=mock_department,
                         teaching_stats=mock_teaching_stats,
                         datetime=datetime)


# ==================== HELPER FUNCTIONS FOR REPORT GENERATION ====================

def generate_sample_attendance_data(dept_id, year, month, report_type):
    """Generate sample attendance data for students in a department"""

    # Department to students mapping
    dept_students = {
        '1': [  # CSE Department
            {'roll_no': '101', 'name': 'Raj Kumar', 'enrollment': 'EN2023001'},
            {'roll_no': '102', 'name': 'Priya Singh', 'enrollment': 'EN2023002'},
            {'roll_no': '103', 'name': 'Amit Verma', 'enrollment': 'EN2023003'},
            {'roll_no': '104', 'name': 'Anjali Sharma', 'enrollment': 'EN2023004'},
            {'roll_no': '105', 'name': 'Rohan Patel', 'enrollment': 'EN2023005'},
        ],
        '2': [  # ECE Department
            {'roll_no': '201', 'name': 'Neha Gupta', 'enrollment': 'EN2023006'},
            {'roll_no': '202', 'name': 'Vikram Singh', 'enrollment': 'EN2023007'},
            {'roll_no': '203', 'name': 'Sakshi Kumar', 'enrollment': 'EN2023008'},
            {'roll_no': '204', 'name': 'Arjun Nair', 'enrollment': 'EN2023009'},
        ],
        '3': [  # ME Department
            {'roll_no': '301', 'name': 'Deepak Verma', 'enrollment': 'EN2023010'},
            {'roll_no': '302', 'name': 'Kavya Reddy', 'enrollment': 'EN2023011'},
            {'roll_no': '303', 'name': 'Nikhil Sharma', 'enrollment': 'EN2023012'},
        ]
    }

    students = dept_students.get(str(dept_id), [])

    # Get calendar for the month
    if report_type == 'monthly':
        cal = monthcalendar(year, month)
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, cal[-1][-1])
    else:  # weekly
        today = datetime(year, month, 1)
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)

    data = []
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday to Friday
            for student in students:
                is_present = random.random() < 0.85

                data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'roll_no': student['roll_no'],
                    'name': student['name'],
                    'enrollment': student['enrollment'],
                    'status': 'PRESENT' if is_present else 'ABSENT'
                })

        current_date += timedelta(days=1)

    return data, students


def create_attendance_csv(dept_id, year, month, report_type):
    """Create CSV file for attendance report"""

    attendance_data, students = generate_sample_attendance_data(dept_id, year, month, report_type)

    # Calculate summary stats
    summary = {}
    for student in students:
        roll = student['roll_no']
        student_records = [r for r in attendance_data if r['roll_no'] == roll]
        total = len(student_records)
        present = len([r for r in student_records if r['status'] == 'PRESENT'])
        percentage = (present / total * 100) if total > 0 else 0

        summary[roll] = {
            'name': student['name'],
            'enrollment': student['enrollment'],
            'total': total,
            'present': present,
            'absent': total - present,
            'percentage': round(percentage, 2)
        }

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    dept_names = {
        '1': 'Computer Science & Engineering',
        '2': 'Electronics Engineering',
        '3': 'Mechanical Engineering'
    }

    period_type = 'Monthly' if report_type == 'monthly' else 'Weekly'
    period_str = f"{month_name[month]} {year}" if report_type == 'monthly' else f"Week of {(datetime(year, month, 1) - timedelta(days=(datetime(year, month, 1).weekday()))).strftime('%Y-%m-%d')}"

    writer.writerow(['ATTENDANCE REPORT'])
    writer.writerow([f"{period_type} Report - {period_str}"])
    writer.writerow([f"Department: {dept_names.get(str(dept_id), 'Unknown')}"])
    writer.writerow([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
    writer.writerow([])

    # Summary Table
    writer.writerow(['STUDENT ATTENDANCE SUMMARY'])
    writer.writerow(['Roll No', 'Name', 'Enrollment No', 'Total Lectures', 'Present', 'Absent', 'Percentage', 'Status'])

    for roll_no, data in summary.items():
        status = 'ELIGIBLE' if data['percentage'] >= 75 else 'DE-BARRED'
        writer.writerow([
            roll_no,
            data['name'],
            data['enrollment'],
            data['total'],
            data['present'],
            data['absent'],
            f"{data['percentage']}%",
            status
        ])

    writer.writerow([])
    writer.writerow(['DETAILED DAILY ATTENDANCE'])
    writer.writerow(['Date', 'Roll No', 'Name', 'Status'])

    for record in sorted(attendance_data, key=lambda x: (x['date'], x['roll_no'])):
        writer.writerow([
            record['date'],
            record['roll_no'],
            record['name'],
            record['status']
        ])

    # Convert to bytes
    output.seek(0)
    return output.getvalue()


@faculty_bp.route("/download-report")
def download_report():
    """Download attendance report as CSV"""

    report_type = request.args.get('type', 'monthly')
    dept_id = request.args.get('dept', '1')
    month_str = request.args.get('month', datetime.now().strftime('%Y-%m'))

    try:
        year, month = map(int, month_str.split('-'))
    except:
        year, month = datetime.now().year, datetime.now().month

    # Generate CSV content
    csv_content = create_attendance_csv(dept_id, year, month, report_type)

    # Create file-like object
    output = io.BytesIO()
    output.write(csv_content.encode('utf-8'))
    output.seek(0)

    # Department names for filename
    dept_names = {
        '1': 'CSE',
        '2': 'ECE',
        '3': 'ME'
    }

    dept_name = dept_names.get(str(dept_id), 'Unknown')
    period_str = f"{month_name[month]}_{year}" if report_type == 'monthly' else f"Week_{year}_{month:02d}"
    filename = f"Attendance_{dept_name}_{report_type.capitalize()}_{period_str}.csv"

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )


@faculty_bp.route("/dashboard")
def fdashboard():
    """Faculty Dashboard with timetable and proxy requests"""
    # Today's Timetable Mock Data
    today = datetime.now().strftime('%A').upper()[:3]
    timetable = [
        {
            'timetable_id': 1,
            'subject_name': 'Web Technologies',
            'subject_code': 'CS301',
            'division_name': 'CSE-A',
            'start_time': '09:00 AM',
            'end_time': '10:00 AM',
            'room_no': '401',
            'is_completed': True
        },
        {
            'timetable_id': 2,
            'subject_name': 'Database Management',
            'subject_code': 'CS302',
            'division_name': 'CSE-B',
            'start_time': '10:00 AM',
            'end_time': '11:00 AM',
            'room_no': '402',
            'is_completed': False
        },
        {
            'timetable_id': 3,
            'subject_name': 'Operating Systems',
            'subject_code': 'CS303',
            'division_name': 'CSE-A',
            'start_time': '11:15 AM',
            'end_time': '12:15 PM',
            'room_no': '401',
            'is_completed': False
        }
    ]

    # Proxy Lectures Mock Data
    proxies = [
        {
            'proxy_id': 1,
            'subject_name': 'Data Structures',
            'division_name': 'ECE-A',
            'lecture_date': datetime.now().strftime('%Y-%m-%d'),
            'lecture_no': 4,
            'original_faculty': 'Dr. Rajesh Kumar',
            'status': 'PENDING'
        }
    ]

    stats = {
        'total_lectures': 4,
        'completed': 1,
        'remaining': 3,
        'proxy_pending': 1
    }

    return render_template("faculty/dashboard.html",
                         title="Faculty Dashboard",
                         user=mock_users['faculty'],
                         faculty=mock_faculty,
                         department=mock_department,
                         teaching_stats=mock_teaching_stats,
                         timetable=timetable,
                         proxies=proxies,
                         stats=stats,
                         datetime=datetime)


@faculty_bp.route("/attendance")
def faculty_attendance():
    """Faculty Attendance Management"""
    divisions = [
        {'div_id': 1, 'division_name': 'CSE-A', 'subjects': [{'id': 1, 'name': 'Web Technologies'}, {'id': 2, 'name': 'Operating Systems'}]},
        {'div_id': 2, 'division_name': 'CSE-B', 'subjects': [{'id': 3, 'name': 'Database Management'}]}
    ]
    return render_template("faculty/attendance.html",
                         title="Attendance Management",
                         user=mock_users['faculty'],
                         divisions=divisions,
                         datetime=datetime)


@faculty_bp.route("/analytics")
def faculty_analytics():
    """Faculty Attendance Analytics"""
    class_wise_attendance = [
        {'division': 'CSE-A', 'percentage': 85},
        {'division': 'CSE-B', 'percentage': 78},
        {'division': 'ECE-A', 'percentage': 92},
    ]
    day_wise_attendance = [
        {'day': 'Monday', 'percentage': 88},
        {'day': 'Tuesday', 'percentage': 82},
        {'day': 'Wednesday', 'percentage': 85},
        {'day': 'Thursday', 'percentage': 80},
        {'day': 'Friday', 'percentage': 84},
        {'day': 'Saturday', 'percentage': 75},
    ]
    return render_template("faculty/analytics.html",
                         title="Attendance Analytics",
                         user=mock_users['faculty'],
                         class_stats=class_wise_attendance,
                         day_stats=day_wise_attendance)


@faculty_bp.route("/reports")
def faculty_reports():
    """Faculty Attendance Reports"""
    students = [
        {'id': 1, 'roll_no': '101', 'name': 'Raj Kumar', 'attendance': 92},
        {'id': 2, 'roll_no': '102', 'name': 'Priya Singh', 'attendance': 88},
        {'id': 3, 'roll_no': '103', 'name': 'Amit Verma', 'attendance': 75},
    ]
    return render_template("faculty/reports.html",
                         title="Attendance Reports",
                         user=mock_users['faculty'],
                         students=students,
                         datetime=datetime)


@faculty_bp.route("/timetable")
def faculty_timetable():
    """Faculty Weekly Timetable"""
    return render_template("faculty/timetable.html",
                         title="Weekly Timetable",
                         user=mock_users['faculty'])


@faculty_bp.route("/profile")
def faculty_profile():
    """Faculty Profile"""
    return render_template("faculty/profile.html",
                         title="Faculty Profile",
                         user=mock_users['faculty'],
                         faculty=mock_faculty,
                         college=mock_college,
                         department=mock_department,
                         teaching_stats=mock_teaching_stats,
                         datetime=datetime)


# ==================== HELPER FUNCTIONS FOR REPORT GENERATION ====================

def generate_sample_attendance_data(dept_id, year, month, report_type):
    """Generate sample attendance data for students in a department"""

    # Department to students mapping
    dept_students = {
        '1': [  # CSE Department
            {'roll_no': '101', 'name': 'Raj Kumar', 'enrollment': 'EN2023001'},
            {'roll_no': '102', 'name': 'Priya Singh', 'enrollment': 'EN2023002'},
            {'roll_no': '103', 'name': 'Amit Verma', 'enrollment': 'EN2023003'},
            {'roll_no': '104', 'name': 'Anjali Sharma', 'enrollment': 'EN2023004'},
            {'roll_no': '105', 'name': 'Rohan Patel', 'enrollment': 'EN2023005'},
        ],
        '2': [  # ECE Department
            {'roll_no': '201', 'name': 'Neha Gupta', 'enrollment': 'EN2023006'},
            {'roll_no': '202', 'name': 'Vikram Singh', 'enrollment': 'EN2023007'},
            {'roll_no': '203', 'name': 'Sakshi Kumar', 'enrollment': 'EN2023008'},
            {'roll_no': '204', 'name': 'Arjun Nair', 'enrollment': 'EN2023009'},
        ],
        '3': [  # ME Department
            {'roll_no': '301', 'name': 'Deepak Verma', 'enrollment': 'EN2023010'},
            {'roll_no': '302', 'name': 'Kavya Reddy', 'enrollment': 'EN2023011'},
            {'roll_no': '303', 'name': 'Nikhil Sharma', 'enrollment': 'EN2023012'},
        ]
    }

    students = dept_students.get(str(dept_id), [])

    # Get calendar for the month
    if report_type == 'monthly':
        cal = monthcalendar(year, month)
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, cal[-1][-1])
    else:  # weekly
        today = datetime(year, month, 1)
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)

    data = []
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday to Friday
            for student in students:
                is_present = random.random() < 0.85

                data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'roll_no': student['roll_no'],
                    'name': student['name'],
                    'enrollment': student['enrollment'],
                    'status': 'PRESENT' if is_present else 'ABSENT'
                })

        current_date += timedelta(days=1)

    return data, students


def create_attendance_csv(dept_id, year, month, report_type):
    """Create CSV file for attendance report"""

    attendance_data, students = generate_sample_attendance_data(dept_id, year, month, report_type)

    # Calculate summary stats
    summary = {}
    for student in students:
        roll = student['roll_no']
        student_records = [r for r in attendance_data if r['roll_no'] == roll]
        total = len(student_records)
        present = len([r for r in student_records if r['status'] == 'PRESENT'])
        percentage = (present / total * 100) if total > 0 else 0

        summary[roll] = {
            'name': student['name'],
            'enrollment': student['enrollment'],
            'total': total,
            'present': present,
            'absent': total - present,
            'percentage': round(percentage, 2)
        }

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    dept_names = {
        '1': 'Computer Science & Engineering',
        '2': 'Electronics Engineering',
        '3': 'Mechanical Engineering'
    }

    period_type = 'Monthly' if report_type == 'monthly' else 'Weekly'
    period_str = f"{month_name[month]} {year}" if report_type == 'monthly' else f"Week of {(datetime(year, month, 1) - timedelta(days=(datetime(year, month, 1).weekday()))).strftime('%Y-%m-%d')}"

    writer.writerow(['ATTENDANCE REPORT'])
    writer.writerow([f"{period_type} Report - {period_str}"])
    writer.writerow([f"Department: {dept_names.get(str(dept_id), 'Unknown')}"])
    writer.writerow([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
    writer.writerow([])

    # Summary Table
    writer.writerow(['STUDENT ATTENDANCE SUMMARY'])
    writer.writerow(['Roll No', 'Name', 'Enrollment No', 'Total Lectures', 'Present', 'Absent', 'Percentage', 'Status'])

    for roll_no, data in summary.items():
        status = 'ELIGIBLE' if data['percentage'] >= 75 else 'DE-BARRED'
        writer.writerow([
            roll_no,
            data['name'],
            data['enrollment'],
            data['total'],
            data['present'],
            data['absent'],
            f"{data['percentage']}%",
            status
        ])

    writer.writerow([])
    writer.writerow(['DETAILED DAILY ATTENDANCE'])
    writer.writerow(['Date', 'Roll No', 'Name', 'Status'])

    for record in sorted(attendance_data, key=lambda x: (x['date'], x['roll_no'])):
        writer.writerow([
            record['date'],
            record['roll_no'],
            record['name'],
            record['status']
        ])

    # Convert to bytes
    output.seek(0)
    return output.getvalue()


@faculty_bp.route("/download-report")
def download_report():
    """Download attendance report as CSV"""

    report_type = request.args.get('type', 'monthly')
    dept_id = request.args.get('dept', '1')
    month_str = request.args.get('month', datetime.now().strftime('%Y-%m'))

    try:
        year, month = map(int, month_str.split('-'))
    except:
        year, month = datetime.now().year, datetime.now().month

    # Generate CSV content
    csv_content = create_attendance_csv(dept_id, year, month, report_type)

    # Create file-like object
    output = io.BytesIO()
    output.write(csv_content.encode('utf-8'))
    output.seek(0)

    # Department names for filename
    dept_names = {
        '1': 'CSE',
        '2': 'ECE',
        '3': 'ME'
    }

    dept_name = dept_names.get(str(dept_id), 'Unknown')
    period_str = f"{month_name[month]}_{year}" if report_type == 'monthly' else f"Week_{year}_{month:02d}"
    filename = f"Attendance_{dept_name}_{report_type.capitalize()}_{period_str}.csv"

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )
