/**
 * Main Application JavaScript
 * Handles routing, authentication, and navigation
 */

// API Base URL
const API_BASE = '/api';

// Global state
const AppState = {
    user: null,
    isAuthenticated: false,
    currentPage: null
};

/**
 * Initialize the application
 */
function initApp() {
    checkAuth();
    setupNavigation();
    loadCurrentPage();
}

/**
 * Check if user is authenticated
 */
async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE}/auth/me`, {
            credentials: 'include'
        });

        if (response.ok) {
            const data = await response.json();
            AppState.user = data.user || data;
            AppState.isAuthenticated = true;
            updateNavigation();
        } else {
            AppState.isAuthenticated = false;
            // Redirect to login if not on public pages
            const publicPages = ['/login', '/register', '/', '/about', '/contact'];
            if (!publicPages.includes(window.location.pathname)) {
                window.location.href = '/login';
            }
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        AppState.isAuthenticated = false;
    }
}

/**
 * Update navigation based on user role
 */
function updateNavigation() {
    const navMenu = document.getElementById('nav-menu');
    if (!navMenu) return;

    const user = AppState.user;
    if (!user) {
        navMenu.innerHTML = `
            <li class="nav-item">
                <a class="nav-link" href="/">Home</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/about">About</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/contact">Contact</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/login">Login</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="/register">Register</a>
            </li>
        `;
        return;
    }

    let menuItems = [];

    // Common items
    menuItems.push({
        label: 'Dashboard',
        href: '/dashboard',
        icon: 'bi-speedometer2'
    });

    // Role-based items
    switch (user.role_name) {
        case 'ADMIN':
        case 'HOD':
            menuItems.push(
                { label: 'Students', href: '/students', icon: 'bi-people' },
                { label: 'Faculty', href: '/faculty', icon: 'bi-person-workspace' },
                { label: 'Departments', href: '/departments', icon: 'bi-building' },
                { label: 'Divisions', href: '/divisions', icon: 'bi-diagram-3' },
                { label: 'Subjects', href: '/subjects', icon: 'bi-book' },
                { label: 'Timetable', href: '/timetable', icon: 'bi-calendar3' },
                { label: 'Reports', href: '/reports', icon: 'bi-graph-up' },
                { label: 'Settings', href: '/settings', icon: 'bi-gear' }
            );
            break;

        case 'FACULTY':
            menuItems.push(
                { label: 'Timetable', href: '/timetable', icon: 'bi-calendar3' },
                { label: 'Mark Attendance', href: '/mark-attendance', icon: 'bi-clipboard-check' },
                { label: 'Students', href: '/students', icon: 'bi-people' },
                { label: 'Reports', href: '/reports', icon: 'bi-graph-up' }
            );
            break;

        case 'STUDENT':
            menuItems.push(
                { label: 'My Attendance', href: '/student-attendance', icon: 'bi-clipboard-data' },
                { label: 'Timetable', href: '/timetable', icon: 'bi-calendar3' }
            );
            break;

        case 'PARENT':
            menuItems.push(
                { label: 'Student Attendance', href: '/student-attendance', icon: 'bi-clipboard-data' }
            );
            break;
    }

    // User menu
    menuItems.push(
        { label: 'Profile', href: '/profile', icon: 'bi-person-circle' },
        { label: 'Logout', href: '#', icon: 'bi-box-arrow-right', onClick: logout }
    );

    // Build menu HTML
    navMenu.innerHTML = menuItems.map(item => `
        <li class="nav-item">
            <a class="nav-link" href="${item.href}" ${item.onClick ? `onclick="${item.onClick.name}(); return false;"` : ''}>
                <i class="bi ${item.icon}"></i> ${item.label}
            </a>
        </li>
    `).join('');
}

/**
 * Setup navigation event listeners
 */
function setupNavigation() {
    // Handle browser back/forward
    window.addEventListener('popstate', loadCurrentPage);

    // Handle all anchor clicks for SPA routing
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (!link) return;

        const shouldSpaNavigate = link.dataset && link.dataset.spa === 'true';
        if (shouldSpaNavigate && link.href && link.host === window.location.host && !link.target) {
            e.preventDefault();
            navigateTo(link.pathname);
        }
    });
}

/**
 * Navigate to a page
 */
function navigateTo(path) {
    window.history.pushState({}, '', path);
    loadCurrentPage();
}

/**
 * Load the current page based on URL
 */
function loadCurrentPage() {
    const path = window.location.pathname;
    AppState.currentPage = path;

    // Update active nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        const linkPath = new URL(link.href, window.location.origin).pathname;
        link.classList.toggle('active', linkPath === path);
    });
}

/**
 * Logout user
 */
async function logout() {
    try {
        await fetch(`${API_BASE}/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        });
    } catch (error) {
        console.error('Logout error:', error);
    }

    AppState.user = null;
    AppState.isAuthenticated = false;
    window.location.href = '/login';
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const container = document.getElementById('alert-container');
    if (!container) return;

    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    container.appendChild(alert);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

/**
 * Show loading overlay
 */
function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.remove('d-none');
    }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('d-none');
    }
}

/**
 * Make API request
 */
async function apiRequest(endpoint, options = {}) {
    const defaultOptions = {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        }
    };

    const config = { ...defaultOptions, ...options };

    try {
        showLoading();
        const url = endpoint.startsWith('/api') ? endpoint : `${API_BASE}${endpoint}`;
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Request failed');
        }

        return data;
    } catch (error) {
        console.error('API request failed:', error);
        showAlert(error.message, 'danger');
        throw error;
    } finally {
        hideLoading();
    }
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Format time
 */
function formatTime(timeString) {
    if (!timeString) return '';
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}

/**
 * Get attendance percentage class
 */
function getAttendanceClass(percentage) {
    if (percentage >= 85) return 'text-success';
    if (percentage >= 75) return 'text-warning';
    return 'text-danger';
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}

// Export for use in other modules
window.AppState = AppState;
window.showAlert = showAlert;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.apiRequest = apiRequest;
window.formatDate = formatDate;
window.formatTime = formatTime;
window.getAttendanceClass = getAttendanceClass;
window.debounce = debounce;
window.logout = logout;

