"""
Authentication routes - Login, Register, Logout
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.user import User, Role, db
from models.college import College

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    """User login with email and password validation"""
    # Check if user is already logged in (GET request)
    if request.method == 'GET' and 'user_id' in session and 'role' in session:
        # Redirect to appropriate dashboard based on role
        role_redirects = {
            'SUPERADMIN': '/superadmin/dashboard',
            'ADMIN': '/college/dashboard',
            'HOD': '/hod/dashboard',
            'FACULTY': '/faculty/dashboard',
            'STUDENT': '/student/dashboard',
            'PARENT': '/parent/dashboard'
        }
        redirect_url = role_redirects.get(session['role'], '/')
        return redirect(redirect_url)
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        
        # Validation
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            })
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user is None:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            })
        
        # Check password
        if not user.check_password(password):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            })
        
        # Check if user is approved by admin
        if not user.is_approved:
            return jsonify({
                'success': False,
                'message': 'Your account is pending admin approval'
            })
        
        # Set session data
        session['user_id'] = user.user_id
        session['email'] = user.email
        session['name'] = user.name
        session['role'] = user.get_role_name()
        session.permanent = remember
        
        # Determine redirect URL based on role
        role_redirects = {
            'SUPERADMIN': '/superadmin/dashboard',
            'ADMIN': '/college/dashboard',
            'HOD': '/hod/dashboard',
            'FACULTY': '/faculty/dashboard',
            'STUDENT': '/student/dashboard',
            'PARENT': '/parent/dashboard'
        }
        redirect_url = role_redirects.get(user.get_role_name(), '/')
        
        # Return JSON response for AJAX requests
        return jsonify({
            'success': True,
            'message': f'Welcome back, {user.name}!',
            'redirect': redirect_url,
            'user': {
                'user_id': user.user_id,
                'email': user.email,
                'name': user.name,
                'role': user.get_role_name()
            }
        })
    
    return render_template("login.html")


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    """User registration with proper validation and password hashing"""
    # Check if user is already logged in (GET request)
    if request.method == 'GET' and 'user_id' in session and 'role' in session:
        # Redirect to appropriate dashboard based on role
        role_redirects = {
            'SUPERADMIN': '/superadmin/dashboard',
            'ADMIN': '/college/dashboard',
            'HOD': '/hod/dashboard',
            'FACULTY': '/faculty/dashboard',
            'STUDENT': '/student/dashboard',
            'PARENT': '/parent/dashboard'
        }
        redirect_url = role_redirects.get(session['role'], '/')
        return redirect(redirect_url)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        college_id = request.form.get('college_id')
        role_id = request.form.get('role_id')
        mobile = request.form.get('mobile', '').strip()
        
        # Validation
        errors = []
        
        if not name:
            errors.append('Name is required')
        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')
        if not confirm_password:
            errors.append('Please confirm password')
        if password != confirm_password:
            errors.append('Passwords do not match')
        if not college_id:
            errors.append('College is required')
        if not role_id:
            errors.append('Role is required')
        
        # Email format validation
        if email and '@' not in email:
            errors.append('Invalid email format')
        
        # Password strength validation (minimum 6 characters)
        if password and len(password) < 6:
            errors.append('Password must be at least 6 characters long')
        
        # Mobile format validation (optional but validate if provided)
        if mobile and not mobile.isdigit():
            errors.append('Mobile number must contain only digits')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            errors.append('Email already registered')
        
        if errors:
            return jsonify({
                'success': False,
                'message': errors[0]  # Return first error message
            })
        
        try:
            from models.student import Student
            from models.parent import Parent
            
            # Create new user
            new_user = User(
                name=name,
                email=email,
                college_id=int(college_id),
                role_id=int(role_id),
                mobile=mobile if mobile else None,
                is_approved=False  # Default: requires admin approval
            )
            
            # Set password with custom hashing
            new_user.set_password(password)
            
            # Add to database
            db.session.add(new_user)
            db.session.flush()  # Get the user_id
            
            # Handle parent-specific linking
            if int(role_id) == 41:  # PARENT role
                student_enrollment = request.form.get('student_enrollment_number', '').strip()
                
                if not student_enrollment:
                    db.session.rollback()
                    return jsonify({
                        'success': False,
                        'message': 'Student enrollment number is required for parent registration'
                    })
                
                # Find student by enrollment number
                student = Student.get_by_enrollment_no(student_enrollment)
                
                if not student:
                    db.session.rollback()
                    return jsonify({
                        'success': False,
                        'message': f'Student with enrollment number "{student_enrollment}" not found. Please verify the enrollment number.'
                    })
                
                # Verify student is in the same college
                if student.department.college_id != int(college_id):
                    db.session.rollback()
                    return jsonify({
                        'success': False,
                        'message': 'Student enrollment number does not match the selected college'
                    })
                
                # Create parent-student link
                parent_link = Parent(
                    user_id=new_user.user_id,
                    student_id=student.student_id
                )
                db.session.add(parent_link)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Registration successful! Your account is pending admin approval. You will receive an email once approved.'
            })
        
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Registration failed: {str(e)}'
            })
    
    # GET request - show form with colleges and roles
    colleges = College.query.all()
    roles = Role.query.all()
    return render_template("register.html", colleges=colleges, roles=roles)


@auth_bp.route("/logout")
def logout():
    """User logout"""
    session.clear()
    
    # Handle AJAX requests usually sent by SessionManager.logout()
    if request.is_json or (request.headers.get('Accept') and 'application/json' in request.headers.get('Accept')):
        return jsonify({
            'success': True,
            'message': 'You have been logged out successfully',
            'redirect': url_for('main.home')
        })
    
    # Handle standard browser requests (e.g. from Navbar link)
    return redirect(url_for('main.home'))
