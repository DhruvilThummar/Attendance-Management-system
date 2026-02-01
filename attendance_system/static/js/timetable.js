/**
 * Timetable Management Module
 * Handles timetable CRUD operations and visualization
 */

class TimetableManager {
    constructor() {
        this.timetable = [];
        this.currentWeek = this.getCurrentWeek();
        this.filters = {
            division: '',
            semester: '',
            faculty: ''
        };
    }

    async init() {
        await this.loadFilters();
        await this.loadTimetable();
        this.setupEventListeners();
    }

    getCurrentWeek() {
        const today = new Date();
        const firstDay = new Date(today.setDate(today.getDate() - today.getDay() + 1));
        return firstDay;
    }

    async loadFilters() {
        try {
            // Load divisions, semesters, faculty based on user role
            if (window.AppState?.user?.role_name === 'ADMIN' || window.AppState?.user?.role_name === 'HOD') {
                const [divisions, semesters] = await Promise.all([
                    window.apiRequest('/api/divisions'),
                    window.apiRequest('/api/semesters')
                ]);
                this.populateFilters(divisions, semesters);
            }
        } catch (error) {
            console.error('Error loading filters:', error);
        }
    }

    populateFilters(divisions, semesters) {
        const divisionSelect = document.getElementById('divisionFilter');
        const semesterSelect = document.getElementById('semesterFilter');

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
    }

    async loadTimetable() {
        try {
            window.showLoading();
            const params = new URLSearchParams(this.filters);
            params.append('week_start', this.currentWeek.toISOString().split('T')[0]);

            const data = await window.apiRequest(`/api/timetable?${params}`);
            this.timetable = data.timetable;
            
            this.renderTimetable();
        } catch (error) {
            window.showAlert('Error loading timetable', 'danger');
        } finally {
            window.hideLoading();
        }
    }

    renderTimetable() {
        const container = document.getElementById('timetableGrid');
        if (!container) return;

        const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        const timeSlots = this.generateTimeSlots();

        let html = `
            <div class="timetable-grid">
                <div class="time-slot"><i class="bi bi-clock"></i><span>Time</span></div>
                ${days.map(day => `<div class="day-header">${day}</div>`).join('')}
        `;

        timeSlots.forEach(slot => {
            html += `<div class="time-slot">${slot.start}<br>${slot.end}</div>`;
            
            days.forEach(day => {
                const lecture = this.findLecture(day, slot.start);
                html += this.renderLectureCell(lecture, day, slot);
            });
        });

        html += '</div>';
        container.innerHTML = html;
    }

    generateTimeSlots() {
        return [
            { start: '09:00', end: '10:00' },
            { start: '10:00', end: '11:00' },
            { start: '11:00', end: '12:00' },
            { start: '12:00', end: '13:00' },
            { start: '13:00', end: '14:00' },
            { start: '14:00', end: '15:00' },
            { start: '15:00', end: '16:00' },
            { start: '16:00', end: '17:00' }
        ];
    }

    findLecture(day, time) {
        return this.timetable.find(l => 
            l.day_of_week.toLowerCase() === day.toLowerCase() && 
            l.start_time === time
        );
    }

    renderLectureCell(lecture, day, slot) {
        if (!lecture) {
            return `
                <div class="lecture-cell empty" onclick="timetableManager.addLecture('${day}', '${slot.start}', '${slot.end}')">
                    <button class="add-lecture-btn">
                        <i class="bi bi-plus-circle"></i> Add Lecture
                    </button>
                </div>
            `;
        }

        return `
            <div class="lecture-cell has-lecture" data-lecture-id="${lecture.id}">
                <div class="lecture-info">
                    <div class="lecture-subject">${lecture.subject_name}</div>
                    <div class="lecture-faculty">
                        <i class="bi bi-person"></i> ${lecture.faculty_name}
                    </div>
                    <div class="lecture-room">
                        <i class="bi bi-geo-alt"></i> ${lecture.room || 'TBA'}
                    </div>
                    <div class="lecture-time">${lecture.start_time} - ${lecture.end_time}</div>
                </div>
                <div class="lecture-actions">
                    <button class="lecture-action-btn edit" onclick="timetableManager.editLecture(${lecture.id})">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="lecture-action-btn delete" onclick="timetableManager.deleteLecture(${lecture.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        `;
    }

    setupEventListeners() {
        // Filter changes
        ['division', 'semester', 'faculty'].forEach(filter => {
            const select = document.getElementById(`${filter}Filter`);
            if (select) {
                select.addEventListener('change', (e) => {
                    this.filters[filter] = e.target.value;
                    this.loadTimetable();
                });
            }
        });

        // Week navigation
        const prevWeekBtn = document.getElementById('prevWeek');
        const nextWeekBtn = document.getElementById('nextWeek');

        if (prevWeekBtn) {
            prevWeekBtn.addEventListener('click', () => {
                this.currentWeek.setDate(this.currentWeek.getDate() - 7);
                this.loadTimetable();
                this.updateWeekDisplay();
            });
        }

        if (nextWeekBtn) {
            nextWeekBtn.addEventListener('click', () => {
                this.currentWeek.setDate(this.currentWeek.getDate() + 7);
                this.loadTimetable();
                this.updateWeekDisplay();
            });
        }

        this.updateWeekDisplay();
    }

    updateWeekDisplay() {
        const display = document.getElementById('weekDisplay');
        if (!display) return;

        const endWeek = new Date(this.currentWeek);
        endWeek.setDate(endWeek.getDate() + 6);

        display.textContent = `${window.formatDate(this.currentWeek)} - ${window.formatDate(endWeek)}`;
    }

    async addLecture(day, startTime, endTime) {
        window.showAlert('Add lecture feature coming soon', 'info');
    }

    async editLecture(id) {
        window.showAlert('Edit lecture feature coming soon', 'info');
    }

    async deleteLecture(id) {
        if (!confirm('Are you sure you want to delete this lecture?')) return;

        try {
            await window.apiRequest(`/api/timetable/${id}`, { method: 'DELETE' });
            window.showAlert('Lecture deleted successfully', 'success');
            this.loadTimetable();
        } catch (error) {
            window.showAlert('Error deleting lecture', 'danger');
        }
    }
}

// Initialize on page load
let timetableManager;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        timetableManager = new TimetableManager();
        timetableManager.init();
    });
} else {
    timetableManager = new TimetableManager();
    timetableManager.init();
}
