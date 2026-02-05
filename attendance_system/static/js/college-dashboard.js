// College Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function () {
    initializeDashboard();
    setupEventListeners();
});

/**
 * Initialize Dashboard
 */
function initializeDashboard() {
    console.log('Initializing College Dashboard...');

    // Initialize all modals
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        new bootstrap.Modal(modal, { keyboard: false });
    });

    // Initialize tooltips
    initializeTooltips();

    // Sync progress bars
    syncProgressBars();

    // Load initial data
    loadDashboardData();
}

/**
 * Setup Event Listeners
 */
function setupEventListeners() {
    // Department Form
    const deptForm = document.getElementById('deptForm');
    if (deptForm) {
        deptForm.addEventListener('submit', handleDepartmentSubmit);
    }

    // Division Form
    const divForm = document.getElementById('divForm');
    if (divForm) {
        divForm.addEventListener('submit', handleDivisionSubmit);
    }

    // Faculty Form
    const facultyForm = document.getElementById('facultyForm');
    if (facultyForm) {
        facultyForm.addEventListener('submit', handleFacultySubmit);
    }

    // Student Form
    const studentForm = document.getElementById('studentForm');
    if (studentForm) {
        studentForm.addEventListener('submit', handleStudentSubmit);
    }

    // Mobile collapse adjustment if needed
    // (Sidebar has been removed, so toggle logic is redundant)
}

/**
 * Initialize Tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Load Dashboard Data
 */
function loadDashboardData() {
    // This would typically fetch data from your API
    console.log('Loading dashboard data...');
    updateStatistics();
}

/**
 * Update Statistics
 */
function updateStatistics() {
    // Update attendance stats
    const statsCards = document.querySelectorAll('.stat-card');
    if (statsCards.length > 0) {
        statsCards.forEach(card => {
            const value = card.querySelector('h3');
            if (value) {
                animateCountUp(value);
            }
        });
    }
}

/**
 * Animate Count Up
 */
function animateCountUp(element) {
    const target = parseInt(element.textContent);
    if (isNaN(target)) return;

    const duration = 1000;
    const increment = target / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

/**
 * Handle Department Form Submit
 */
function handleDepartmentSubmit(e) {
    e.preventDefault();

    const formData = {
        dept_name: document.getElementById('deptName').value,
        dept_code: document.getElementById('deptCode').value,
        hod_id: document.getElementById('hodId').value || null,
        description: document.getElementById('deptDesc').value
    };

    console.log('Submitting department:', formData);

    // Validate form
    if (!formData.dept_name || !formData.dept_code) {
        showAlert('Please fill in all required fields', 'error');
        return;
    }

    // Submit data
    submitDepartment(formData);
}

/**
 * Submit Department
 */
function submitDepartment(data) {
    // Show loading spinner
    showLoadingSpinner();

    // Simulate API call
    setTimeout(() => {
        hideLoadingSpinner();
        showAlert('Department saved successfully!', 'success');

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addDeptModal'));
        if (modal) {
            modal.hide();
        }

        // Reload data
        location.reload();
    }, 1000);
}

/**
 * Handle Division Form Submit
 */
function handleDivisionSubmit(e) {
    e.preventDefault();

    const formData = {
        dept_id: document.getElementById('divDept').value,
        division_name: document.getElementById('divName').value,
        division_code: document.getElementById('divCode').value,
        capacity: parseInt(document.getElementById('divCapacity').value),
        class_teacher_id: document.getElementById('classTeacher').value || null
    };

    console.log('Submitting division:', formData);

    // Validate form
    if (!formData.dept_id || !formData.division_name || !formData.division_code || !formData.capacity) {
        showAlert('Please fill in all required fields', 'error');
        return;
    }

    if (formData.capacity <= 0) {
        showAlert('Capacity must be greater than 0', 'error');
        return;
    }

    // Submit data
    submitDivision(formData);
}

/**
 * Submit Division
 */
function submitDivision(data) {
    showLoadingSpinner();

    setTimeout(() => {
        hideLoadingSpinner();
        showAlert('Division saved successfully!', 'success');

        const modal = bootstrap.Modal.getInstance(document.getElementById('addDivModal'));
        if (modal) {
            modal.hide();
        }

        location.reload();
    }, 1000);
}

/**
 * Handle Faculty Form Submit
 */
function handleFacultySubmit(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('facultyName').value,
        email: document.getElementById('facultyEmail').value,
        dept_id: document.getElementById('facultyDept').value,
        phone: document.getElementById('facultyPhone').value,
        specialization: document.getElementById('facultySpecialization').value,
        short_name: document.getElementById('facultyShortName').value,
        is_hod: document.getElementById('isHod').checked
    };

    console.log('Submitting faculty:', formData);

    if (!formData.name || !formData.email || !formData.dept_id) {
        showAlert('Please fill in all required fields', 'error');
        return;
    }

    submitFaculty(formData);
}

