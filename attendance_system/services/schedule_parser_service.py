"""
Service to parse timetable PDFs using pdfplumber.
Extracts schedule data: Day, Time, Subject, Division/Faculty.
"""
from __future__ import annotations
import pdfplumber
import re
from typing import List, Dict, Any

def parse_schedule_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Parses a PDF file to extract timetable entries.
    Assumes a grid format where headers are Days/Times.
    Returns a list of dictionaries:
    [{'day': 'Monday', 'time': '10:00-11:00', 'subject': 'CS101', 'division': 'A'}]
    """
    entries = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            
            for table in tables:
                if not table:
                    continue
                
                # Simple Heuristic:
                # Row 0 usually contains headers (Time slots or Days)
                # Col 0 usually contains the other dimension
                
                headers = [str(h).strip() if h else "" for h in table[0]]
                
                # Check if headers look like Days or Times
                is_day_header = any(d in headers[1:] for d in ["Monday", "Tuesday", "Wednesday"])
                
                for row_idx, row in enumerate(table[1:], start=1):
                    row_label = str(row[0]).strip()
                    
                    for col_idx, cell in enumerate(row[1:], start=1):
                        if not cell:
                            continue
                            
                        # Determine Day and Time based on layout
                        header_label = headers[col_idx]
                        
                        if is_day_header:
                            day = header_label
                            time_slot = row_label
                        else:
                            day = row_label
                            time_slot = header_label
                            
                        # Clean up cell content (Subject / Faculty / Room)
                        # cell text might be "CS101\nProf. X\nRoom 101"
                        lines = cell.split('\n')
                        subject = lines[0].strip()
                        
                        # simple entry
                        entries.append({
                            'day': day,
                            'slot': time_slot,
                            'subject': subject,
                            'raw_text': cell
                        })
                        
    return entries

def save_extracted_schedule(entries: List[Dict[str, Any]], division_id: int):
    """
    Saves parsed entries to the database.
    Requires mapping 'subject' text to actual Subject IDs.
    For this demo, we'll auto-create subjects if missing or match loosely.
    """
    from ..db_manager import execute, fetch_one
    from ..models.subject import Subject
    from ..models.timetable import TimetableEntry
    
    # Clean previous schedule for this division? 
    # execute("DELETE FROM timetable WHERE division_id = %s", (division_id,))
    
    for entry in entries:
        subject_name = entry['subject']
        if not subject_name or len(subject_name) < 2:
            continue
            
        # 1. Find or Create Subject
        # Loosely match code or name
        sub_row = fetch_one("SELECT id FROM subjects WHERE code = %s OR name = %s", (subject_name, subject_name))
        if sub_row:
            sub_id = sub_row[0]
        else:
            # Create new subject stub
            # Assume code is first word if 2 words, else generated
            parts = subject_name.split()
            code = parts[0] if len(parts) > 1 and any(c.isdigit() for c in parts[0]) else f"SUB{hash(subject_name)%1000}"
            execute("INSERT INTO subjects (code, name) VALUES (%s, %s)", (code, subject_name))
            sub_id = fetch_one("SELECT LAST_INSERT_ID()")[0]
            
        # 2. Insert Timetable Entry
        # Defaulting Faculty to ID 1 (Admin/Placeholder) if not parsed
        # In real app, we'd parse "Prof. Name" from cell and lookup faculty
        faculty_id = 1 
        
        # Save
        # TimetableEntry model uses raw SQL now from base.py extraction, or we use execute directly
        execute("""
            INSERT INTO timetable (subject_id, faculty_id, division_id, day, slot)
            VALUES (%s, %s, %s, %s, %s)
        """, (sub_id, faculty_id, division_id, entry['day'], entry['slot']))
        
    return len(entries)
