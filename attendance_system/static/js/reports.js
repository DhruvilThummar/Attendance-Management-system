/**
 * Reports Generation Module
 * Handles various attendance reports with charts and export
 */

class ReportsGenerator {
    constructor() {
        this.currentReport = null;
        this.filters = {
            reportType: 'daily',
            division: '',
            semester: '',
            subject: '',
            dateFrom: '',
            dateTo: '',
            threshold: 75
        };
    }

    async init() {
        await this.loadFilters();
        this.setupEventListeners();
        this.selectReportType('daily');
    }

    async loadFilters() {
        try {
            const [divisions, semesters, subjects] = await Promise.all([
                window.apiRequest('/api/divisions'),
                window.apiRequest('/api/semesters'),
                window.apiRequest('/api/subjects')
            ]);
            
            this.populateFilters(divisions, semesters, subjects);
        } catch (error) {
            console.error('Error loading filters:', error);
        }
    }

    populateFilters(divisions, semesters, subjects) {
        const divisionSelect = document.getElementById('divisionFilter');
        const semesterSelect = document.getElementById('semesterFilter');
        const subjectSelect = document.getElementById('subjectFilter');

        if (divisionSelect) {
            divisionSelect.innerHTML = '<option value="">All Divisions</option>';
            divisions.forEach(div => {
                divisionSelect.innerHTML += `<option value="${div.id}">${div.name}</option>`;
            });
        }

        if (semesterSelect) {
            semesterSelect.innerHTML = '<option value="">All Semesters</option>';
            semesters.forEach(sem => {
                semesterSelect.innerHTML += `<option value="${sem.id}">${sem.name}</option>`;
            });
        }

        if (subjectSelect) {
            subjectSelect.innerHTML = '<option value="">All Subjects</option>';
            subjects.forEach(sub => {
                subjectSelect.innerHTML += `<option value="${sub.id}">${sub.name}</option>`;
            });
        }
    }

