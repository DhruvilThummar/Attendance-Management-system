"""Authentication endpoints and entry pages."""
from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, session, url_for

from ..services import auth_service

bp = Blueprint("auth", __name__)


@bp.get("/")
def home():
    return render_template("home.html")


@bp.get("/login")
def login_form():
    next_path = request.args.get("next")
    return render_template("auth/login.html", next_path=next_path)


@bp.get("/about")
def about():
    return render_template("about.html")



@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")
        role = request.form.get("role")
        
        # Basic validation
        if not email or not password or not role:
            return render_template("auth/signup.html", error="All fields are required.")
            
        # Check specific constraints
        # Only HOD, Faculty, Student can sign up freely (Admin is seeded or internal)
        if role not in ["HOD", "Faculty", "Student"]:
             return render_template("auth/signup.html", error="Invalid role selected.")

        # Create user with is_approved=False
        try:
            from ..models.user import User
            # Check existing
            existing = auth_service.verify_credentials(email, "dummy") 
            # Note: verify_credentials checks password, so this isn't best for existence check.
            # Ideally we use a specific check or catch duplicate key error.
            # Using execute directly for uniqueness check to be safe
            from ..db_manager import fetch_one
            college_id = request.form.get("college_id")
            if not college_id:
                 return render_template("auth/signup.html", error="College selection is required.", colleges=[{"id": r[0], "name": r[1]} for r in execute("SELECT id, name FROM colleges")])

            if fetch_one("SELECT 1 FROM users WHERE email = %s", (email,)):
                 return render_template("auth/signup.html", error="Email already exists.", colleges=[{"id": r[0], "name": r[1]} for r in execute("SELECT id, name FROM colleges")])

            user = User(email=email, password=password, role=role, is_approved=False)
            user.save()
            # Patch college_id (as User model __init__ might not take it or save didn't use it yet if not updated)
            # Actually we usually update the model. Let's do raw update for safety until model refactor.
            from ..db_manager import execute
            execute("UPDATE users SET college_id=%s WHERE id=%s", (college_id, user.id))
            user.save()
            
            return render_template("auth/signup.html", success="Registration successful! Please wait for approval from your superior.")
        except Exception as e:
             return render_template("auth/signup.html", error=f"Registration failed: {e}")

    from ..db_manager import execute
    colleges = [{"id": r[0], "name": r[1]} for r in execute("SELECT id, name FROM colleges")]
    return render_template("auth/signup.html", colleges=colleges)

@bp.route("/register-college", methods=["GET", "POST"])
def register_college():
    if request.method == "POST":
        name = request.form.get("name")
        # In a real app we'd save this request to a table or status.
        # User asked for "register... new college option".
        # Let's insert it directly into colleges for now.
        from ..db_manager import execute
        try:
            execute("INSERT INTO colleges (name) VALUES (%s)", (name,))
            return render_template("auth/register_college.html", success=f"College '{name}' registered successfully! You can now sign up users under this college.")
        except Exception as e:
             return render_template("auth/register_college.html", error=f"Error: {e}")

    return render_template("auth/register_college.html")

@bp.post("/login")
def login():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    next_path = request.form.get("next") or request.args.get("next")

    if not email or not password:
        return (
            render_template(
                "auth/login.html",
                error="Email and password are required.",
                next_path=next_path,
            ),
            400,
        )

    user = auth_service.verify_credentials(email, password)
    if not user:
        return (
            render_template(
                "auth/login.html",
                error="Invalid email or password.",
                next_path=next_path,
            ),
            401,
        )
        
    # Check Approval Status
    # Verify credentials returns dict, need to fetch full user or check DB
    # We can update verify_credentials to return is_approved or check here
    from ..db_manager import fetch_one
    is_approved = fetch_one("SELECT is_approved FROM users WHERE id = %s", (user['id'],))[0]
    
    if not is_approved:
         return (
            render_template(
                "auth/login.html",
                error="Your account is pending approval.",
                next_path=next_path,
            ),
            403,
        )

    session["user"] = user

    # Redirect priority: provided next_path -> role dashboard -> home
    if next_path and next_path.startswith("/"):
        return redirect(next_path)

    role_target = {
        "SuperAdmin": "super_admin.dashboard",
        "CollegeAdmin": "admin.dashboard",
        "Admin": "admin.dashboard",  # Fallback
        "HOD": "hod.dashboard",
        "Faculty": "faculty.dashboard",
        "Student": "student.dashboard",
    }.get(user.get("role"))

    if role_target:
        return redirect(url_for(role_target))

    return redirect(url_for("auth.home"))


@bp.post("/logout")
def logout():
    session.pop("user", None)
    session.clear()
    return redirect(url_for("auth.home"))
