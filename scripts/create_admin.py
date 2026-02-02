#!/usr/bin/env python3
"""
Script to create the first admin user.
"""

import os
import sys
import getpass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash
from attendance_system.db_manager import create_connection


def create_admin_user(name, email, password, mobile, college_id):
    """Create an admin user."""
    conn = create_connection()
    if not conn:
        print("❌ Could not connect to database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Get ADMIN role_id (case-insensitive)
        cursor.execute("SELECT role_id FROM role WHERE UPPER(role_name) = 'ADMIN'")
        result = cursor.fetchone()
        if not result:
            print("❌ Admin role not found in database. Run scripts/seed_initial_data.py first.")
            return False
        
        role_id = result[0]
        
        # Check if email already exists
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"❌ User with email {email} already exists")
            cursor.close()
            conn.close()
            return False
        
        # Create admin user with werkzeug password hashing
        password_hash = generate_password_hash(password)
        cursor.execute(
            """INSERT INTO users 
               (college_id, name, email, password_hash, mobile, role_id, is_approved) 
               VALUES (%s, %s, %s, %s, %s, %s, 1)""",
            (college_id, name, email, password_hash, mobile, role_id)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print()
        print("=" * 60)
        print("✓ Admin user created successfully!")
        print("=" * 60)
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Mobile: {mobile}")
        print(f"Role: ADMIN")
        print()
        print("You can now login with these credentials.")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution."""
    print("=" * 60)
    print("Create Admin User")
    print("=" * 60)
    print()
    
    # First, show available colleges
    try:
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT college_id, college_name FROM college")
        colleges = cursor.fetchall()
        
        if not colleges:
            print("❌ No colleges found in database.")
            print("   Run scripts/seed_initial_data.py first to add colleges.")
            return False
        
        print("Available Colleges:")
        for college in colleges:
            print(f"  [{college['college_id']}] {college['college_name']}")
        print()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return False
    
    # Get user input
    name = input("Admin Name: ").strip()
    email = input("Admin Email: ").strip()
    mobile = input("Mobile Number: ").strip()
    college_id = input(f"College ID (1-{len(colleges)}): ").strip()
    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")
    
    if not all([name, email, mobile, college_id, password]):
        print("❌ All fields are required")
        return False
    
    if password != confirm_password:
        print("❌ Passwords do not match")
        return False
    
    if len(password) < 8:
        print("❌ Password must be at least 8 characters")
        return False
    
    try:
        college_id = int(college_id)
    except ValueError:
        print("❌ Invalid college ID")
        return False
    
    # Create admin
    return create_admin_user(name, email, password, mobile, college_id)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
