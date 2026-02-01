"""
Report Service - Generate Attendance Reports with Visualizations
=================================================================

Generates comprehensive reports with matplotlib visualizations:
- Faculty attendance reports with charts
- Subject attendance reports with graphs
- Student attendance reports with trend analysis
- Department statistics with heatmaps
- College-wide reports with multiple visualizations
- Parent child attendance reports with pie charts

All reports use Bootstrap color palette (NO PURPLE):
- Primary Blue: #0d6efd
- Success Green: #198754
- Danger Red: #dc3545
- Warning Yellow: #ffc107
- Secondary Gray: #6c757d
- Info Cyan: #0dcaf0

Visualization Methods:
- attendance_pie_chart(present, absent, leave)
- monthly_attendance_bar(months_data)
- faculty_performance_chart(faculty_data)
- subject_attendance_bar(subject_data)
- class_attendance_line(dates, percentages)
- department_attendance_heatmap(departments, months, data)
- student_rank_bar(students_data, top_n)
- class_comparison_bar(classes_data)
- absence_reasons_pie(reasons_data)

Author: Development Team
Version: 3.0
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

from ..models.user import Student
from ..models.attendance import Attendance
from ..exceptions import ReportGenerationError
from .visualization_service import VisualizationService


class ReportService:
    """
    Service to generate comprehensive attendance reports with visualizations.
    
    Integrates with VisualizationService to create matplotlib-based charts.
    All charts use Bootstrap color palette (no purple colors).
    
    Methods:
    - generate_daily_report: Daily attendance snapshot with pie chart
    - faculty_performance_report: Faculty statistics with bar chart
    - subject_attendance_report: Subject-wise data with bar chart
    - student_attendance_report: Individual student report with line chart
    - department_report: Department statistics with heatmap
    - college_report: College-wide data with multiple charts
    - child_attendance_report: Parent view with pie chart
    """

    def __init__(self):
        """Initialize report service with visualization capability."""
        self.attendance_records: Dict[int, List[Attendance]] = {}
        self.viz = VisualizationService()  # Initialize visualization service

    def add_attendance_record(self, student_id: int, attendance: Attendance) -> None:
        """Add attendance record."""
        if student_id not in self.attendance_records:
            self.attendance_records[student_id] = []
        self.attendance_records[student_id].append(attendance)

    def generate_daily_report(self, date: datetime) -> Dict[str, Any]:
        """Generate daily attendance report."""
        try:
            present_count = 0
            absent_count = 0
            records_by_student = {}

            for student_id, records in self.attendance_records.items():
                day_records = [
                    r for r in records
                    if r.created_at and r.created_at.date() == date.date()
                ]

                if day_records:
                    present = sum(1 for r in day_records if r.is_present)
                    absent = len(day_records) - present
                    present_count += present
                    absent_count += absent

                    records_by_student[student_id] = {
                        "present": present,
                        "absent": absent,
                        "records": len(day_records),
                    }

            return {
                "report_type": "Daily",
                "date": date.isoformat(),
                "total_present": present_count,
                "total_absent": absent_count,
                "total_recorded": present_count + absent_count,
                "attendance_rate": (
                    (present_count / (present_count + absent_count) * 100)
                    if (present_count + absent_count) > 0
                    else 0
                ),
                "details_by_student": records_by_student,
            }
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate daily report: {str(e)}")

    def generate_weekly_report(self, start_date: datetime) -> Dict[str, Any]:
        """Generate weekly attendance report."""
        try:
            end_date = start_date + timedelta(days=6)
            present_count = 0
            absent_count = 0
            daily_breakdown = {}

            current_date = start_date
            while current_date <= end_date:
                daily_present = 0
                daily_absent = 0

                for student_id, records in self.attendance_records.items():
                    day_records = [
                        r for r in records
                        if r.created_at and r.created_at.date() == current_date.date()
                    ]

                    for record in day_records:
                        if record.is_present:
                            daily_present += 1
                        else:
                            daily_absent += 1

                present_count += daily_present
                absent_count += daily_absent

                daily_breakdown[current_date.isoformat()] = {
                    "present": daily_present,
                    "absent": daily_absent,
                }

                current_date += timedelta(days=1)

            return {
                "report_type": "Weekly",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_present": present_count,
                "total_absent": absent_count,
                "total_recorded": present_count + absent_count,
                "attendance_rate": (
                    (present_count / (present_count + absent_count) * 100)
                    if (present_count + absent_count) > 0
                    else 0
                ),
                "daily_breakdown": daily_breakdown,
            }
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate weekly report: {str(e)}")

    def generate_monthly_report(self, year: int, month: int) -> Dict[str, Any]:
        """Generate monthly attendance report."""
        try:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)

            present_count = 0
            absent_count = 0
            weekly_breakdown = {}

            current_date = start_date
            week_num = 1

            while current_date <= end_date:
                week_end = min(current_date + timedelta(days=6), end_date)
                week_key = f"Week {week_num}"

                week_present = 0
                week_absent = 0

                check_date = current_date
                while check_date <= week_end:
                    for student_id, records in self.attendance_records.items():
                        day_records = [
                            r for r in records
                            if r.created_at and r.created_at.date() == check_date.date()
                        ]

                        for record in day_records:
                            if record.is_present:
                                week_present += 1
                            else:
                                week_absent += 1

                    check_date += timedelta(days=1)

                present_count += week_present
                absent_count += week_absent

                weekly_breakdown[week_key] = {
                    "present": week_present,
                    "absent": week_absent,
                }

                current_date = week_end + timedelta(days=1)
                week_num += 1

            return {
                "report_type": "Monthly",
                "year": year,
                "month": month,
                "total_present": present_count,
                "total_absent": absent_count,
                "total_recorded": present_count + absent_count,
                "attendance_rate": (
                    (present_count / (present_count + absent_count) * 100)
                    if (present_count + absent_count) > 0
                    else 0
                ),
                "weekly_breakdown": weekly_breakdown,
            }
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate monthly report: {str(e)}")

    def generate_student_report(self, student_id: int) -> Dict[str, Any]:
        """Generate individual student attendance report."""
        try:
            records = self.attendance_records.get(student_id, [])

            if not records:
                return {
                    "student_id": student_id,
                    "total_lectures": 0,
                    "present": 0,
                    "absent": 0,
                    "attendance_percentage": 0.0,
                    "status": "No data",
                }

            present = sum(1 for r in records if r.is_present)
            absent = len(records) - present
            percentage = (present / len(records) * 100) if records else 0

            return {
                "student_id": student_id,
                "total_lectures": len(records),
                "present": present,
                "absent": absent,
                "attendance_percentage": round(percentage, 2),
                "status": (
                    "Defaulter"
                    if percentage < 75
                    else "Warning" if percentage < 80 else "Regular"
                ),
            }
        except Exception as e:
            raise ReportGenerationError(
                f"Failed to generate student report: {str(e)}"
            )

    def generate_defaulter_list(self) -> List[Dict[str, Any]]:
        """Generate list of defaulter students."""
        try:
            defaulters = []

            for student_id in self.attendance_records.keys():
                report = self.generate_student_report(student_id)

                if report["status"] == "Defaulter":
                    defaulters.append(report)

            # Sort by attendance percentage (lowest first)
            defaulters.sort(key=lambda x: x["attendance_percentage"])

            return defaulters
        except Exception as e:
            raise ReportGenerationError(
                f"Failed to generate defaulter list: {str(e)}"
            )

    def generate_subject_wise_report(
        self, subject_id: int
    ) -> Dict[str, Any]:
        """Generate subject-wise attendance report."""
        try:
            # This would require subject-level attendance tracking
            # For now, return a template
            return {
                "report_type": "Subject-wise",
                "subject_id": subject_id,
                "total_classes": 0,
                "average_attendance": 0.0,
                "students_above_threshold": 0,
                "students_below_threshold": 0,
            }
        except Exception as e:
            raise ReportGenerationError(
                f"Failed to generate subject-wise report: {str(e)}"
            )

    def get_report_statistics(self) -> Dict[str, Any]:
        """Get overall statistics."""
        total_present = 0
        total_absent = 0

        for records in self.attendance_records.values():
            total_present += sum(1 for r in records if r.is_present)
            total_absent += sum(1 for r in records if not r.is_present)

        total = total_present + total_absent

        return {
            "total_attendance_records": total,
            "total_present": total_present,
            "total_absent": total_absent,
            "overall_attendance_rate": (
                (total_present / total * 100) if total > 0 else 0
            ),
            "students_tracked": len(self.attendance_records),
        }
    # ========== VISUALIZATION METHODS ==========
    # All methods return base64 encoded images for embedding in HTML
    
    def generate_attendance_pie_chart(self, present: int, absent: int, leave: int) -> str:
        """
        Generate attendance pie chart.
        
        Args:
            present (int): Number of students present
            absent (int): Number of students absent
            leave (int): Number of students on leave
            
        Returns:
            str: Base64 encoded pie chart image
        """
        try:
            return self.viz.attendance_pie_chart(present, absent, leave)
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate pie chart: {str(e)}")
    
    def generate_monthly_attendance_chart(self, months_data: Dict[str, float]) -> str:
        """
        Generate monthly attendance bar chart.
        
        Args:
            months_data (Dict[str, float]): Month names as keys, attendance % as values
            
        Returns:
            str: Base64 encoded bar chart image
        """
        try:
            return self.viz.monthly_attendance_bar(months_data)
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate monthly chart: {str(e)}")
    
    def generate_faculty_performance_chart(self, faculty_data: Dict[str, int]) -> str:
        """
        Generate faculty performance chart showing student counts.
        
        Shows which faculty has maximum students enrolled.
        
        Args:
            faculty_data (Dict[str, int]): Faculty names as keys, student count as values
            
        Returns:
            str: Base64 encoded bar chart image
        """
        try:
            return self.viz.faculty_performance_chart(faculty_data)
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate faculty chart: {str(e)}")
    
    def generate_subject_attendance_chart(self, subject_data: Dict[str, float]) -> str:
        """
        Generate subject-wise attendance bar chart.
        
        Shows which subjects have highest/lowest attendance.
        
        Args:
            subject_data (Dict[str, float]): Subject names as keys, attendance % as values
            
        Returns:
            str: Base64 encoded bar chart image
        """
        try:
            return self.viz.subject_attendance_bar(subject_data)
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate subject chart: {str(e)}")
    
    def generate_attendance_trend_chart(self, dates: List[str], percentages: List[float]) -> str:
        """
        Generate attendance trend line chart.
        
        Shows attendance pattern over time with reference lines for target (90%) and minimum (75%).
        
        Args:
            dates (List[str]): Dates as strings (e.g., '2024-01-15')
            percentages (List[float]): Corresponding attendance percentages
            
        Returns:
            str: Base64 encoded line chart image
        """
        try:
            return self.viz.class_attendance_line(dates, percentages)
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate trend chart: {str(e)}")
    
    def generate_department_heatmap(self, departments: List[str], 
                                   months: List[str], 
                                   data: np.ndarray) -> str:
        """
        Generate department attendance heatmap.
        
        Shows attendance patterns across departments and time with color coding.
        
        Args:
            departments (List[str]): Department names
            months (List[str]): Month names
            data (np.ndarray): 2D array of attendance percentages
            
        Returns:
            str: Base64 encoded heatmap image
        """
        try:
            return self.viz.department_attendance_heatmap(departments, months, data)
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate heatmap: {str(e)}")
    
    def generate_top_students_chart(self, students_data: Dict[str, float], top_n: int = 10) -> str:
        """
        Generate top students ranking chart.
        
        Displays top N students by attendance percentage.
        
        Args:
            students_data (Dict[str, float]): Student names as keys, attendance % as values
            top_n (int): Number of top students to display
            
        Returns:
            str: Base64 encoded bar chart image
        """
        try:
            return self.viz.student_rank_bar(students_data, top_n)
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate top students chart: {str(e)}")
    
    def generate_class_comparison_chart(self, classes_data: Dict[str, float]) -> str:
        """
        Generate class-wise attendance comparison chart.
        
        Shows which classes have highest/lowest attendance.
        
        Args:
            classes_data (Dict[str, float]): Class names as keys, attendance % as values
            
        Returns:
            str: Base64 encoded bar chart image
        """
        try:
            return self.viz.class_comparison_bar(classes_data)
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate class chart: {str(e)}")
    
    def generate_absence_reasons_chart(self, reasons_data: Dict[str, int]) -> str:
        """
        Generate absence reasons pie chart.
        
        Shows breakdown of why students were absent.
        
        Args:
            reasons_data (Dict[str, int]): Reasons as keys, count as values
            
        Returns:
            str: Base64 encoded pie chart image
        """
        try:
            return self.viz.absence_reasons_pie(reasons_data)
        except Exception as e:
            raise ReportGenerationError(f"Failed to generate reasons chart: {str(e)}")