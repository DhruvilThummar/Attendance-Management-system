/**
 * Register Page JavaScript
 * Handles role selection and modal-based registration
 */

// Role ID mapping
const roleMapping = {
    'ADMIN': 1,
    'HOD': 2,
    'FACULTY': 3,
    'STUDENT': 4,
    'PARENT': 5
};

// Role display names
const roleNames = {
    'ADMIN': 'College Admin',
    'HOD': 'Head of Department',
    'FACULTY': 'Faculty Member',
    'STUDENT': 'Student',
    'PARENT': 'Parent/Guardian'
};

/**
 * Open registration modal for selected role
 */
function openRegisterModal(roleName) {
    // Set role title
    document.getElementById('roleTitle').textContent = roleNames[roleName];

    // Set hidden role_id field
    document.getElementById('role_id').value = roleMapping[roleName];

    // Clear previous form data
    document.getElementById('registerForm').reset();
    document.getElementById('role_id').value = roleMapping[roleName];

    // Clear role-specific fields
    document.getElementById('roleSpecificFields').innerHTML = '';

    // Add role-specific fields if needed
    addRoleSpecificFields(roleName);

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('registerModal'));
    modal.show();
}

/**
 * Add role-specific form fields
 */
function addRoleSpecificFields(roleName) {
    const container = document.getElementById('roleSpecificFields');
    let fieldsHTML = '';

    switch (roleName) {
        case 'STUDENT':
            fieldsHTML = `
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-123"></i> Roll Number
                    </label>
                    <input type="text" class="form-control" name="roll_number" placeholder="Enter your roll number">
                </div>
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-calendar"></i> Academic Year
                    </label>
                    <select class="form-control" name="academic_year">
                        <option value="">Select Year</option>
                        <option value="1">First Year</option>
                        <option value="2">Second Year</option>
                        <option value="3">Third Year</option>
                        <option value="4">Fourth Year</option>
                    </select>
                </div>
            `;
            break;

        case 'FACULTY':
            fieldsHTML = `
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-book"></i> Subject Specialization
                    </label>
                    <input type="text" class="form-control" name="specialization" placeholder="e.g., Computer Science">
                </div>
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-award"></i> Qualification
                    </label>
                    <input type="text" class="form-control" name="qualification" placeholder="e.g., M.Tech, Ph.D">
                </div>
            `;
            break;

        case 'HOD':
            fieldsHTML = `
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-diagram-3"></i> Department
                    </label>
                    <input type="text" class="form-control" name="department" placeholder="Department name">
                </div>
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-award"></i> Qualification
                    </label>
                    <input type="text" class="form-control" name="qualification" placeholder="e.g., M.Tech, Ph.D">
                </div>
            `;
            break;

        case 'PARENT':
            fieldsHTML = `
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-person"></i> Student Name
                    </label>
                    <input type="text" class="form-control" name="student_name" placeholder="Your child's name">
                </div>
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-123"></i> Student Roll Number
                    </label>
                    <input type="text" class="form-control" name="student_roll" placeholder="Student's roll number">
                </div>
            `;
            break;

        case 'ADMIN':
            fieldsHTML = `
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-shield-check"></i> Admin Code
                    </label>
                    <input type="text" class="form-control" name="admin_code" placeholder="Enter admin authorization code">
                    <small class="text-muted">Contact college to get admin code</small>
                </div>
            `;
            break;
    }

    container.innerHTML = fieldsHTML;
}