/**
 * Submit Faculty
 */
function submitFaculty(data) {
    showLoadingSpinner();

    setTimeout(() => {
        hideLoadingSpinner();
        showAlert('Faculty saved successfully!', 'success');

        const modal = bootstrap.Modal.getInstance(document.getElementById('addFacultyModal'));
        if (modal) {
            modal.hide();
        }

        location.reload();
    }, 1000);
}

/**
 * Handle Student Form Submit
 */
function handleStudentSubmit(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('studentName').value,
        email: document.getElementById('studentEmail').value,
        roll_number: document.getElementById('studentRoll').value,
        phone: document.getElementById('studentPhone').value,
        dept_id: document.getElementById('studentDept').value,
        div_id: document.getElementById('studentDiv').value
    };

    console.log('Submitting student:', formData);

    if (!formData.name || !formData.email || !formData.roll_number || !formData.dept_id || !formData.div_id) {
        showAlert('Please fill in all required fields', 'error');
        return;
    }

    submitStudent(formData);
}

/**
 * Submit Student
 */
function submitStudent(data) {
    showLoadingSpinner();

    setTimeout(() => {
        hideLoadingSpinner();
        showAlert('Student saved successfully!', 'success');

        const modal = bootstrap.Modal.getInstance(document.getElementById('addStudentModal'));
        if (modal) {
            modal.hide();
        }

        location.reload();
    }, 1000);
}

/**
 * Show Alert Message
 */
function showAlert(message, type = 'info') {
    // Create alert element
    const alertId = 'alert-' + Date.now();
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); animation: slideInLeft 0.3s ease;">
            <strong>${type.charAt(0).toUpperCase() + type.slice(1)}!</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', alertHTML);

    // Auto remove after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Show Loading Spinner
 */
