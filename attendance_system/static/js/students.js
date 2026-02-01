/**
 * Students Management Module
 * Handles student CRUD operations, search, and pagination
 */

class StudentsManager {
    constructor() {
        this.students = [];
        this.currentPage = 1;
        this.perPage = 10;
        this.totalStudents = 0;
        this.filters = {
            department: '',
            division: '',
            semester: '',
            search: ''
        };
    }

    async init() {
        await this.loadDepartments();
        await this.loadStudents();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Search
        const searchInput = document.getElementById('studentSearch');
        if (searchInput) {
            searchInput.addEventListener('input', window.debounce(() => {
                this.filters.search = searchInput.value;
                this.currentPage = 1;
                this.loadStudents();
            }, 300));
        }

        // Filters
        ['department', 'division', 'semester'].forEach(filter => {
            const select = document.getElementById(`${filter}Filter`);
            if (select) {
                select.addEventListener('change', (e) => {
                    this.filters[filter] = e.target.value;
                    this.currentPage = 1;
                    this.loadStudents();
                });
            }
        });

        // Add student button
        const addBtn = document.getElementById('addStudentBtn');
        if (addBtn) {
            addBtn.addEventListener('click', () => this.showAddStudentModal());
        }
    }

    async loadDepartments() {
        try {
            const data = await window.apiRequest('/api/departments');
            const select = document.getElementById('departmentFilter');
            if (select) {
                select.innerHTML = '<option value="">All Departments</option>';
                data.forEach(dept => {
                    select.innerHTML += `<option value="${dept.id}">${dept.name}</option>`;
                });
            }
        } catch (error) {
            console.error('Error loading departments:', error);
        }
    }

    async loadStudents() {
        try {
            window.showLoading();
            const params = new URLSearchParams({
                page: this.currentPage,
                per_page: this.perPage,
                ...this.filters
            });

            const data = await window.apiRequest(`/api/students?${params}`);
            this.students = data.students;
            this.totalStudents = data.total;
            
            this.renderStudents();
            this.renderPagination();
        } catch (error) {
            window.showAlert('Error loading students', 'danger');
            console.error(error);
        } finally {
            window.hideLoading();
        }
    }

    renderStudents() {
        const container = document.getElementById('studentsContainer');
        if (!container) return;

        if (this.students.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="bi bi-people"></i>
                    <h3>No Students Found</h3>
                    <p>No students match your search criteria</p>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Roll No</th>
                            <th>Name</th>
                            <th>Enrollment</th>
                            <th>Division</th>
                            <th>Semester</th>
                            <th>Attendance</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.students.map(student => this.renderStudentRow(student)).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    renderStudentRow(student) {
        const attendanceClass = window.getAttendanceClass(student.attendance_percentage || 0);
        
        return `
            <tr>
                <td>${student.roll_no}</td>
                <td>
                    <div class="d-flex align-items-center">
                        <div class="student-avatar me-2">
                            ${student.name.charAt(0).toUpperCase()}
                        </div>
                        <div>
                            <strong>${student.name}</strong>
                            <br><small class="text-muted">${student.email}</small>
                        </div>
                    </div>
                </td>
                <td>${student.enrollment_no}</td>
                <td>${student.division_name || '-'}</td>
                <td>${student.semester_name || '-'}</td>
                <td>
                    <span class="badge bg-${attendanceClass}">
                        ${(student.attendance_percentage || 0).toFixed(1)}%
                    </span>
                </td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="studentsManager.viewStudent(${student.id})">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-outline-warning" onclick="studentsManager.editStudent(${student.id})">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="studentsManager.deleteStudent(${student.id})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }

    renderPagination() {
        const container = document.getElementById('paginationContainer');
        if (!container) return;

        const totalPages = Math.ceil(this.totalStudents / this.perPage);
        if (totalPages <= 1) {
            container.innerHTML = '';
            return;
        }

        let html = '<nav><ul class="pagination justify-content-center">';
        
        // Previous button
        html += `
            <li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="studentsManager.goToPage(${this.currentPage - 1}); return false;">
                    Previous
                </a>
            </li>
        `;

        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= this.currentPage - 2 && i <= this.currentPage + 2)) {
                html += `
                    <li class="page-item ${i === this.currentPage ? 'active' : ''}">
                        <a class="page-link" href="#" onclick="studentsManager.goToPage(${i}); return false;">${i}</a>
                    </li>
                `;
            } else if (i === this.currentPage - 3 || i === this.currentPage + 3) {
                html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
            }
        }

        // Next button
        html += `
            <li class="page-item ${this.currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="studentsManager.goToPage(${this.currentPage + 1}); return false;">
                    Next
                </a>
            </li>
        `;

        html += '</ul></nav>';
        container.innerHTML = html;
    }

    goToPage(page) {
        const totalPages = Math.ceil(this.totalStudents / this.perPage);
        if (page < 1 || page > totalPages) return;
        
        this.currentPage = page;
        this.loadStudents();
    }

    async viewStudent(id) {
        try {
            const student = await window.apiRequest(`/api/students/${id}`);
            this.showStudentDetailsModal(student);
        } catch (error) {
            window.showAlert('Error loading student details', 'danger');
        }
    }

    async editStudent(id) {
        try {
            const student = await window.apiRequest(`/api/students/${id}`);
            this.showEditStudentModal(student);
        } catch (error) {
            window.showAlert('Error loading student', 'danger');
        }
    }

    async deleteStudent(id) {
        if (!confirm('Are you sure you want to delete this student?')) return;

        try {
            await window.apiRequest(`/api/students/${id}`, { method: 'DELETE' });
            window.showAlert('Student deleted successfully', 'success');
            this.loadStudents();
        } catch (error) {
            window.showAlert('Error deleting student', 'danger');
        }
    }

    showAddStudentModal() {
        // Modal implementation
        window.showAlert('Add student feature coming soon', 'info');
    }

    showEditStudentModal(student) {
        // Modal implementation
        window.showAlert('Edit student feature coming soon', 'info');
    }

    showStudentDetailsModal(student) {
        // Modal implementation
        window.showAlert('Student details feature coming soon', 'info');
    }
}

// Initialize on page load
let studentsManager;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        studentsManager = new StudentsManager();
        studentsManager.init();
    });
} else {
    studentsManager = new StudentsManager();
    studentsManager.init();
}
