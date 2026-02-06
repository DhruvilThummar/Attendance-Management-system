#!/usr/bin/env python
"""
Flask application entry point
Run with: python run.py or flask run
"""

import os
import sys

# Add both project root and attendance_system directory to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'attendance_system'))

from attendance_system.app import app

if __name__ == '__main__':
    # Get port from environment or use 5000
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Get debug mode from environment
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"\n{'='*100}")
    print(f"Starting Attendance Management System")
    print(f"{'='*100}")
    print(f"Server: http://localhost:{port}")
    print(f"Debug:  {debug}")
    print(f"{'='*100}\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=True
    )
