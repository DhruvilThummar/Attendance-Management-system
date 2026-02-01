/**
 * Dashboard Module
 * Handles dashboard rendering with role-based content
 */

// Initialize dashboard
async function initDashboard() {
    const user = AppState.user;
    if (!user) {
        window.location.href = '/login';
        return;
    }

    // Update page title with user name
    const pageTitle = document.querySelector('.page-heading');
    if (pageTitle) {
        pageTitle.textContent = `Welcome, ${user.name}!`;
    }

    // Load dashboard content based on role
    switch (user.role_name) {
        case 'ADMIN':
        case 'HOD':
            await loadAdminDashboard();
            break;
        case 'FACULTY':
            await loadFacultyDashboard();
            break;
        case 'STUDENT':
            await loadStudentDashboard();
            break;
        case 'PARENT':
            await loadParentDashboard();
            break;
    }
}

/**
 * Load Admin/HOD Dashboard
 */
async function loadAdminDashboard() {
    const statsContainer = document.getElementById('stats-container');
    if (!statsContainer) return;

    try {
        showLoading();
        const response = await fetch('/api/dashboard/admin-stats');
        const stats = await response.json();

        statsContainer.innerHTML = `
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card stats-card">
                        <h6>Total Students</h6>
                        <h2 class="text-primary">${stats.total_students || 0}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card success">
                        <h6>Total Faculty</h6>
                        <h2 class="text-success">${stats.total_faculty || 0}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card info">
                        <h6>Active Courses</h6>
                        <h2 class="text-info">${stats.total_subjects || 0}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card warning">
                        <h6>Avg Attendance</h6>
                        <h2 class="text-warning">${stats.avg_attendance || '0'}%</h2>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Attendance Trend (Last 7 Days)</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="attendance-trend-chart"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Low Attendance Alerts</h5>
                        </div>
                        <div class="card-body">
                            <div id="defaulters-list"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Load attendance trend chart
        if (stats.attendance_trend) {
            loadAttendanceTrendChart(stats.attendance_trend);
        }

        // Load defaulters
        loadDefaultersList();

    } catch (error) {
        console.error('Error loading admin dashboard:', error);
        showAlert('Error loading dashboard data', 'danger');
    } finally {
        hideLoading();
    }
}

/**
 * Load Faculty Dashboard
 */
async function loadFacultyDashboard() {
    const statsContainer = document.getElementById('stats-container');
    if (!statsContainer) return;

    try {
        showLoading();
        const response = await fetch('/api/dashboard/faculty-stats');
        const stats = await response.json();

        statsContainer.innerHTML = `
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card stats-card">
                        <h6>Today's Lectures</h6>
                        <h2 class="text-primary">${stats.todays_lectures || 0}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card success">
                        <h6>Completed</h6>
                        <h2 class="text-success">${stats.completed_lectures || 0}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card warning">
                        <h6>Pending</h6>
                        <h2 class="text-warning">${stats.pending_lectures || 0}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card info">
                        <h6>My Students</h6>
                        <h2 class="text-info">${stats.total_students || 0}</h2>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Today's Timetable</h5>
                        </div>
                        <div class="card-body">
                            <div id="todays-timetable"></div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Recent Activity</h5>
                        </div>
                        <div class="card-body">
                            <div id="recent-activity"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        loadTodaysTimetable();
        loadRecentActivity();

    } catch (error) {
        console.error('Error loading faculty dashboard:', error);
        showAlert('Error loading dashboard data', 'danger');
    } finally {
        hideLoading();
    }
}

/**
 * Load Student Dashboard
 */