    setupEventListeners() {
        // Report type selection
        document.querySelectorAll('.report-type-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const type = e.currentTarget.dataset.reportType;
                this.selectReportType(type);
            });
        });

        // Filter changes
        Object.keys(this.filters).forEach(filter => {
            const input = document.getElementById(`${filter}Filter`);
            if (input) {
                input.addEventListener('change', (e) => {
                    this.filters[filter] = e.target.value;
                });
            }
        });

        // Generate report button
        const generateBtn = document.getElementById('generateReport');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => this.generateReport());
        }

        // Export buttons
        document.getElementById('exportPdf')?.addEventListener('click', () => this.exportReport('pdf'));
        document.getElementById('exportExcel')?.addEventListener('click', () => this.exportReport('excel'));
        document.getElementById('printReport')?.addEventListener('click', () => window.print());
    }

    selectReportType(type) {
        this.filters.reportType = type;
        
        // Update UI
        document.querySelectorAll('.report-type-card').forEach(card => {
            card.classList.toggle('active', card.dataset.reportType === type);
        });
    }

    async generateReport() {
        try {
            window.showLoading();
            
            const endpoint = this.getReportEndpoint();
            const params = new URLSearchParams(this.filters);
            
            const data = await window.apiRequest(`${endpoint}?${params}`);
            this.currentReport = data;
            
            this.renderReport(data);
        } catch (error) {
            window.showAlert('Error generating report', 'danger');
        } finally {
            window.hideLoading();
        }
    }

    getReportEndpoint() {
        const endpoints = {
            daily: '/api/reports/daily',
            weekly: '/api/reports/weekly',
            monthly: '/api/reports/monthly',
            defaulters: '/api/reports/defaulters',
            subjectWise: '/api/reports/subject-wise',
            divisionWise: '/api/reports/division-wise'
        };
        return endpoints[this.filters.reportType] || endpoints.daily;
    }

    renderReport(data) {
        const container = document.getElementById('reportContent');
        if (!container) return;

        switch (this.filters.reportType) {
            case 'daily':
            case 'weekly':
            case 'monthly':
                this.renderPeriodReport(data);
                break;
            case 'defaulters':
                this.renderDefaultersReport(data);
                break;
            case 'subjectWise':
                this.renderSubjectWiseReport(data);
                break;
            case 'divisionWise':
                this.renderDivisionWiseReport(data);
                break;
        }
    }

    renderPeriodReport(data) {
        const container = document.getElementById('reportBody');
        if (!container) return;

        container.innerHTML = `
            <div class="chart-container">
                <div class="chart-title">Attendance Trend</div>
                <canvas id="trendChart"></canvas>
            </div>
            
            <div class="table-responsive mt-4">
                <table class="report-table">
                    <thead>
                        <tr>
                            <th>Student</th>
                            <th>Total Lectures</th>
                            <th>Present</th>
                            <th>Absent</th>
                            <th>Percentage</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.students.map(s => `
                            <tr>
                                <td>${s.name}</td>
                                <td>${s.total_lectures}</td>
                                <td>${s.present}</td>
                                <td>${s.absent}</td>
                                <td>
                                    <span class="attendance-badge ${this.getAttendanceLevel(s.percentage)}">
                                        ${s.percentage.toFixed(1)}%
                                    </span>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;

        this.renderTrendChart(data.trend);
    }

    renderDefaultersReport(data) {
        const container = document.getElementById('reportBody');
        if (!container) return;

        if (!data.defaulters || data.defaulters.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="bi bi-emoji-smile"></i>
                    <h3>No Defaulters Found!</h3>
                    <p>All students are meeting the minimum attendance requirement</p>
                </div>
            `;
            return;
        }

        container.innerHTML = data.defaulters.map(student => `
            <div class="defaulter-card">
                <div class="defaulter-header">
                    <div class="defaulter-name">${student.name}</div>
                    <div class="defaulter-percentage">${student.percentage.toFixed(1)}%</div>
                </div>
                <div class="defaulter-details">
                    <div class="detail-item">
                        <i class="bi bi-person-badge"></i>
                        <span>Roll: ${student.roll_no}</span>
                    </div>
                    <div class="detail-item">
                        <i class="bi bi-building"></i>
                        <span>${student.division_name}</span>
                    </div>
                    <div class="detail-item">
                        <i class="bi bi-clipboard-check"></i>
                        <span>${student.present}/${student.total_lectures} Present</span>
                    </div>
                    <div class="detail-item">
                        <i class="bi bi-envelope"></i>
                        <span>${student.email}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }

    renderSubjectWiseReport(data) {
        const container = document.getElementById('reportBody');
        if (!container) return;

        container.innerHTML = `
            <div class="chart-container">
                <div class="chart-title">Subject-wise Attendance</div>
                <canvas id="subjectChart"></canvas>
            </div>
            
            <div class="table-responsive mt-4">
                <table class="report-table">
                    <thead>
                        <tr>
                            <th>Subject</th>
                            <th>Faculty</th>
                            <th>Total Lectures</th>
                            <th>Avg Attendance</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.subjects.map(s => `
                            <tr>
                                <td>${s.subject_name}</td>
                                <td>${s.faculty_name}</td>
                                <td>${s.total_lectures}</td>
                                <td>
                                    <span class="attendance-badge ${this.getAttendanceLevel(s.avg_attendance)}">
                                        ${s.avg_attendance.toFixed(1)}%
                                    </span>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;

        this.renderSubjectChart(data.subjects);
    }

    renderDivisionWiseReport(data) {
        const container = document.getElementById('reportBody');
        if (!container) return;

        container.innerHTML = `
            <div class="chart-container">
                <div class="chart-title">Division-wise Attendance Comparison</div>
                <canvas id="divisionChart"></canvas>
            </div>
        `;

        this.renderDivisionChart(data.divisions);
    }

    renderTrendChart(trendData) {
        const ctx = document.getElementById('trendChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: trendData.map(d => d.date),
                datasets: [{
                    label: 'Attendance %',
                    data: trendData.map(d => d.percentage),
                    borderColor: '#4e73df',
                    backgroundColor: 'rgba(78, 115, 223, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    renderSubjectChart(subjects) {
        const ctx = document.getElementById('subjectChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: subjects.map(s => s.subject_name),
                datasets: [{
                    label: 'Average Attendance %',
                    data: subjects.map(s => s.avg_attendance),
                    backgroundColor: '#4e73df'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    renderDivisionChart(divisions) {
        const ctx = document.getElementById('divisionChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: divisions.map(d => d.division_name),
                datasets: [{
                    label: 'Average Attendance %',
                    data: divisions.map(d => d.avg_attendance),
                    backgroundColor: '#1cc88a'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    getAttendanceLevel(percentage) {
        if (percentage >= 85) return 'high';
        if (percentage >= 75) return 'medium';
        return 'low';
    }

    async exportReport(format) {
        try {
            window.showLoading();
            
            const params = new URLSearchParams({
                ...this.filters,
                format
            });
            
            const response = await fetch(`/api/reports/export?${params}`);
            const blob = await response.blob();
            
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `report_${this.filters.reportType}_${Date.now()}.${format}`;
            a.click();
            
            window.showAlert(`Report exported as ${format.toUpperCase()}`, 'success');
        } catch (error) {
            window.showAlert(`Error exporting report`, 'danger');
        } finally {
            window.hideLoading();
        }
    }
}

// Initialize on page load
let reportsGenerator;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        reportsGenerator = new ReportsGenerator();
        reportsGenerator.init();
    });
} else {
    reportsGenerator = new ReportsGenerator();
    reportsGenerator.init();
}
