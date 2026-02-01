#!/usr/bin/env python3
"""
Script to create the first admin user.
"""

import os
import sys
import getpass
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from attendance_system.db_manager import get_connection


def hash_password(password):
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def create_college(cursor, college_name):
    """Create a college and return its ID."""
    cursor.execute(
        "INSERT INTO college (college_name) VALUES (%s)",
        (college_name,)
    )
    return cursor.lastrowid


def create_admin_user(name, email, password, college_name):
    """Create an admin user."""
    conn = get_connection()
    if not conn:
        print("❌ Could not connect to database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create college
        college_id = create_college(cursor, college_name)
        print(f"✓ Created college: {college_name} (ID: {college_id})")
        
        # Get ADMIN role_id
        cursor.execute("SELECT role_id FROM role WHERE role_name = 'ADMIN'")
        result = cursor.fetchone()
        if not result:
            print("❌ ADMIN role not found in database. Run seed_db.py first.")
            return False
        
        role_id = result[0]
        
        # Check if email already exists
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"❌ User with email {email} already exists")
            return False
        
        # Create admin user
        password_hash = hash_password(password)
        cursor.execute(
            """INSERT INTO users 
               (college_id, name, email, password_hash, role_id, is_approved) 
               VALUES (%s, %s, %s, %s, %s, 1)""",
            (college_id, name, email, password_hash, role_id)
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
        print(f"College: {college_name}")
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
    
    # Get user input
    name = input("Admin Name: ").strip()
    email = input("Admin Email: ").strip()
    college_name = input("College Name: ").strip()
    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")
    
    if not all([name, email, college_name, password]):
        print("❌ All fields are required")
        return False
    
    if password != confirm_password:
        print("❌ Passwords do not match")
        return False
    
    if len(password) < 6:
        print("❌ Password must be at least 6 characters")
        return False
    
    # Create admin
    return create_admin_user(name, email, password, college_name)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
