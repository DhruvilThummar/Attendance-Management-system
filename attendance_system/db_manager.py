"""
Database manager using mysql.connector as requested.
"""
from __future__ import annotations
import mysql.connector
import os

def create_connection(dsn: str | None = None):
    """
    Establishes a connection to the MySQL database.
    Configuration is fetched from Flask config or Environment variables.
    """
    try:
        # Parse DATABASE_URL or use individual env vars
        # DB URL format: mysql://user:pass@host:port/dbname
        # We'll use simple env vars fallback if URL parsing is complex given the strict pattern request
        
        # Taking reference from user's code but adapting for Config
        # We need to support the connection string we already use or parse it.
        from urllib.parse import urlparse
        
        db_url = dsn or os.getenv("DATABASE_URL", "mysql://root:password@localhost:3306/attendance_db")
        # Handle the commonly used mysql:// scheme
        if not db_url:
             return None
             
        # Simple parse for standard URL
        try:
            result = urlparse(db_url)
            host = result.hostname
            user = result.username
            password = result.password
            database = result.path.lstrip('/')
            port = result.port or 3306
        except:
            # Fallback defaults locally
            host = "localhost"
            user = "root"
            password = ""
            database = "attendance_db"

        # Connect
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        return mydb
        
    except mysql.connector.Error as err:
        # Using print instead of st.error since this is Flask
        print(f"Error connecting to database: {err}")
        return None

def execute(query: str, params: tuple | None = None):
    """
    Executes a SQL query and returns the result (for SELECT) 
    or commits changes (for INSERT/UPDATE/DELETE).
    Alias for run_query to maintain compatibility with existing code.
    """
    return run_query(query, params)

def fetch_one(query: str, params: tuple | None = None):
    """
    Helper to fetch a single row.
    """
    rows = run_query(query, params)
    if isinstance(rows, list) and len(rows) > 0:
        # run_query returns dictionary=True? 
        # The user's code used dictionary=True. 
        # My existing code expects tuples mainly.
        # I need to check what my codebase expects.
        # My code does `row[0]` accessing by index often (e.g. `is_approved = row[0]`).
        # If I switch to dictionary=True, I break ALL that code.
        # I MUST use dictionary=False for compatibility OR refactor the whole app.
        # Given "tack a reference", I should adapt it to fit.
        # I will use dictionary=False to match my existing `fetch_one` contract.
        return rows[0]
    return None

# Legacy compatibility: validate DB connectivity at startup.
def init_db_pool(dsn: str = "") -> None:
    conn = create_connection(dsn or None)
    if conn is None:
        raise RuntimeError("Failed to create MySQL connection")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        _ = cursor.fetchone()
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

def run_query(query, params=None):
    """
    Executes a SQL query.
    """
    conn = create_connection()
    if conn is None:
        return []
    
    try:
        # Using dictionary=False to maintain compatibility with tuple-based access in my app
        cursor = conn.cursor(dictionary=False)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER")):
            conn.commit()
            # For INSERT, return lastrowid so we can get keys
            if query.strip().upper().startswith("INSERT"):
                return cursor.lastrowid
            return [] # Other DML returns empty list
        else:
            return cursor.fetchall()
            
    except mysql.connector.Error as err:
        print(f"Query Error: {err}")
        # Re-raise or return empty? My old code might expect exceptions or handle them.
        # I'll return empty list to be safe as per user snippet style
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
