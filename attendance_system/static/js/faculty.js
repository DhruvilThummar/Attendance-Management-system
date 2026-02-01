/**
 * Faculty Management Module
 * Handles faculty CRUD operations and approval workflow
 */

class FacultyManager {
    constructor() {
        this.faculty = [];
        this.currentPage = 1;
        this.perPage = 10;
        this.filters = {
            department: '',
            status: 'all',
            search: ''
        };
    }

    async init() {
        await this.loadDepartments();
        await this.loadFaculty();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Search
        const searchInput = document.getElementById('facultySearch');
        if (searchInput) {
            searchInput.addEventListener('input', window.debounce(() => {
                this.filters.search = searchInput.value;
                this.currentPage = 1;
                this.loadFaculty();
            }, 300));
        }

        // Filters
        ['department', 'status'].forEach(filter => {
            const select = document.getElementById(`${filter}Filter`);
            if (select) {
                select.addEventListener('change', (e) => {
                    this.filters[filter] = e.target.value;
                    this.currentPage = 1;
                    this.loadFaculty();
                });
            }
        });

        // Add faculty button
        const addBtn = document.getElementById('addFacultyBtn');
        if (addBtn) {
            addBtn.addEventListener('click', () => this.showAddFacultyModal());
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

    async loadFaculty() {
        try {
            window.showLoading();
            const params = new URLSearchParams({
                page: this.currentPage,
                per_page: this.perPage,
                ...this.filters
            });

            const data = await window.apiRequest(`/api/faculty?${params}`);
            this.faculty = data.faculty;
            this.totalFaculty = data.total;
            
            this.renderFaculty();
            this.renderPagination();
        } catch (error) {
            window.showAlert('Error loading faculty', 'danger');
            console.error(error);
        } finally {
            window.hideLoading();
        }
    }

    renderFaculty() {
        const container = document.getElementById('facultyContainer');
        if (!container) return;

        if (this.faculty.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="bi bi-person-workspace"></i>
                    <h3>No Faculty Found</h3>
                    <p>No faculty members match your search criteria</p>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="row">
                ${this.faculty.map(f => this.renderFacultyCard(f)).join('')}
            </div>
        `;
    }

    renderFacultyCard(faculty) {
        const statusBadge = this.getStatusBadge(faculty.status);
        
        return `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100 faculty-card">
                    <div class="card-body">
                        <div class="text-center mb-3">
                            <div class="faculty-avatar mx-auto">
                                ${faculty.name.charAt(0).toUpperCase()}
                            </div>
                            <h5 class="mt-3 mb-1">${faculty.name}</h5>
                            <p class="text-muted small mb-2">${faculty.email}</p>
                            ${statusBadge}
                        </div>
                        
                        <hr>
                        
                        <div class="faculty-details">
                            <p class="mb-2">
                                <i class="bi bi-building me-2 text-primary"></i>
                                <strong>Department:</strong> ${faculty.department_name || '-'}
                            </p>
                            <p class="mb-2">
                                <i class="bi bi-phone me-2 text-primary"></i>
                                <strong>Phone:</strong> ${faculty.phone || '-'}
                            </p>
                            <p class="mb-2">
                                <i class="bi bi-calendar-event me-2 text-primary"></i>
                                <strong>Joined:</strong> ${window.formatDate(faculty.created_at)}
                            </p>
                        </div>

                        <div class="btn-group w-100 mt-3">
                            <button class="btn btn-sm btn-outline-primary" onclick="facultyManager.viewFaculty(${faculty.id})">
                                <i class="bi bi-eye"></i> View
                            </button>
                            <button class="btn btn-sm btn-outline-warning" onclick="facultyManager.editFaculty(${faculty.id})">
                                <i class="bi bi-pencil"></i> Edit
                            </button>
                            ${faculty.status === 'pending' ? `
                                <button class="btn btn-sm btn-outline-success" onclick="facultyManager.approveFaculty(${faculty.id})">
                                    <i class="bi bi-check-circle"></i> Approve
                                </button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getStatusBadge(status) {
        const badges = {
            active: '<span class="badge bg-success">Active</span>',
            pending: '<span class="badge bg-warning">Pending Approval</span>',
            inactive: '<span class="badge bg-secondary">Inactive</span>',
            suspended: '<span class="badge bg-danger">Suspended</span>'
        };
        return badges[status] || badges.pending;
    }

    renderPagination() {
        const container = document.getElementById('paginationContainer');
        if (!container) return;

        const totalPages = Math.ceil(this.totalFaculty / this.perPage);
        if (totalPages <= 1) {
            container.innerHTML = '';
            return;
        }

        let html = '<nav><ul class="pagination justify-content-center">';
        
        html += `
            <li class="page-item ${this.currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="facultyManager.goToPage(${this.currentPage - 1}); return false;">
                    Previous
                </a>
            </li>
        `;

        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= this.currentPage - 2 && i <= this.currentPage + 2)) {
                html += `
                    <li class="page-item ${i === this.currentPage ? 'active' : ''}">
                        <a class="page-link" href="#" onclick="facultyManager.goToPage(${i}); return false;">${i}</a>
                    </li>
                `;
            }
        }

        html += `
            <li class="page-item ${this.currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="facultyManager.goToPage(${this.currentPage + 1}); return false;">
                    Next
                </a>
            </li>
        `;

        html += '</ul></nav>';
        container.innerHTML = html;
    }

    goToPage(page) {
        const totalPages = Math.ceil(this.totalFaculty / this.perPage);
        if (page < 1 || page > totalPages) return;
        
        this.currentPage = page;
        this.loadFaculty();
    }

    async viewFaculty(id) {
        window.showAlert('View faculty feature coming soon', 'info');
    }

    async editFaculty(id) {
        window.showAlert('Edit faculty feature coming soon', 'info');
    }

    async approveFaculty(id) {
        if (!confirm('Are you sure you want to approve this faculty member?')) return;

        try {
            await window.apiRequest(`/api/faculty/${id}/approve`, { method: 'POST' });
            window.showAlert('Faculty approved successfully', 'success');
            this.loadFaculty();
        } catch (error) {
            window.showAlert('Error approving faculty', 'danger');
        }
    }

    showAddFacultyModal() {
        window.showAlert('Add faculty feature coming soon', 'info');
    }
}

// Initialize on page load
let facultyManager;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        facultyManager = new FacultyManager();
        facultyManager.init();
    });
} else {
    facultyManager = new FacultyManager();
    facultyManager.init();
}
