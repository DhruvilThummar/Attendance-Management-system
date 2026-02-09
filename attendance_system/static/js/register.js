/**
 * Register Page JavaScript
 * Handles role selection and modal-based registration
 */

// Role ID mapping
const roleMapping = {
    'ADMIN': 37,
    'HOD': 38,
    'FACULTY': 39,
    'STUDENT': 40,
    'PARENT': 41
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
                        <i class="bi bi-123"></i> Enrollment Number *
                    </label>
                    <input type="text" class="form-control" name="enrollment_number" placeholder="Enter your enrollment number" required>
                </div>
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-diagram-3"></i> Department *
                    </label>
                    <select class="form-control" name="department" required>
                        <option value="">-- Select Department --</option>
                        <option value="CSE">Computer Science & Engineering</option>
                        <option value="ECE">Electronics & Communication</option>
                        <option value="ME">Mechanical Engineering</option>
                        <option value="CE">Civil Engineering</option>
                        <option value="EE">Electrical Engineering</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-layers"></i> Division *
                    </label>
                    <select class="form-control" name="division" required>
                        <option value="">-- Select Division --</option>
                        <option value="A">Division A</option>
                        <option value="B">Division B</option>
                        <option value="C">Division C</option>
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
                        <i class="bi bi-person"></i> Student Name *
                    </label>
                    <input type="text" class="form-control" name="student_name" placeholder="Your child's name" required>
                </div>
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-123"></i> Student Enrollment Number *
                    </label>
                    <input type="text" class="form-control" name="student_enrollment_number" placeholder="Student's enrollment number" required>
                </div>
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-diagram-3"></i> Department *
                    </label>
                    <select class="form-control" name="student_department" required>
                        <option value="">-- Select Department --</option>
                        <option value="CSE">Computer Science & Engineering</option>
                        <option value="ECE">Electronics & Communication</option>
                        <option value="ME">Mechanical Engineering</option>
                        <option value="CE">Civil Engineering</option>
                        <option value="EE">Electrical Engineering</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label class="form-label">
                        <i class="bi bi-layers"></i> Division *
                    </label>
                    <select class="form-control" name="student_division" required>
                        <option value="">-- Select Division --</option>
                        <option value="A">Division A</option>
                        <option value="B">Division B</option>
                        <option value="C">Division C</option>
                    </select>
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

        // Role-specific validation
        if (roleId === '4') { // STUDENT
            const enrollmentNumber = formData.get('enrollment_number')?.trim();
            const department = formData.get('department')?.trim();
            const division = formData.get('division')?.trim();

            if (!enrollmentNumber) errors.push('Enrollment Number is required for students');
            if (!department) errors.push('Department is required for students');
            if (!division) errors.push('Division is required for students');
        }

        if (roleId === '5') { // PARENT
            const studentName = formData.get('student_name')?.trim();
            const enrollmentNumber = formData.get('student_enrollment_number')?.trim();
            const department = formData.get('student_department')?.trim();
            const division = formData.get('student_division')?.trim();

            if (!studentName) errors.push('Student name is required');
            if (!enrollmentNumber) errors.push('Student enrollment number is required');
            if (!department) errors.push('Student department is required');
            if (!division) errors.push('Student division is required');
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
});
