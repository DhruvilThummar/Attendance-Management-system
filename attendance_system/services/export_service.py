"""
Attendance Export Service

Handles exporting compiled attendance reports to CSV and PDF formats.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import csv
import io

from sqlalchemy import bindparam, text
from sqlalchemy.orm import aliased

from models.attendance import Attendance
from models.division import Division
from models.faculty import Faculty
from models.student import Student
from models.subject import Subject, Semester
from models.timetable import Timetable
from models.user import User, db


SUBJECT_GROUPS = {
    "DE": ["DE"],
    "FSD1": ["FSD-1", "FSD1"],
    "PS": ["PS"],
}

WEEK_LABEL = "WEEK-12"


class ExportService:
    """Service for exporting compiled attendance data"""

    @staticmethod
    def _get_subject_ids_by_key() -> Dict[str, List[int]]:
        """Get subject IDs grouped by subject key"""
        subject_ids_by_key: Dict[str, List[int]] = {}
        for key, codes in SUBJECT_GROUPS.items():
            subject_ids = [
                s.subject_id
                for s in Subject.query.filter(Subject.subject_code.in_(codes)).all()
            ]
            subject_ids_by_key[key] = subject_ids
        return subject_ids_by_key

    @staticmethod
    def _count_lectures_by_division(subject_ids: List[int]) -> Dict[int, int]:
        """Count total lectures per division for given subjects"""
        if not subject_ids:
            return {}

        stmt = text(
            """
            SELECT t.division_id AS division_id, COUNT(l.lecture_id) AS total
            FROM lecture l
            JOIN timetable t ON t.timetable_id = l.timetable_id
            WHERE t.subject_id IN :subject_ids
            GROUP BY t.division_id
            """
        ).bindparams(bindparam("subject_ids", expanding=True))

        results = db.session.execute(stmt, {"subject_ids": subject_ids}).fetchall()
        return {int(row.division_id): int(row.total) for row in results}

    @staticmethod
    def _count_attended_by_student(subject_ids: List[int]) -> Dict[int, int]:
        """Count attended lectures per student for given subjects"""
        if not subject_ids:
            return {}

        stmt = text(
            """
            SELECT a.student_id AS student_id, COUNT(a.attendance_id) AS attended
            FROM attendance a
            JOIN lecture l ON l.lecture_id = a.lecture_id
            JOIN timetable t ON t.timetable_id = l.timetable_id
            WHERE a.status_id = 1 AND t.subject_id IN :subject_ids
            GROUP BY a.student_id
            """
        ).bindparams(bindparam("subject_ids", expanding=True))

        results = db.session.execute(stmt, {"subject_ids": subject_ids}).fetchall()
        return {int(row.student_id): int(row.attended) for row in results}

    @staticmethod
    def _percent(attended: int, total: int) -> float:
        """Calculate percentage"""
        if total <= 0:
            return 0.0
        return round((attended / total) * 100, 2)

    @staticmethod
    def _get_semester_header() -> str:
        """Get semester header for report"""
        semester = (
            Semester.query.filter(Semester.semester_no == 3)
            .order_by(Semester.academic_year.desc())
            .first()
        )
        year = "2025"
        if semester and semester.academic_year:
            year = semester.academic_year.split("-")[-1]
        return f"SY (CE/IT-1) Sem-III {year} Compiled Attendance"

    @staticmethod
    def build_rows() -> Tuple[List[str], List[List[str]]]:
        """Build header and data rows for attendance report"""
        subject_ids_by_key = ExportService._get_subject_ids_by_key()

        total_lectures_by_div_key: Dict[Tuple[int, str], int] = {}
        attended_by_student_key: Dict[Tuple[int, str], int] = {}

        for key, subject_ids in subject_ids_by_key.items():
            totals = ExportService._count_lectures_by_division(subject_ids)
            for division_id, total in totals.items():
                total_lectures_by_div_key[(division_id, key)] = total

            attended = ExportService._count_attended_by_student(subject_ids)
            for student_id, count in attended.items():
                attended_by_student_key[(student_id, key)] = count

        mentor_user = aliased(User)

        students = (
            db.session.query(Student, User, Division, Semester, Faculty, mentor_user)
            .join(User, Student.user_id == User.user_id)
            .join(Division, Student.division_id == Division.division_id)
            .join(Semester, Student.semester_id == Semester.semester_id)
            .outerjoin(Faculty, Student.mentor_id == Faculty.faculty_id)
            .outerjoin(mentor_user, Faculty.user_id == mentor_user.user_id)
            .order_by(Division.division_name, Student.roll_no)
            .all()
        )

        header = [
            "Roll no.",
            "Div",
            "Branch",
            "Enrollment No",
            "Name",
            "Mentor Name",
        ]

        for key in SUBJECT_GROUPS:
            header.extend([
                f"{key} Total Attended",
                f"{key} Total Lecture",
                f"{key} Overall %",
            ])

        header.extend([
            "OVERALL Total Attended",
            "OVERALL Total Lecture",
            "OVERALL %",
        ])

        rows: List[List[str]] = []

        for student, user, division, semester, faculty, mentor in students:
            mentor_name = mentor.name if mentor else ""
            branch = division.department.dept_name if division.department else ""

            row = [
                str(student.roll_no),
                division.division_name,
                branch,
                student.enrollment_no,
                user.name,
                mentor_name,
            ]

            overall_attended = 0
            overall_total = 0

            for key in SUBJECT_GROUPS:
                attended = attended_by_student_key.get((student.student_id, key), 0)
                total = total_lectures_by_div_key.get((division.division_id, key), 0)
                overall_attended += attended
                overall_total += total
                row.extend([
                    str(attended),
                    str(total),
                    f"{ExportService._percent(attended, total):.2f}",
                ])

            row.extend([
                str(overall_attended),
                str(overall_total),
                f"{ExportService._percent(overall_attended, overall_total):.2f}",
            ])

            rows.append(row)

        return header, rows

    @staticmethod
    def export_csv() -> io.StringIO:
        """Generate CSV content for attendance report"""
        header, rows = ExportService.build_rows()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        title_row = [ExportService._get_semester_header()]
        sub_title = [f"Compiled Attendance of {WEEK_LABEL}"]
        sub_heading = [f"Subjectwise Compiled Attendance upto {WEEK_LABEL}"]
        
        writer.writerow(title_row)
        writer.writerow(sub_title)
        writer.writerow(sub_heading)
        writer.writerow([])
        writer.writerow(header)
        writer.writerows(rows)
        
        output.seek(0)
        return output

    @staticmethod
    def export_pdf() -> io.BytesIO:
        """Generate PDF content for attendance report"""
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
        except ImportError as exc:
            raise RuntimeError(
                "reportlab is required for PDF export. Install it with: pip install reportlab"
            ) from exc

        header, rows = ExportService.build_rows()
        
        output = io.BytesIO()
        
        styles = getSampleStyleSheet()
        story: List[object] = []

        story.append(Paragraph(ExportService._get_semester_header(), styles["Title"]))
        story.append(Paragraph(f"Compiled Attendance of {WEEK_LABEL}", styles["Heading3"]))
        story.append(Paragraph(f"Subjectwise Compiled Attendance upto {WEEK_LABEL}", styles["Heading4"]))
        story.append(Spacer(1, 0.2 * inch))

        table_data = [header] + rows

        table = Table(table_data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]
            )
        )

        story.append(table)

        doc = SimpleDocTemplate(
            output,
            pagesize=A4,
            leftMargin=0.4 * inch,
            rightMargin=0.4 * inch,
            topMargin=0.4 * inch,
            bottomMargin=0.4 * inch,
        )
        doc.build(story)
        
        output.seek(0)
        return output