document.addEventListener('DOMContentLoaded', function () {
    // Get form
    const registerForm = document.getElementById('registerForm');

    if (!registerForm) {
        return;
    }

    // Handle form submission
    registerForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);

        // Validation
        const name = formData.get('name').trim();
        const email = formData.get('email').trim();
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');
        const collegeId = formData.get('college_id');
        const roleId = formData.get('role_id');
        const terms = formData.get('terms');

        // Client-side validation
        const errors = [];
        if (!name) errors.push('Name is required');
        if (!email) errors.push('Email is required');
        if (!password) errors.push('Password is required');
        if (password !== confirmPassword) errors.push('Passwords do not match');
        if (!collegeId) errors.push('College is required');
        if (!roleId) errors.push('Role is required');
        if (!terms) errors.push('You must accept the terms & conditions');

        if (password && password.length < 6) {
            errors.push('Password must be at least 6 characters');
        }

        if (errors.length > 0) {
            alert('Registration failed:\n\n' + errors.join('\n'));
            return;
        }

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(formData)
            });

            const contentType = response.headers.get('content-type');

            if (contentType && contentType.includes('application/json')) {
                // JSON response from AJAX endpoint
                const data = await response.json();
                if (data.success) {
                    // Close modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
                    modal.hide();

                    // Show success message and redirect
                    alert('✓ Registration successful!\nYour account is pending admin approval.\nPlease login after approval.');
                    window.location.href = '/login';
                } else {
                    alert('❌ Registration failed:\n' + data.message);
                }
            } else {
                // HTML response (fallback)
                const text = await response.text();
                document.body.innerHTML = text;
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });

    // Redirect to dashboard if already logged in
    if (typeof SessionManager !== 'undefined' && SessionManager.isLoggedIn()) {
        const roleRedirects = {
            'ADMIN': '/college/dashboard',
            'HOD': '/hod/dashboard',
            'FACULTY': '/faculty/dashboard',
            'STUDENT': '/student/dashboard',
            'PARENT': '/parent/dashboard'
        };

        const role = SessionManager.getUserRole();
        const redirectUrl = roleRedirects[role] || '/';
        window.location.href = redirectUrl;
    }
});

break;
        case 'parent':
document.getElementById('parentFields').style.display = 'block';
break;
    }

// Scroll to top
document.querySelector('.auth-card').scrollTop = 0;
}

// Go back to role selection
function goBackToRoleSelection(e) {
    e.preventDefault();
    document.getElementById('roleSelectionScreen').style.display = 'block';
    document.getElementById('formScreen').style.display = 'none';
    resetForm();
}

// Reset form
function resetForm() {
    document.getElementById('registrationForm').reset();
    document.getElementById('selectedRole').value = '';

    // Clear all error messages
    document.querySelectorAll('.error-text').forEach(el => {
        el.classList.add('d-none');
    });

    // Clear all invalid classes
    document.querySelectorAll('.form-control').forEach(el => {
        el.classList.remove('is-invalid');
    });
}

// Initialize college autocomplete
function initCollegeSearch(inputId, suggestionsId) {
    const input = document.getElementById(inputId);
    const suggestionsBox = document.getElementById(suggestionsId);

    input.addEventListener('input', function () {
        const value = this.value.toLowerCase();

        if (value.length > 0) {
            const filtered = colleges.filter(college =>
                college.toLowerCase().includes(value)
            );

            if (filtered.length > 0) {
                suggestionsBox.innerHTML = filtered.map(college =>
                    `<div class="suggestion-item" onclick="selectCollege('${college}', '${inputId}')">${college}</div>`
                ).join('');
                suggestionsBox.classList.add('show');
            } else {
                suggestionsBox.classList.remove('show');
            }
        } else {
            suggestionsBox.classList.remove('show');
        }
    });

    // Close suggestions on focus out
    input.addEventListener('blur', function () {
        setTimeout(() => {
            suggestionsBox.classList.remove('show');
        }, 200);
    });
}

// Select college from dropdown
function selectCollege(college, inputId) {
    document.getElementById(inputId).value = college;
    const suggestionsId = inputId + 'Suggestions';
    document.getElementById(suggestionsId).classList.remove('show');
}

// Validate Email
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validate Password
function validatePassword(password) {
    const hasMinLength = password.length >= 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[!@#$%^&*()_\-+=\[\]{};:'",.<>?/\\|`~]/.test(password);

    return hasMinLength && hasUpperCase && hasNumber && hasSpecialChar;
}

// Show error
function showError(inputId, errorId, message) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);

    input.classList.add('is-invalid');
    if (error) {
        error.innerHTML = `<i class="bi bi-exclamation-circle"></i> ${message}`;
        error.classList.remove('d-none');
    }
}

// Clear error
function clearError(inputId, errorId) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);

    input.classList.remove('is-invalid');
    if (error) {
        error.classList.add('d-none');
        error.innerHTML = '';
    }
}

