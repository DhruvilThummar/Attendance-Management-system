"""
Database Seeding Script
=======================

This script populates the database with initial lookup data required
for the attendance management system to function properly.

Run this after creating the database schema.

Usage:
    python scripts/seed_initial_data.py
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from attendance_system.db_manager import create_connection


def seed_database():
    """Seed the database with initial lookup data."""
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        print("Starting database seeding...")
        
        # 1. Seed Roles
        print("\n1. Seeding roles...")
        roles = [
            ('Admin',),
            ('HOD',),
            ('Faculty',),
            ('Student',),
            ('Parent',)
        ]
        
        cursor.execute("SELECT COUNT(*) FROM role")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO role (role_name) VALUES (%s)",
                roles
            )
            print(f"   ✓ Inserted {len(roles)} roles")
        else:
            print("   ⚠ Roles already exist, skipping")
        
        # 2. Seed Attendance Statuses
        print("\n2. Seeding attendance statuses...")
        statuses = [
            ('PRESENT',),
            ('ABSENT',)
        ]
        
        cursor.execute("SELECT COUNT(*) FROM attendance_status")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO attendance_status (status_name) VALUES (%s)",
                statuses
            )
            print(f"   ✓ Inserted {len(statuses)} attendance statuses")
        else:
            print("   ⚠ Attendance statuses already exist, skipping")
        
        # 3. Seed Colleges
        print("\n3. Seeding colleges...")
        colleges = [
            ('Sample Engineering College', 'SEC', '123 College Street, City', '1234567890', 'info@sec.edu'),
            ('Tech Institute', 'TI', '456 Tech Avenue, City', '0987654321', 'contact@techinst.edu')
        ]
        
        cursor.execute("SELECT COUNT(*) FROM college")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """INSERT INTO college (college_name, college_code, address, phone, email) 
                   VALUES (%s, %s, %s, %s, %s)""",
                colleges
            )
            print(f"   ✓ Inserted {len(colleges)} colleges")
        else:
            print("   ⚠ Colleges already exist, skipping")
        
        # Get first college_id for departments
        cursor.execute("SELECT college_id FROM college LIMIT 1")
        college_id = cursor.fetchone()[0]
        
        # 4. Seed Departments
        print("\n4. Seeding departments...")
        departments = [
            (college_id, 'Computer Engineering'),
            (college_id, 'Information Technology'),
            (college_id, 'Electronics and Telecommunication'),
            (college_id, 'Mechanical Engineering'),
            (college_id, 'Civil Engineering'),
            (college_id, 'Electrical Engineering')
        ]
        
        cursor.execute("SELECT COUNT(*) FROM department")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO department (college_id, dept_name) VALUES (%s, %s)",
                departments
            )
            print(f"   ✓ Inserted {len(departments)} departments")
        else:
            print("   ⚠ Departments already exist, skipping")
        
        # 5. Seed Divisions
        print("\n5. Seeding divisions...")
        divisions = [
            ('A',),
            ('B',),
            ('C',),
            ('D',)
        ]
        
        cursor.execute("SELECT COUNT(*) FROM division")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO division (division_name) VALUES (%s)",
                divisions
            )
            print(f"   ✓ Inserted {len(divisions)} divisions")
        else:
            print("   ⚠ Divisions already exist, skipping")
        
        # 6. Seed Semesters
        print("\n6. Seeding semesters...")
        semesters = [
            ('Semester 1',),
            ('Semester 2',),
            ('Semester 3',),
            ('Semester 4',),
            ('Semester 5',),
            ('Semester 6',),
            ('Semester 7',),
            ('Semester 8',)
        ]
        
        cursor.execute("SELECT COUNT(*) FROM semester")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO semester (semester_name) VALUES (%s)",
                semesters
            )
            print(f"   ✓ Inserted {len(semesters)} semesters")
        else:
            print("   ⚠ Semesters already exist, skipping")
        
        # 7. Seed Sample Subjects
        print("\n7. Seeding sample subjects...")
        
        # Get semester IDs
        cursor.execute("SELECT semester_id FROM semester WHERE semester_name = 'Semester 3'")
        sem3_id = cursor.fetchone()
        
        if sem3_id:
            sem3_id = sem3_id[0]
            subjects = [
                ('CS301', 'Data Structures and Algorithms', sem3_id),
                ('CS302', 'Database Management Systems', sem3_id),
                ('CS303', 'Operating Systems', sem3_id),
                ('CS304', 'Computer Networks', sem3_id),
                ('CS305', 'Software Engineering', sem3_id)
            ]
            
            cursor.execute("SELECT COUNT(*) FROM subject WHERE semester_id = %s", (sem3_id,))
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    "INSERT INTO subject (subject_code, subject_name, semester_id) VALUES (%s, %s, %s)",
                    subjects
                )
                print(f"   ✓ Inserted {len(subjects)} sample subjects for Semester 3")
            else:
                print("   ⚠ Subjects already exist, skipping")
        
        # Commit all changes
        conn.commit()
        
        print("\n" + "="*60)
        print("✓ Database seeding completed successfully!")
        print("="*60)
        
        # Show summary
        print("\nSummary:")
        cursor.execute("SELECT COUNT(*) FROM role")
        print(f"  Roles: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM attendance_status")
        print(f"  Attendance Statuses: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM college")
        print(f"  Colleges: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM department")
        print(f"  Departments: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM division")
        print(f"  Divisions: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM semester")
        print(f"  Semesters: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM subject")
        print(f"  Subjects: {cursor.fetchone()[0]}")
        
        print("\nNext steps:")
        print("1. Create an admin user: python scripts/create_admin.py")
        print("2. Run the application: python -m flask --app attendance_system.app:create_app run")
        print("3. Access at: http://localhost:5000")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n✗ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    seed_database()
