// Colleges list for autocomplete
const colleges = [
    "Engineering College Mumbai",
    "IIT Bombay",
    "COEP Pune",
    "NIT Surathkal",
    "Delhi Institute of Technology",
    "MIT Manipal",
    "VIT Vellore",
    "BITS Pilani"
];

// Role titles mapping
const roleTitles = {
    'student': 'Student',
    'faculty': 'Faculty',
    'hod': 'Head of Department (HOD)',
    'college_admin': 'College Administrator',
    'parent': 'Parent/Guardian'
};

// Select role and show form
function selectRole(role) {
    const selectedRole = document.getElementById('selectedRole');
    selectedRole.value = role;

    // Hide role selection, show form
    document.getElementById('roleSelectionScreen').style.display = 'none';
    document.getElementById('formScreen').style.display = 'block';

    // Update form title
    document.getElementById('formTitle').textContent = `Register as ${roleTitles[role]}`;

    // Hide all role-specific fields first
    document.getElementById('studentFields').style.display = 'none';
    document.getElementById('facultyFields').style.display = 'none';
    document.getElementById('hodFields').style.display = 'none';
    document.getElementById('collegeAdminFields').style.display = 'none';
    document.getElementById('parentFields').style.display = 'none';

    // Show selected role fields
    switch (role) {
        case 'student':
            document.getElementById('studentFields').style.display = 'block';
            initCollegeSearch('studentCollege', 'studentCollegeSuggestions');
            break;
        case 'faculty':
            document.getElementById('facultyFields').style.display = 'block';
            initCollegeSearch('facultyCollege', 'facultyCollegeSuggestions');
            break;
        case 'hod':
            document.getElementById('hodFields').style.display = 'block';
            initCollegeSearch('hodCollege', 'hodCollegeSuggestions');
            break;
        case 'college_admin':
            document.getElementById('collegeAdminFields').style.display = 'block';
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
