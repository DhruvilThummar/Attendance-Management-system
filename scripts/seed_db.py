#!/usr/bin/env python3
"""
Seed script to initialize the database with schema.sql
"""
from __future__ import annotations

import os
import sys
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def parse_db_url(url):
    """Parse MySQL connection URL."""
    parsed = urlparse(url)
    return {
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 3306,
        'user': parsed.username or 'root',
        'password': parsed.password or '',
        'database': parsed.path.lstrip('/') if parsed.path else 'databse'
    }


def create_database(db_config):
    """Create database if it doesn't exist."""
    try:
        # Connect without database
        conn = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_config['database']}`")
        print(f"✓ Database '{db_config['database']}' ready")
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error creating database: {e}")
        return False


def load_schema(db_config):
    """Load and execute the schema.sql file."""
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "attendance_system",
        "schema.sql"
    )
    
    if not os.path.exists(schema_path):
        print(f"Error: schema.sql not found at {schema_path}")
        return False
    
    print(f"Loading schema from {schema_path}...")
    
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Execute USE database
        cursor.execute(f"USE `{db_config['database']}`")
        
        # Split and execute statements
        statements = []
        current_statement = []
        
        for line in schema_sql.split('\n'):
            line = line.strip()
            # Skip comments and SET commands
            if (not line or line.startswith('--') or line.startswith('/*') or 
                line.startswith('*/') or line.startswith('SET') or 
                line.startswith('START') or line.startswith('COMMIT') or
                line.startswith('/*!')):
                continue
            
            current_statement.append(line)
            
            if line.endswith(';'):
                statement = ' '.join(current_statement)
                statements.append(statement)
                current_statement = []
        
        # Execute each statement
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except Error as e:
                    # Ignore errors for already exists
                    if "already exists" not in str(e).lower() and "duplicate" not in str(e).lower():
                        print(f"Warning: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Schema loaded successfully!")
        print("\n📊 Database Tables Created:")
        print("  - users (authentication)")
        print("  - role (ADMIN, HOD, FACULTY, STUDENT, PARENT)")
        print("  - college")
        print("  - department")
        print("  - division")
        print("  - semester")
        print("  - subject")
        print("  - faculty")
        print("  - student")
        print("  - parent")
        print("  - timetable")
        print("  - lecture")
        print("  - attendance")
        print("  - attendance_status (PRESENT, ABSENT)")
        print("  - proxy_lecture")
        print("  - academic_calendar")
        
        return True
        
    except Exception as e:
        print(f"Error loading schema: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution."""
    print("=" * 60)
    print("Attendance Management System - Database Setup")
    print("=" * 60)
    print()
    
    # Get database config
    db_url = os.getenv("DATABASE_URL", "mysql://root:@localhost:3306/databse")
    db_config = parse_db_url(db_url)
    
    print(f"Database: {db_config['database']}")
    print(f"Host: {db_config['host']}:{db_config['port']}")
    print(f"User: {db_config['user']}")
    print()
    
    # Create database
    if not create_database(db_config):
        print("❌ Failed to create database")
        return False
    
    # Load schema
    if not load_schema(db_config):
        print("❌ Failed to load schema")
        return False
    
    print()
    print("=" * 60)
    print("✓ Database setup completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Run: python scripts/create_admin.py")
    print("  2. Start the Flask app: python -m attendance_system.app")
    print()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
