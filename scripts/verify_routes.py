"""
Route Verification Script
========================

This script verifies that all routes are properly connected and registered.
Run this to check the routing configuration of the application.

Usage:
    python scripts/verify_routes.py
"""

from __future__ import annotations
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from attendance_system.app import create_app


def verify_routes():
    """Verify all routes are properly registered."""
    print("=" * 80)
    print("ATTENDANCE MANAGEMENT SYSTEM - ROUTE VERIFICATION")
    print("=" * 80)
    print()
    
    # Create app instance
    app = create_app()
    
    # Group routes by blueprint
    routes_by_blueprint = {}
    
    for rule in app.url_map.iter_rules():
        # Skip static route
        if rule.endpoint == 'static':
            continue
        
        # Get blueprint name
        blueprint = rule.endpoint.split('.')[0] if '.' in rule.endpoint else 'app'
        
        if blueprint not in routes_by_blueprint:
            routes_by_blueprint[blueprint] = []
        
        routes_by_blueprint[blueprint].append({
            'endpoint': rule.endpoint,
            'path': rule.rule,
            'methods': sorted([m for m in rule.methods if m not in ['HEAD', 'OPTIONS']])
        })
    
    # Print routes organized by blueprint
    total_routes = 0
    
    for blueprint_name in sorted(routes_by_blueprint.keys()):
        routes = sorted(routes_by_blueprint[blueprint_name], key=lambda x: x['path'])
        
        print(f"\n{'=' * 80}")
        print(f"Blueprint: {blueprint_name.upper()}")
        print(f"{'=' * 80}")
        print(f"{'Endpoint':<40} {'Path':<30} {'Methods':<15}")
        print("-" * 80)
        
        for route in routes:
            methods_str = ', '.join(route['methods'])
            print(f"{route['endpoint']:<40} {route['path']:<30} {methods_str:<15}")
            total_routes += 1
        
        print(f"\nTotal routes in {blueprint_name}: {len(routes)}")
    
    print(f"\n{'=' * 80}")
    print(f"TOTAL ROUTES: {total_routes}")
    print(f"{'=' * 80}")
    
    # Check for required routes
    print("\n" + "=" * 80)
    print("CHECKING CRITICAL ROUTES")
    print("=" * 80)
    
    critical_routes = [
        ('/', 'Home page'),
        ('/api/login', 'Login API'),
        ('/api/registration', 'Registration API'),
        ('/dashboard', 'Dashboard'),
        ('/dashboard/student', 'Student Dashboard'),
        ('/dashboard/faculty', 'Faculty Dashboard'),
        ('/mark-attendance', 'Mark Attendance'),
        ('/api/attendance/mark', 'Attendance API'),
        ('/api/reports', 'Reports API'),
        ('/faculty', 'Faculty Page'),
        ('/students', 'Students Page'),
    ]
    
    all_paths = [r['path'] for routes in routes_by_blueprint.values() for r in routes]
    
    print()
    for path, description in critical_routes:
        status = "✓" if path in all_paths else "✗"
        print(f"{status} {description:<30} {path}")
    
    # Check for potential conflicts
    print("\n" + "=" * 80)
    print("CHECKING FOR ROUTE CONFLICTS")
    print("=" * 80)
    print()
    
    path_counts = {}
    for routes in routes_by_blueprint.values():
        for route in routes:
            path = route['path']
            if path not in path_counts:
                path_counts[path] = []
            path_counts[path].append(route['endpoint'])
    
    conflicts = {path: endpoints for path, endpoints in path_counts.items() if len(endpoints) > 1}
    
    if conflicts:
        print("⚠️  WARNING: Found route conflicts:")
        for path, endpoints in conflicts.items():
            print(f"  Path: {path}")
            for endpoint in endpoints:
                print(f"    - {endpoint}")
    else:
        print("✓ No route conflicts found")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Blueprints: {len(routes_by_blueprint)}")
    print(f"Total Routes: {total_routes}")
    print(f"Route Conflicts: {len(conflicts)}")
    print()
    
    if len(conflicts) > 0:
        print("⚠️  VERIFICATION FAILED: Route conflicts detected")
        return False
    else:
        print("✓ VERIFICATION PASSED: All routes properly configured")
        return True


if __name__ == "__main__":
    try:
        success = verify_routes()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
