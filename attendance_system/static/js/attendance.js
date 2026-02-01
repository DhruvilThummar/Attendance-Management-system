/**
 * Attendance Marking Module
 * Handles lecture-wise attendance marking by faculty
 */

class AttendanceMarker {
    constructor() {
        this.lectureId = null;
        this.students = [];
        this.attendance = {};
    }

    async init(lectureId) {
        this.lectureId = lectureId;
        await this.loadLectureDetails();
        await this.loadStudents();
        this.setupEventListeners();
    }

    async loadLectureDetails() {
        try {
            const lecture = await window.apiRequest(`/api/lectures/${this.lectureId}`);
            this.renderLectureHeader(lecture);
        } catch (error) {
            window.showAlert('Error loading lecture details', 'danger');
        }
    }

    async loadStudents() {
        try {
            window.showLoading();
            const data = await window.apiRequest(`/api/lectures/${this.lectureId}/students`);
            this.students = data.students;
            
            // Load existing attendance if any
            if (data.attendance) {
                this.attendance = data.attendance;
            }
            
            this.renderStudents();
            this.updateSummary();
        } catch (error) {
            window.showAlert('Error loading students', 'danger');
        } finally {
            window.hideLoading();
        }
    }

    renderLectureHeader(lecture) {
        const container = document.getElementById('lectureInfo');
        if (!container) return;

        container.innerHTML = `
            <div class="lecture-detail">
                <div class="lecture-detail-label">Subject</div>
                <div class="lecture-detail-value">${lecture.subject_name}</div>
            </div>
            <div class="lecture-detail">
                <div class="lecture-detail-label">Division</div>
                <div class="lecture-detail-value">${lecture.division_name}</div>
            </div>
            <div class="lecture-detail">
                <div class="lecture-detail-label">Time</div>
                <div class="lecture-detail-value">${lecture.start_time} - ${lecture.end_time}</div>
            </div>
            <div class="lecture-detail">
                <div class="lecture-detail-label">Date</div>
                <div class="lecture-detail-value">${window.formatDate(lecture.date)}</div>
            </div>
        `;
    }

    renderStudents() {
        const container = document.getElementById('studentsGrid');
        if (!container) return;

        container.innerHTML = this.students.map(student => {
            const status = this.attendance[student.id] || 'unmarked';
            return `
                <div class="student-card ${status}" data-student-id="${student.id}">
                    <div class="student-header">
                        <div class="student-avatar">
                            ${student.name.charAt(0).toUpperCase()}
                        </div>
                        <div class="student-details">
                            <div class="student-name">${student.name}</div>
                            <div class="student-meta">
                                Roll No: ${student.roll_no} | Enrollment: ${student.enrollment_no}
                            </div>
                        </div>
                    </div>
                    <div class="attendance-toggle-group">
                        <button class="attendance-btn ${status === 'present' ? 'present' : ''}" 
                                onclick="attendanceMarker.markAttendance(${student.id}, 'present')">
                            <i class="bi bi-check-circle"></i> Present
                        </button>
                        <button class="attendance-btn ${status === 'absent' ? 'absent' : ''}"
                                onclick="attendanceMarker.markAttendance(${student.id}, 'absent')">
                            <i class="bi bi-x-circle"></i> Absent
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    markAttendance(studentId, status) {
        this.attendance[studentId] = status;
        this.renderStudents();
        this.updateSummary();
    }

    setupEventListeners() {
        // Mark all present
        const markAllPresentBtn = document.getElementById('markAllPresent');
        if (markAllPresentBtn) {
            markAllPresentBtn.addEventListener('click', () => {
                this.students.forEach(student => {
                    this.attendance[student.id] = 'present';
                });
                this.renderStudents();
                this.updateSummary();
            });
        }

        // Mark all absent
        const markAllAbsentBtn = document.getElementById('markAllAbsent');
        if (markAllAbsentBtn) {
            markAllAbsentBtn.addEventListener('click', () => {
                this.students.forEach(student => {
                    this.attendance[student.id] = 'absent';
                });
                this.renderStudents();
                this.updateSummary();
            });
        }

        // Save attendance
        const saveBtn = document.getElementById('saveAttendance');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveAttendance());
        }
    }

    updateSummary() {
        const total = this.students.length;
        const present = Object.values(this.attendance).filter(s => s === 'present').length;
        const absent = Object.values(this.attendance).filter(s => s === 'absent').length;
        const percentage = total > 0 ? (present / total * 100).toFixed(1) : 0;

        document.getElementById('totalStudents').textContent = total;
        document.getElementById('presentCount').textContent = present;
        document.getElementById('absentCount').textContent = absent;
        document.getElementById('attendancePercentage').textContent = percentage + '%';
    }

    async saveAttendance() {
        try {
            const unmarked = this.students.filter(s => !this.attendance[s.id]);
            
            if (unmarked.length > 0) {
                if (!confirm(`${unmarked.length} student(s) are unmarked. Do you want to continue?`)) {
                    return;
                }
            }

            window.showLoading();
            
            await window.apiRequest(`/api/lectures/${this.lectureId}/attendance`, {
                method: 'POST',
                body: JSON.stringify({ attendance: this.attendance })
            });

            window.showAlert('Attendance saved successfully', 'success');
            
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1500);
        } catch (error) {
            window.showAlert('Error saving attendance', 'danger');
        } finally {
            window.hideLoading();
        }
    }
}

// Initialize on page load
let attendanceMarker;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        // Get lecture ID from URL or data attribute
        const lectureId = document.getElementById('attendanceContainer')?.dataset.lectureId;
        if (lectureId) {
            attendanceMarker = new AttendanceMarker();
            attendanceMarker.init(lectureId);
        }
    });
} else {
    const lectureId = document.getElementById('attendanceContainer')?.dataset.lectureId;
    if (lectureId) {
        attendanceMarker = new AttendanceMarker();
        attendanceMarker.init(lectureId);
    }
}
