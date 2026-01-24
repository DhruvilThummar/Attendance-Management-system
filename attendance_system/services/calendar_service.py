"""Lecture auto-generation logic."""
from __future__ import annotations
import logging
from datetime import date, timedelta
from typing import List
from ..models.timetable import TimetableEntry
from ..models.lecture import Lecture
from ..db_manager import execute

logger = logging.getLogger(__name__)

def get_day_name(d: date) -> str:
    """Return full day name, e.g., 'Monday'."""
    return d.strftime("%A")

def is_working_day(d: date) -> bool:
    """Check if date is a working day (Mon-Sat, excluding holidays)."""
    # TODO: Integrate with specific Academic Calendar/Holiday table
    if d.weekday() == 6:  # Sunday
        return False
    return True

def generate_lectures(start_date: date, end_date: date) -> int:
    """Generate lectures for the given date range based on timetable."""
    logger.info(f"Generating lectures from {start_date} to {end_date}...")
    
    # 1. Fetch all timetable entries
    timetable_entries = TimetableEntry.get_all()
    # Optimize: Group by day
    schedule_by_day = {}
    for entry in timetable_entries:
        if entry.day:
            day = entry.day.capitalize()
            if day not in schedule_by_day:
                schedule_by_day[day] = []
            schedule_by_day[day].append(entry)

    current_date = start_date
    count = 0
    
    while current_date <= end_date:
        if is_working_day(current_date):
            day_name = get_day_name(current_date)
            entries = schedule_by_day.get(day_name, [])
            
            for entry in entries:
                # Check if lecture already exists to avoid duplicates
                # This could be slow for bulk; optimized query would be better
                exists_query = "SELECT 1 FROM lectures WHERE timetable_id = %s AND date = %s"
                exists = execute(exists_query, (entry.id, current_date.isoformat()))
                
                if not exists:
                    lecture = Lecture(
                        timetable_id=entry.id,
                        date=current_date.isoformat()
                    )
                    lecture.save()
                    count += 1
        
        current_date += timedelta(days=1)
        
    logger.info(f"Generated {count} lectures.")
    return count
