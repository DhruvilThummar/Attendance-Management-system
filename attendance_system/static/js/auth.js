/**
 * Authentication Module
 * Handles login, registration, and logout
 */

// Login Form Handler
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        try {
            showLoading();
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showAlert('Login successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            } else {
                showAlert(data.message || 'Login failed', 'danger');
            }
        } catch (error) {
            console.error('Login error:', error);
            showAlert('An error occurred. Please try again.', 'danger');
        } finally {
            hideLoading();
        }
    });
}

// Registration Form Handler
const registerForm = document.getElementById('register-form');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        
        if (password !== confirmPassword) {
            showAlert('Passwords do not match!', 'danger');
            return;
        }
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            password: password,
            mobile: document.getElementById('mobile').value,
            college_id: document.getElementById('college_id').value,
            role_id: document.getElementById('role_id').value
        };
        
        // Add role-specific fields
        const roleId = parseInt(formData.role_id);
        if (roleId === 3) { // Faculty
            formData.dept_id = document.getElementById('dept_id').value;
        } else if (roleId === 4) { // Student
            formData.enrollment_no = document.getElementById('enrollment_no').value;
            formData.roll_no = document.getElementById('roll_no').value;
            formData.division_id = document.getElementById('division_id').value;
            formData.dept_id = document.getElementById('dept_id').value;
            formData.semester_id = document.getElementById('semester_id').value;
        }
        
        try {
            showLoading();
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showAlert('Registration successful! Please wait for admin approval.', 'success');
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                showAlert(data.message || 'Registration failed', 'danger');
            }
        } catch (error) {
            console.error('Registration error:', error);
            showAlert('An error occurred. Please try again.', 'danger');
        } finally {
            hideLoading();
        }
    });
}

// Password Toggle
document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', function() {
        const input = this.previousElementSibling;
        const icon = this.querySelector('i');
        
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
    });
});

// Load colleges for registration
async function loadColleges() {
    const collegeSelect = document.getElementById('college_id');
    if (!collegeSelect) return;
    
    try {
        const response = await fetch('/api/colleges');
        const colleges = await response.json();
        
        collegeSelect.innerHTML = '<option value="">Select College</option>';
        colleges.forEach(college => {
            const option = document.createElement('option');
            option.value = college.college_id;
            option.textContent = college.college_name;
            collegeSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading colleges:', error);
    }
}

// Load roles for registration
async function loadRoles() {
    const roleSelect = document.getElementById('role_id');
    if (!roleSelect) return;
    
    try {
        const response = await fetch('/api/roles');
        const roles = await response.json();
        
        // Filter out admin and superadmin roles
        const allowedRoles = roles.filter(r => ['FACULTY', 'STUDENT', 'PARENT'].includes(r.role_name));
        
        roleSelect.innerHTML = '<option value="">Select Role</option>';
        allowedRoles.forEach(role => {
            const option = document.createElement('option');
            option.value = role.role_id;
            option.textContent = role.role_name;
            roleSelect.appendChild(option);
        });
        
        // Handle role change to show/hide role-specific fields
        roleSelect.addEventListener('change', handleRoleChange);
    } catch (error) {
        console.error('Error loading roles:', error);
    }
}

// Handle role change
function handleRoleChange(e) {
    const roleId = parseInt(e.target.value);
    const facultyFields = document.getElementById('faculty-fields');
    const studentFields = document.getElementById('student-fields');
    const parentFields = document.getElementById('parent-fields');
    
    // Hide all role-specific fields
    if (facultyFields) facultyFields.classList.add('d-none');
    if (studentFields) studentFields.classList.add('d-none');
    if (parentFields) parentFields.classList.add('d-none');
    
    // Show relevant fields based on role
    if (roleId === 3 && facultyFields) { // Faculty
        facultyFields.classList.remove('d-none');
        loadDepartments();
    } else if (roleId === 4 && studentFields) { // Student
        studentFields.classList.remove('d-none');
        loadDepartments();
        loadSemesters();
    } else if (roleId === 5 && parentFields) { // Parent
        parentFields.classList.remove('d-none');
    }
}

// Load departments
async function loadDepartments() {
    const deptSelect = document.getElementById('dept_id');
    if (!deptSelect) return;
    
    try {
        const response = await fetch('/api/departments');
        const departments = await response.json();
        
        deptSelect.innerHTML = '<option value="">Select Department</option>';
        departments.forEach(dept => {
            const option = document.createElement('option');
            option.value = dept.dept_id;
            option.textContent = dept.dept_name;
            deptSelect.appendChild(option);
        });
        
        // If student, load divisions when department changes
        if (document.getElementById('division_id')) {
            deptSelect.addEventListener('change', loadDivisions);
        }
    } catch (error) {
        console.error('Error loading departments:', error);
    }
}

// Load divisions
async function loadDivisions() {
    const deptId = document.getElementById('dept_id').value;
    const divisionSelect = document.getElementById('division_id');
    if (!divisionSelect || !deptId) return;
    
    try {
        const response = await fetch(`/api/divisions?dept_id=${deptId}`);
        const divisions = await response.json();
        
        divisionSelect.innerHTML = '<option value="">Select Division</option>';
        divisions.forEach(div => {
            const option = document.createElement('option');
            option.value = div.division_id;
            option.textContent = div.division_name;
            divisionSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading divisions:', error);
    }
}

// Load semesters
async function loadSemesters() {
    const semesterSelect = document.getElementById('semester_id');
    if (!semesterSelect) return;
    
    try {
        const response = await fetch('/api/semesters');
        const semesters = await response.json();
        
        semesterSelect.innerHTML = '<option value="">Select Semester</option>';
        semesters.forEach(sem => {
            const option = document.createElement('option');
            option.value = sem.semester_id;
            option.textContent = `Semester ${sem.semester_no} (${sem.academic_year})`;
            semesterSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading semesters:', error);
    }
}

// Initialize on page load
if (document.getElementById('register-form')) {
    loadColleges();
    loadRoles();
}
