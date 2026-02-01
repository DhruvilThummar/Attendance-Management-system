"""Calendar service - Auto-generate lectures from timetable."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Dict, Any

from ..models.lecture import Lecture
from ..models.timetable import Timetable
from ..exceptions import CalendarGenerationError


class AcademicCalendar:
    """Academic calendar with holidays and exam weeks."""

    def __init__(self):
        self.holidays: List[tuple[datetime, str]] = []
        self.exam_weeks: List[tuple[datetime, datetime]] = []

    def add_holiday(self, date: datetime, name: str) -> None:
        """Add a holiday to the calendar."""
        self.holidays.append((date, name))

    def add_exam_week(self, start_date: datetime, end_date: datetime) -> None:
        """Add an exam week (no lectures)."""
        self.exam_weeks.append((start_date, end_date))

    def is_holiday(self, date: datetime) -> bool:
        """Check if a date is a holiday."""
        return any(holiday[0].date() == date.date() for holiday in self.holidays)

    def is_exam_week(self, date: datetime) -> bool:
        """Check if a date is in exam week."""
        date_only = date.date()
        return any(
            start.date() <= date_only <= end.date()
            for start, end in self.exam_weeks
        )

    def get_holidays(self) -> List[tuple[datetime, str]]:
        """Get all holidays."""
        return self.holidays

    def get_exam_weeks(self) -> List[tuple[datetime, datetime]]:
        """Get all exam weeks."""
        return self.exam_weeks


class CalendarService:
    """Service to generate lectures from timetable based on academic calendar."""

    def __init__(self):
        self.academic_calendar = AcademicCalendar()
        self.generated_lectures: List[Lecture] = []

    def set_academic_calendar(self, calendar: AcademicCalendar) -> None:
        """Set the academic calendar."""
        self.academic_calendar = calendar

    def generate_lectures(
        self,
        timetable: Timetable,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Lecture]:
        """Generate lectures for a timetable entry over a date range."""
        if start_date >= end_date:
            raise CalendarGenerationError("Start date must be before end date")

        if not timetable.validate():
            raise CalendarGenerationError("Invalid timetable entry")

        lectures = []
        current_date = start_date

        # DAY_OF_WEEK: 1=Monday to 6=Saturday
        target_day = timetable.day_of_week or 1

        while current_date <= end_date:
            # Monday is 0 in weekday(), so convert: 1(Mon) -> 0, 2(Tue) -> 1, etc.
            current_weekday = current_date.weekday() + 1

            # Check if it's the right day of week
            if current_weekday == target_day:
                # Check if not holiday or exam week
                if not (
                    self.academic_calendar.is_holiday(current_date)
                    or self.academic_calendar.is_exam_week(current_date)
                ):
                    lecture = Lecture(
                        timetable_id=timetable.id,
                        lecture_date=current_date,
                        start_time=timetable.start_time,
                        end_time=timetable.end_time,
                        faculty_id=timetable.faculty_id,
                        subject_id=timetable.subject_id,
                        division_id=timetable.division_id,
                        canceled=False,
                    )
                    lectures.append(lecture)

            current_date += timedelta(days=1)

        self.generated_lectures.extend(lectures)
        return lectures

    def generate_all_lectures(
        self,
        timetables: List[Timetable],
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[int, List[Lecture]]:
        """Generate lectures for all timetable entries."""
        result = {}

        for timetable in timetables:
            try:
                lectures = self.generate_lectures(timetable, start_date, end_date)
                result[timetable.id or 0] = lectures
            except CalendarGenerationError as e:
                result[timetable.id or 0] = []

        return result

    def cancel_lectures_for_date(self, date: datetime, reason: str = "") -> int:
        """Cancel all lectures for a specific date."""
        canceled_count = 0

        for lecture in self.generated_lectures:
            if (
                lecture.lecture_date
                and lecture.lecture_date.date() == date.date()
                and not lecture.canceled
            ):
                lecture.canceled = True
                canceled_count += 1

        return canceled_count

    def get_lectures_between(
        self, start_date: datetime, end_date: datetime
    ) -> List[Lecture]:
        """Get all lectures between two dates."""
        return [
            lecture
            for lecture in self.generated_lectures
            if lecture.lecture_date
            and start_date <= lecture.lecture_date <= end_date
            and not lecture.canceled
        ]

    def get_division_lectures(
        self, division_id: int, start_date: datetime, end_date: datetime
    ) -> List[Lecture]:
        """Get all lectures for a division between two dates."""
        return [
            lecture
            for lecture in self.generated_lectures
            if lecture.division_id == division_id
            and lecture.lecture_date
            and start_date <= lecture.lecture_date <= end_date
            and not lecture.canceled
        ]

    def get_faculty_lectures(
        self, faculty_id: int, start_date: datetime, end_date: datetime
    ) -> List[Lecture]:
        """Get all lectures for a faculty member between two dates."""
        return [
            lecture
            for lecture in self.generated_lectures
            if lecture.faculty_id == faculty_id
            and lecture.lecture_date
            and start_date <= lecture.lecture_date <= end_date
            and not lecture.canceled
        ]

    def get_statistics(self) -> Dict[str, Any]:
        """Get calendar statistics."""
        total_lectures = len(self.generated_lectures)
        active_lectures = sum(1 for l in self.generated_lectures if not l.canceled)
        canceled_lectures = total_lectures - active_lectures

        return {
            "total_lectures": total_lectures,
            "active_lectures": active_lectures,
            "canceled_lectures": canceled_lectures,
            "cancellation_rate": (
                (canceled_lectures / total_lectures * 100)
                if total_lectures > 0
                else 0
            ),
            "holidays_count": len(self.academic_calendar.get_holidays()),
            "exam_weeks_count": len(self.academic_calendar.get_exam_weeks()),
        }