async function loadStudentDashboard() {
    const statsContainer = document.getElementById('stats-container');
    if (!statsContainer) return;

    try {
        showLoading();
        const response = await fetch('/api/dashboard/student-stats');
        const stats = await response.json();

        const attendanceClass = getAttendanceClass(stats.overall_percentage || 0);

        statsContainer.innerHTML = `
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card stats-card">
                        <h6>Overall Attendance</h6>
                        <h2 class="${attendanceClass}">${stats.overall_percentage || 0}%</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card success">
                        <h6>Total Present</h6>
                        <h2 class="text-success">${stats.total_present || 0}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card danger">
                        <h6>Total Absent</h6>
                        <h2 class="text-danger">${stats.total_absent || 0}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stats-card info">
                        <h6>Total Lectures</h6>
                        <h2 class="text-info">${stats.total_lectures || 0}</h2>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Subject-wise Attendance</h5>
                        </div>
                        <div class="card-body">
                            <canvas id="subject-attendance-chart"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Today's Timetable</h5>
                        </div>
                        <div class="card-body">
                            <div id="todays-timetable"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        if (stats.subject_wise) {
            loadSubjectAttendanceChart(stats.subject_wise);
        }

        loadTodaysTimetable();

    } catch (error) {
        console.error('Error loading student dashboard:', error);
        showAlert('Error loading dashboard data', 'danger');
    } finally {
        hideLoading();
    }
}

/**
 * Load Parent Dashboard
 */
async function loadParentDashboard() {
    const statsContainer = document.getElementById('stats-container');
    if (!statsContainer) return;

    try {
        showLoading();
        const response = await fetch('/api/dashboard/parent-stats');
        const students = await response.json();

        statsContainer.innerHTML = `
            <div class="row">
                ${students.map(student => `
                    <div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-header bg-primary text-white">
                                <h5 class="mb-0">${student.name}</h5>
                            </div>
                            <div class="card-body">
                                <div class="row text-center mb-3">
                                    <div class="col-4">
                                        <h6 class="text-muted">Attendance</h6>
                                        <h3 class="${getAttendanceClass(student.attendance_percentage)}">${student.attendance_percentage}%</h3>
                                    </div>
                                    <div class="col-4">
                                        <h6 class="text-muted">Present</h6>
                                        <h3 class="text-success">${student.present}</h3>
                                    </div>
                                    <div class="col-4">
                                        <h6 class="text-muted">Absent</h6>
                                        <h3 class="text-danger">${student.absent}</h3>
                                    </div>
                                </div>
                                <a href="/student-attendance?student_id=${student.student_id}" class="btn btn-primary btn-sm">View Details</a>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

    } catch (error) {
        console.error('Error loading parent dashboard:', error);
        showAlert('Error loading dashboard data', 'danger');
    } finally {
        hideLoading();
    }
}

// Helper functions for dashboard
function loadAttendanceTrendChart(data) {
    const ctx = document.getElementById('attendance-trend-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Attendance %',
                data: data.values,
                borderColor: '#4e73df',
                backgroundColor: 'rgba(78, 115, 223, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

function loadSubjectAttendanceChart(data) {
    const ctx = document.getElementById('subject-attendance-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Attendance %',
                data: data.values,
                backgroundColor: '#4e73df'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

async function loadDefaultersList() {
    const container = document.getElementById('defaulters-list');
    if (!container) return;

    try {
        const response = await fetch('/api/reports/defaulters?threshold=75');
        const defaulters = await response.json();

        if (defaulters.length === 0) {
            container.innerHTML = '<p class="text-muted">No defaulters found</p>';
            return;
        }

        container.innerHTML = defaulters.map(student => `
            <div class="student-row">
                <div class="student-info">
                    <div class="student-name">${student.name}</div>
                    <div class="student-details">${student.enrollment_no} - ${student.division_name}</div>
                </div>
                <div class="text-danger fw-bold">${student.attendance_percentage}%</div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Error loading defaulters:', error);
    }
}

async function loadTodaysTimetable() {
    const container = document.getElementById('todays-timetable');
    if (!container) return;

    try {
        const response = await fetch('/api/timetable/today');
        const lectures = await response.json();

        if (lectures.length === 0) {
            container.innerHTML = '<p class="text-muted">No lectures scheduled for today</p>';
            return;
        }

        container.innerHTML = `
            <div class="list-group">
                ${lectures.map(lecture => `
                    <div class="list-group-item">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="mb-1">${lecture.subject_name}</h6>
                                <small class="text-muted">${lecture.faculty_name} - ${lecture.room_no}</small>
                            </div>
                            <div class="text-end">
                                <small>${formatTime(lecture.start_time)} - ${formatTime(lecture.end_time)}</small>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

    } catch (error) {
        console.error('Error loading timetable:', error);
    }
}

async function loadRecentActivity() {
    const container = document.getElementById('recent-activity');
    if (!container) return;

    try {
        const response = await fetch('/api/dashboard/recent-activity');
        const activities = await response.json();

        if (activities.length === 0) {
            container.innerHTML = '<p class="text-muted">No recent activity</p>';
            return;
        }

        container.innerHTML = `
            <div class="list-group">
                ${activities.map(activity => `
                    <div class="list-group-item">
                        <div class="d-flex justify-content-between">
                            <div>
                                <small>${activity.description}</small>
                            </div>
                            <small class="text-muted">${formatDate(activity.created_at)}</small>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

    } catch (error) {
        console.error('Error loading recent activity:', error);
    }
}

// Initialize dashboard on page load
if (document.getElementById('stats-container')) {
    initDashboard();
}