function showLoadingSpinner() {
    const spinnerId = 'spinner-' + Date.now();
    const spinnerHTML = `
        <div id="${spinnerId}" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 9998;">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', spinnerHTML);
    return spinnerId;
}

/**
 * Hide Loading Spinner
 */
function hideLoadingSpinner() {
    const spinners = document.querySelectorAll('[id^="spinner-"]');
    spinners.forEach(spinner => {
        spinner.remove();
    });
}



/**
 * Filter Functions
 */
function filterByDept() {
    const selectedDept = document.getElementById('deptFilter').value;
    const sections = document.querySelectorAll('.dept-section');
    const rows = document.querySelectorAll('.div-row');

    sections.forEach(section => {
        section.style.display = (!selectedDept || section.dataset.deptId === selectedDept) ? 'block' : 'none';
    });

    rows.forEach(row => {
        row.style.display = (!selectedDept || row.dataset.deptId === selectedDept) ? 'table-row' : 'none';
    });
}

function filterFaculty() {
    const deptFilter = document.getElementById('facultyDeptFilter').value.toLowerCase();
    const searchText = document.getElementById('facultySearch').value.toLowerCase();

    const cards = document.querySelectorAll('.faculty-card-container');
    const rows = document.querySelectorAll('.faculty-row');

    cards.forEach(card => {
        const deptId = card.dataset.deptId;
        const name = card.dataset.name;
        const show = (!deptFilter || deptId === deptFilter) && name.includes(searchText);
        card.style.display = show ? 'block' : 'none';
    });

    rows.forEach(row => {
        const deptId = row.dataset.deptId;
        const name = row.dataset.name;
        const show = (!deptFilter || deptId === deptFilter) && name.includes(searchText);
        row.style.display = show ? 'table-row' : 'none';
    });
}

function filterStudents() {
    const deptFilter = document.getElementById('studentDeptFilter').value;
    const divFilter = document.getElementById('studentDivFilter').value;
    const searchText = document.getElementById('studentSearch').value.toLowerCase();

    const rows = document.querySelectorAll('.student-row');

    rows.forEach(row => {
        const deptId = row.dataset.deptId;
        const divId = row.dataset.divId;
        const name = row.dataset.name;
        const roll = row.dataset.roll;

        const deptMatch = !deptFilter || deptId === deptFilter;
        const divMatch = !divFilter || divId === divFilter;
        const searchMatch = name.includes(searchText) || roll.includes(searchText);

        row.style.display = (deptMatch && divMatch && searchMatch) ? 'table-row' : 'none';
    });
}

/**
 * Modal Functions
 */
function editDepartment(deptId, deptName = '', deptCode = '', hodId = '') {
    document.getElementById('deptName').value = deptName;
    document.getElementById('deptCode').value = deptCode;
    document.getElementById('hodId').value = hodId;

    const modal = new bootstrap.Modal(document.getElementById('addDeptModal'));
    modal.show();
}

function deleteDepartment(deptId) {
    if (confirm('Are you sure you want to delete this department? This action cannot be undone.')) {
        console.log('Deleting department:', deptId);
        showLoadingSpinner();

        setTimeout(() => {
            hideLoadingSpinner();
            showAlert('Department deleted successfully!', 'success');
            location.reload();
        }, 1000);
    }
}

function editDivision(divId) {
    console.log('Edit division:', divId);
    const modal = new bootstrap.Modal(document.getElementById('addDivModal'));
    modal.show();
}

function deleteDivision(divId) {
    if (confirm('Are you sure you want to delete this division? This action cannot be undone.')) {
        console.log('Deleting division:', divId);
        showLoadingSpinner();

        setTimeout(() => {
            hideLoadingSpinner();
            showAlert('Division deleted successfully!', 'success');
            location.reload();
        }, 1000);
    }
}

function viewFacultyDetails(facultyId) {
    console.log('View details for faculty:', facultyId);
    const modal = new bootstrap.Modal(document.getElementById('facultyDetailsModal'));
    modal.show();

    // Fetch and display faculty details
    loadFacultyDetails(facultyId);
}

function editFaculty(facultyId, name = '', email = '', deptId = '', phone = '', specialization = '', shortName = '', isHod = false) {
    console.log('Edit faculty:', facultyId);

    document.getElementById('facultyName').value = name;
    document.getElementById('facultyEmail').value = email;
    document.getElementById('facultyDept').value = deptId;
    document.getElementById('facultyPhone').value = phone;
    document.getElementById('facultySpecialization').value = specialization;
    document.getElementById('facultyShortName').value = shortName;
    document.getElementById('isHod').checked = isHod;

    document.querySelector('#addFacultyModal .modal-title').textContent = 'Edit Faculty';

    const modal = new bootstrap.Modal(document.getElementById('addFacultyModal'));
    modal.show();
}

function deleteFaculty(facultyId) {
    if (confirm('Are you sure you want to delete this faculty member?')) {
        console.log('Deleting faculty:', facultyId);
        showLoadingSpinner();
        setTimeout(() => {
            hideLoadingSpinner();
            showAlert('Faculty member deleted successfully!', 'success');
            location.reload();
        }, 1000);
    }
}

function editStudent(studentId, name = '', email = '', roll = '', phone = '', deptId = '', divId = '') {
    console.log('Edit student:', studentId);

    document.getElementById('studentName').value = name;
    document.getElementById('studentEmail').value = email;
    document.getElementById('studentRoll').value = roll;
    document.getElementById('studentPhone').value = phone;
    document.getElementById('studentDept').value = deptId;
    document.getElementById('studentDiv').value = divId;

    document.querySelector('#addStudentModal .modal-title').textContent = 'Edit Student';

    const modal = new bootstrap.Modal(document.getElementById('addStudentModal'));
    modal.show();
}

function deleteStudent(studentId) {
    if (confirm('Are you sure you want to delete this student?')) {
        console.log('Deleting student:', studentId);
        showLoadingSpinner();
        setTimeout(() => {
            hideLoadingSpinner();
            showAlert('Student deleted successfully!', 'success');
            location.reload();
        }, 1000);
    }
}

function viewStudentDetails(studentId) {
    console.log('View details for student:', studentId);
    const modal = new bootstrap.Modal(document.getElementById('studentDetailsModal'));
    modal.show();

    // Fetch and display student details
    loadStudentDetails(studentId);
}

function viewAttendance(studentId) {
    console.log('View attendance for student:', studentId);
    const modal = new bootstrap.Modal(document.getElementById('attendanceModal'));
    modal.show();

    // Fetch and display attendance data
    loadStudentAttendance(studentId);
}

/**
 * Load Faculty Details
 */
function loadFacultyDetails(facultyId) {
    const contentDiv = document.getElementById('facultyDetailsContent');

    // Simulate loading
    contentDiv.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>';

    // Simulate API call
    setTimeout(() => {
        contentDiv.innerHTML = `
            <div class="row">
                <div class="col-md-4 text-center">
                    <img src="https://via.placeholder.com/150" alt="Faculty" class="rounded-circle mb-3" style="width: 150px; height: 150px; object-fit: cover;">
                </div>
                <div class="col-md-8">
                    <h5>Dr. Faculty Name</h5>
                    <p><strong>Faculty ID:</strong> FAC001</p>
                    <p><strong>Department:</strong> Computer Science</p>
                    <p><strong>Email:</strong> faculty@college.edu</p>
                    <p><strong>Phone:</strong> +91-9876543210</p>
                    <p><strong>Specialization:</strong> Web Development</p>
                    <p><strong>Qualifications:</strong> B.Tech, M.Tech, PhD</p>
                    <p><strong>Experience:</strong> 10 years</p>
                </div>
            </div>
        `;
    }, 500);
}

/**
 * Load Student Details
 */
function loadStudentDetails(studentId) {
    const contentDiv = document.getElementById('studentDetailsContent');

    contentDiv.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>';

    setTimeout(() => {
        contentDiv.innerHTML = `
            <div class="row">
                <div class="col-md-4 text-center">
                    <img src="https://via.placeholder.com/150" alt="Student" class="rounded-circle mb-3" style="width: 150px; height: 150px; object-fit: cover;">
                </div>
                <div class="col-md-8">
                    <h5>Student Name</h5>
                    <p><strong>Roll Number:</strong> CSE001</p>
                    <p><strong>Department:</strong> Computer Science</p>
                    <p><strong>Division:</strong> A</p>
                    <p><strong>Email:</strong> student@college.edu</p>
                    <p><strong>Phone:</strong> +91-9876543210</p>
                    <p><strong>Date of Birth:</strong> 01-01-2003</p>
                    <p><strong>Address:</strong> City, State, Postal Code</p>
                    <p><strong>Enrollment Date:</strong> 01-08-2021</p>
                </div>
            </div>
        `;
    }, 500);
}

/**
 * Load Student Attendance
 */
function loadStudentAttendance(studentId) {
    const contentDiv = document.getElementById('attendanceContent');

    contentDiv.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>';

    setTimeout(() => {
        contentDiv.innerHTML = `
            <div class="mb-3">
                <h6>Overall Attendance</h6>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar bg-success" role="progressbar" style="width: 85%">85% Present</div>
                </div>
            </div>
            <div class="table-responsive">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>2024-01-15</td>
                            <td><span class="badge bg-success">Present</span></td>
                        </tr>
                        <tr>
                            <td>2024-01-14</td>
                            <td><span class="badge bg-success">Present</span></td>
                        </tr>
                        <tr>
                            <td>2024-01-13</td>
                            <td><span class="badge bg-danger">Absent</span></td>
                        </tr>
                        <tr>
                            <td>2024-01-12</td>
                            <td><span class="badge bg-success">Present</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
    }, 500);
}

