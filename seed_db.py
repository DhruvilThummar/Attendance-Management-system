"""
Database Seeding Script.
"""
from __future__ import annotations
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from attendance_system.db_manager import execute, create_connection
from attendance_system.models.user import User
from attendance_system.models.student import Student
from attendance_system.models.faculty import Faculty
from attendance_system.models.hod import HOD
from attendance_system.services.search_service import init_bst

def run_schema(schema_path="attendance_system/schema.sql"):
    print("🛠️ Resetting database schema...")
    with open(schema_path, "r") as f:
        schema = f.read()
    
    # Drop existing tables to ensure clean slate
    # Order matters for foreign keys
    tables = ["notifications", "attendance_audit", "attendance", "lectures", "timetable", "hods", "faculties", "students", "subjects", "divisions", "users", "colleges", "academic_calendar"]
    execute("SET FOREIGN_KEY_CHECKS = 0")
    for t in tables:
        execute(f"DROP TABLE IF EXISTS {t}")
    execute("SET FOREIGN_KEY_CHECKS = 1")
    print("🗑️ Old tables dropped.")

    # Execute schema
    # Split by semicolon but handle potential tricky parts? 
    # Since schema is simple, splitting by ';' is fine usually.
    commands = schema.split(';')
    for cmd in commands:
        if cmd.strip():
            execute(cmd)
            
    print("✅ Tables created from schema.")

def seed():
    print("🌱 Seeding database...")
    
    # 1. Create College
    execute("INSERT INTO colleges (name) VALUES (%s)", ("LJKU Institute of Engineering",))
    college_id = 1
    print(f"Created College: ID {college_id}")

    # 2. Create Global Data (Divisions, Subjects)
    execute("INSERT INTO divisions (college_id, name, semester) VALUES (%s, %s, %s)", (college_id, "Div A", 3))
    execute("INSERT INTO divisions (college_id, name, semester) VALUES (%s, %s, %s)", (college_id, "Div B", 3))
    
    div_a = execute("SELECT id FROM divisions WHERE name='Div A'")[0] # returns tuple (id,) usually via fetchall in backend, but execute returns list of tuples
    # Wait, my execute function in db_manager returns list of tuples for SELECT?
    # db_manager.execute alias run_query returns fetchall() list of tuples.
    # So execute("SELECT..")[0] is the first row (tuple).
    div_a_id = div_a[0]
    
    execute("INSERT INTO subjects (college_id, code, name, branch) VALUES (%s, %s, %s, %s)", (college_id, "CS101", "Python Programming", "Computer Engineering"))
    execute("INSERT INTO subjects (college_id, code, name, branch) VALUES (%s, %s, %s, %s)", (college_id, "CS102", "Web Development", "Computer Engineering"))
    sub_py_row = execute("SELECT id FROM subjects WHERE code='CS101'")[0]
    sub_py_id = sub_py_row[0]
    
    print("Created Divisions and Subjects")

    # 3. Create Users
    
    # Super Admin
    # user logic: email, name, pass, role, is_approved, college_id
    sa = User(email="Admin@edu.com", name="Super Admin", password="AdminPassword123!", role="SuperAdmin", is_approved=True, college_id=college_id)
    sa.save()
    
    # College Admin
    ca = User(email="admin@college.edu", name="College Admin", password="AdminPassword123!", role="CollegeAdmin", is_approved=True, college_id=college_id)
    ca.save()
    
    # HOD
    hod_u = User(email="hod@college.edu", name="Dr. HOD", password="HODPassword123!", role="HOD", is_approved=True, college_id=college_id)
    hod_u.save()
    hod = HOD(user_id=hod_u.id, department_id=101) # Mock dept id
    hod.save()
    
    # Faculty
    fac_u = User(email="faculty@college.edu", name="Ravi Kumar Sharma", password="FacultyPassword123!", role="Faculty", is_approved=True, college_id=college_id)
    fac_u.save()
    fac = Faculty(user_id=fac_u.id, department="Computer Engineering", short_name="RKS", phone_number="9898989898")
    fac.save()
    
    # Student
    stu_u = User(email="student@college.edu", name="Student Name", password="StudentPassword123!", role="Student", is_approved=True, college_id=college_id)
    stu_u.save()
    stu = Student(user_id=stu_u.id, enrollment_no="E2023001", roll_no="101", branch="Computer Engineering", phone_number="9876543210", mentor_name="Prof. Mentor", division_id=div_a_id)
    stu.save()
    
    print("Created Users (SuperAdmin, CollegeAdmin, HOD, Faculty, Student)")
    
    # 4. Timetable
    execute("INSERT INTO timetable (subject_id, faculty_id, division_id, day, slot) VALUES (%s, %s, %s, %s, %s)", 
            (sub_py_id, fac.id, div_a_id, "Monday", "10:00 - 11:00"))
            
    # 5. Generate Lectures
    from attendance_system.services.calendar_service import generate_lectures
    from datetime import date, timedelta
    today = date.today()
    count = generate_lectures(today - timedelta(days=7), today + timedelta(days=7))
    print(f"Generated {count} Lectures")
    
    # Init BST
    try:
        init_bst()
    except Exception as e:
        print(f"BST Init Warning: {e}")
        
    print("✅ Database seeding complete!")

if __name__ == "__main__":
    run_schema()
    seed()
