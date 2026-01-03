# Attendance-Management-system

Starter scaffold for the Smart Attendance Management System.

## Run
- Create a virtual environment and install deps: `pip install -e .`
- Set `DATABASE_URL` env var for PostgreSQL.
- Run dev server: `flask --app attendance_system.app run --debug`.

## Structure
- attendance_system/app.py — Flask factory + RBAC decorator
- attendance_system/blueprints/ — role-based blueprints
- attendance_system/services/ — business logic stubs
- attendance_system/models/ — data classes (no I/O)
- scripts/ — schema + seed placeholders
- docs/api.md — expand with contracts
- tests/ — pytest smoke test