/**
 * Analytics Functions
 */
function updateAnalytics() {
    const dept = document.getElementById('analyticsDeptFilter').value;
    const div = document.getElementById('analyticsDivFilter').value;
    const month = document.getElementById('analyticsMonth').value;

    console.log('Update analytics:', { dept, div, month });
    // Update charts with new data
    showAlert('Analytics updated!', 'info');
}

function generateReport() {
    const dept = document.getElementById('analyticsDeptFilter').value;
    const div = document.getElementById('analyticsDivFilter').value;
    const month = document.getElementById('analyticsMonth').value;

    console.log('Generate report:', { dept, div, month });
    showLoadingSpinner();

    setTimeout(() => {
        hideLoadingSpinner();
        showAlert('Report generated and downloaded!', 'success');
    }, 1500);
}

/**
 * Utility Functions
 */
function formatDate(date) {
    const d = new Date(date);
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}-${month}-${year}`;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function calculatePercentage(value, total) {
    if (total === 0) return 0;
    return ((value / total) * 100).toFixed(2);
}

/**
 * Export Functions
 */
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    const csv = [];

    // Get headers
    const headers = [];
    table.querySelectorAll('thead th').forEach(th => {
        headers.push(th.textContent);
    });
    csv.push(headers.join(','));

    // Get rows
    table.querySelectorAll('tbody tr').forEach(tr => {
        const row = [];
        tr.querySelectorAll('td').forEach(td => {
            row.push('"' + td.textContent.replace(/"/g, '""') + '"');
        });
        csv.push(row.join(','));
    });

    // Download
    const csvContent = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv.join('\n'));
    const link = document.createElement('a');
    link.setAttribute('href', csvContent);
    link.setAttribute('download', filename + '.csv');
    link.click();
}

/**
 * Real-time Validation
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[0-9]{10}$/;
    return re.test(phone.replace(/\D/g, ''));
}

function validateCapacity(capacity) {
    return capacity > 0;
}

// Export functions for use in templates
window.editDepartment = editDepartment;
window.deleteDepartment = deleteDepartment;
window.editDivision = editDivision;
window.deleteDivision = deleteDivision;
window.viewFacultyDetails = viewFacultyDetails;
window.editFaculty = editFaculty;
window.deleteFaculty = deleteFaculty;
window.viewStudentDetails = viewStudentDetails;
window.editStudent = editStudent;
window.deleteStudent = deleteStudent;
window.viewAttendance = viewAttendance;
window.filterByDept = filterByDept;
window.filterFaculty = filterFaculty;
window.filterStudents = filterStudents;
window.updateAnalytics = updateAnalytics;
window.generateReport = generateReport;
window.syncProgressBars = syncProgressBars;

/**
 * Sync Progress Bars
 * Updates width and aria-valuenow from data-now attribute
 * to satisfy template linters and ensure accessibility.
 */
function syncProgressBars() {
    const bars = document.querySelectorAll('.sync-progress');
    bars.forEach(bar => {
        const val = bar.getAttribute('data-now');
        if (val !== null) {
            bar.style.width = val + '%';
            bar.setAttribute('aria-valuenow', val);
        }
    });
}

// Department Selection and Persistence
function selectDepartment() {
    const selector = document.getElementById('deptSelector');
    const deptId = selector.value;
    const deptNames = {
        '1': 'CSE - Computer Science',
        '2': 'ECE - Electronics',
        '3': 'ME - Mechanical'
    };

    // Store selected department in localStorage
    if (deptId) {
        localStorage.setItem('selectedDept', deptId);
        localStorage.setItem('selectedDeptName', deptNames[deptId]);
        document.getElementById('selectedDeptDisplay').textContent = deptNames[deptId];

        // Show department-specific menu items
        document.querySelectorAll('.dept-specific').forEach(el => {
            el.style.display = 'block';
        });

        // Dispatch custom event for pages to listen
        const event = new CustomEvent('departmentSelected', {
            detail: { deptId: deptId, deptName: deptNames[deptId] }
        });
        window.dispatchEvent(event);
    } else {
        localStorage.removeItem('selectedDept');
        localStorage.removeItem('selectedDeptName');
        document.getElementById('selectedDeptDisplay').textContent = 'Select a department';

        // Hide department-specific menu items
        document.querySelectorAll('.dept-specific').forEach(el => {
            el.style.display = 'none';
        });
    }
}

// Load stored department on page load
document.addEventListener('DOMContentLoaded', function () {
    const stored = localStorage.getItem('selectedDept');
    if (stored) {
        document.getElementById('deptSelector').value = stored;
        selectDepartment();
    }
});