// Form submission
function submitRegistration(e) {
    e.preventDefault();

    const role = document.getElementById('selectedRole').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const terms = document.getElementById('terms').checked;

    let isValid = true;

    // Validate email
    if (!email || !validateEmail(email)) {
        showError('email', 'emailError', email ? 'Invalid email format' : 'Email is required');
        isValid = false;
    } else {
        clearError('email', 'emailError');
    }

    // Validate password
    if (!password) {
        showError('password', 'passwordError', 'Password is required');
        isValid = false;
    } else if (!validatePassword(password)) {
        showError('password', 'passwordError',
            'Password must have: 8+ chars, 1 uppercase, 1 number, 1 special char');
        isValid = false;
    } else {
        clearError('password', 'passwordError');
    }

    // Validate confirm password
    if (!confirmPassword) {
        showError('confirmPassword', 'confirmPasswordError', 'Please confirm your password');
        isValid = false;
    } else if (password !== confirmPassword) {
        showError('confirmPassword', 'confirmPasswordError', 'Passwords do not match');
        isValid = false;
    } else {
        clearError('confirmPassword', 'confirmPasswordError');
    }

    // Validate terms
    if (!terms) {
        alert('Please agree to the Terms & Conditions');
        isValid = false;
    }

    // Role-specific validation
    if (role === 'student') {
        const name = document.getElementById('studentName').value;
        const enrollment = document.getElementById('enrollment').value;
        const college = document.getElementById('studentCollege').value;

        if (!name) {
            showError('studentName', null, 'Name is required');
            isValid = false;
        }
        if (!enrollment) {
            showError('enrollment', null, 'Enrollment number is required');
            isValid = false;
        }
        if (!college) {
            showError('studentCollege', null, 'Please select a college');
            isValid = false;
        }
    } else if (role === 'faculty') {
        const name = document.getElementById('facultyName').value;
        const college = document.getElementById('facultyCollege').value;
        const department = document.getElementById('department').value;

        if (!name) isValid = false;
        if (!college) isValid = false;
        if (!department) isValid = false;
    } else if (role === 'hod') {
        const name = document.getElementById('hodName').value;
        const college = document.getElementById('hodCollege').value;
        const department = document.getElementById('hodDepartment').value;

        if (!name) isValid = false;
        if (!college) isValid = false;
        if (!department) isValid = false;
    } else if (role === 'college_admin') {
        const name = document.getElementById('adminName').value;
        const college = document.getElementById('adminCollege').value;
        const phone = document.getElementById('adminPhone').value;

        if (!name) isValid = false;
        if (!college) isValid = false;
        if (!phone) isValid = false;
    } else if (role === 'parent') {
        const name = document.getElementById('parentName').value;
        const enrollment = document.getElementById('studentEnrollmentParent').value;
        const phone = document.getElementById('parentPhone').value;

        if (!name) isValid = false;
        if (!enrollment) isValid = false;
        if (!phone) isValid = false;
    }

    if (isValid) {
        // Prepare form data
        const formData = new FormData(document.getElementById('registrationForm'));

        // Additional data based on role
        if (role === 'student') {
            formData.set('name', document.getElementById('studentName').value);
            formData.set('college', document.getElementById('studentCollege').value);
            formData.set('enrollment', document.getElementById('enrollment').value);
        } else if (role === 'faculty') {
            formData.set('name', document.getElementById('facultyName').value);
            formData.set('college', document.getElementById('facultyCollege').value);
            formData.set('department', document.getElementById('department').value);
        } else if (role === 'hod') {
            formData.set('name', document.getElementById('hodName').value);
            formData.set('college', document.getElementById('hodCollege').value);
            formData.set('department', document.getElementById('hodDepartment').value);
        } else if (role === 'college_admin') {
            formData.set('name', document.getElementById('adminName').value);
            formData.set('college', document.getElementById('adminCollege').value);
            formData.set('phone', document.getElementById('adminPhone').value);
        } else if (role === 'parent') {
            formData.set('name', document.getElementById('parentName').value);
            formData.set('childEnrollment', document.getElementById('studentEnrollmentParent').value);
            formData.set('phone', document.getElementById('parentPhone').value);
        }

        console.log('Form Data:', {
            role: formData.get('role'),
            email: formData.get('email'),
            password: '***',
            name: formData.get('name'),
            college: formData.get('college')
        });

        // TODO: Send to backend
        alert(`Registration form submitted for ${roleTitles[role]}!\n\nEmail: ${formData.get('email')}\nRole: ${roleTitles[role]}`);

        // Uncomment below to send to server
        // fetch('/register', {
        //     method: 'POST',
        //     body: formData
        // })
        // .then(response => response.json())
        // .then(data => {
        //     if (data.success) {
        //         alert('Registration successful!');
        //         window.location.href = '/login';
        //     } else {
        //         alert('Error: ' + data.message);
        //     }
        // })
        // .catch(error => console.error('Error:', error));
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    // Highlight role selection
    document.querySelectorAll('.role-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.role-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
