/**
 * Enhanced Navbar with Role-Based Navigation
 * Auto-included in all authenticated pages
 */

// Navbar State
const NavbarState = {
    notifications: [],
    unreadCount: 0
};

/**
 * Initialize Navbar
 */
function initNavbar() {
    if (!window.AppState?.user) {
        checkAuthAndInitNavbar();
    } else {
        updateNavbarForUser();
        loadNotifications();
    }
}

/**
 * Check authentication and update navbar
 */
async function checkAuthAndInitNavbar() {
    try {
        const response = await fetch('/api/auth/me');
        if (response.ok) {
            const data = await response.json();
            if (window.AppState) {
                window.AppState.user = data.user;
                window.AppState.isAuthenticated = true;
            }
            updateNavbarForUser();
            loadNotifications();
        }
    } catch (error) {
        console.log('User not authenticated');
    }
}

/**
 * Update navbar based on user role
 */
function updateNavbarForUser() {
    const user = window.AppState?.user;
    if (!user) return;

    // Update user info
    const userName = document.getElementById('navUserName');
    const userFullName = document.getElementById('navUserFullName');
    const userRole = document.getElementById('navUserRole');

    if (userName) userName.textContent = user.name.split(' ')[0];
    if (userFullName) userFullName.textContent = user.name;
    if (userRole) userRole.textContent = user.role_name;

    // Build navigation menu based on role
    const leftMenu = document.getElementById('navLeftMenu');
    if (!leftMenu) return;

    const menuItems = getMenuItemsForRole(user.role_name);
    leftMenu.innerHTML = menuItems.map(item => `
        <li class="nav-item">
            <a class="nav-link" href="${item.href}">
                <i class="bi bi-${item.icon} me-1"></i>
                ${item.label}
            </a>
        </li>
    `).join('');

    // Highlight active page
    highlightActivePage();
}

/**
 * Get menu items based on user role
 */
function getMenuItemsForRole(role) {
    const menus = {
        ADMIN: [
            { label: 'Dashboard', href: '/dashboard', icon: 'speedometer2' },
            { label: 'Students', href: '/students', icon: 'people' },
            { label: 'Faculty', href: '/faculty', icon: 'person-workspace' },
            { label: 'Departments', href: '/departments', icon: 'building' },
            { label: 'Timetable', href: '/timetable', icon: 'calendar3' },
            { label: 'Reports', href: '/reports', icon: 'graph-up' },
            { label: 'Settings', href: '/settings', icon: 'gear' }
        ],
        HOD: [
            { label: 'Dashboard', href: '/dashboard', icon: 'speedometer2' },
            { label: 'Students', href: '/students', icon: 'people' },
            { label: 'Faculty', href: '/faculty', icon: 'person-workspace' },
            { label: 'Timetable', href: '/timetable', icon: 'calendar3' },
            { label: 'Reports', href: '/reports', icon: 'graph-up' }
        ],
        FACULTY: [
            { label: 'Dashboard', href: '/dashboard', icon: 'speedometer2' },
            { label: 'Mark Attendance', href: '/mark-attendance', icon: 'clipboard-check' },
            { label: 'Timetable', href: '/timetable', icon: 'calendar3' },
            { label: 'Reports', href: '/reports', icon: 'graph-up' }
        ],
        STUDENT: [
            { label: 'Dashboard', href: '/dashboard', icon: 'speedometer2' },
            { label: 'My Attendance', href: '/student-attendance', icon: 'clipboard-data' },
            { label: 'Timetable', href: '/timetable', icon: 'calendar3' }
        ],
        PARENT: [
            { label: 'Dashboard', href: '/dashboard', icon: 'speedometer2' }
        ]
    };

    return menus[role] || [];
}

/**
 * Highlight active page in navigation
 */
function highlightActivePage() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('#navLeftMenu .nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Load notifications
 */
async function loadNotifications() {
    try {
        const response = await fetch('/api/notifications/recent');
        const data = await response.json();
        
        NavbarState.notifications = data.notifications || [];
        NavbarState.unreadCount = data.unread || 0;
        
        updateNotificationBadge();
        renderNotifications();
    } catch (error) {
        console.error('Error loading notifications:', error);
    }
}

/**
 * Update notification badge
 */
function updateNotificationBadge() {
    const badge = document.querySelector('.notification-badge');
    if (!badge) return;

    if (NavbarState.unreadCount > 0) {
        badge.textContent = NavbarState.unreadCount > 9 ? '9+' : NavbarState.unreadCount;
        badge.style.display = 'inline-block';
    } else {
        badge.style.display = 'none';
    }
}

/**
 * Render notifications dropdown
 */
function renderNotifications() {
    const dropdown = document.querySelector('.notification-dropdown');
    if (!dropdown) return;

    if (NavbarState.notifications.length === 0) {
        dropdown.innerHTML = `
            <h6 class="dropdown-header">Notifications</h6>
            <div class="dropdown-divider"></div>
            <div class="text-center py-3 text-muted">
                <i class="bi bi-bell-slash"></i>
                <p class="mb-0 small">No notifications</p>
            </div>
        `;
        return;
    }

    dropdown.innerHTML = `
        <h6 class="dropdown-header">Notifications</h6>
        <div class="dropdown-divider"></div>
        ${NavbarState.notifications.map(n => `
            <a class="dropdown-item notification-item ${n.is_read ? '' : 'unread'}" href="#" onclick="markNotificationRead(${n.id}); return false;">
                <div class="d-flex">
                    <div class="flex-shrink-0">
                        <i class="bi bi-${getNotificationIcon(n.type)} text-${getNotificationColor(n.type)}"></i>
                    </div>
                    <div class="flex-grow-1 ms-3">
                        <p class="mb-0 small">${n.message}</p>
                        <small class="text-muted">${window.formatDate(n.created_at)}</small>
                    </div>
                </div>
            </a>
        `).join('')}
        <div class="dropdown-divider"></div>
        <a class="dropdown-item text-center small text-muted" href="/notifications">View all notifications</a>
    `;
}

/**
 * Get notification icon based on type
 */
function getNotificationIcon(type) {
    const icons = {
        attendance: 'clipboard-check',
        warning: 'exclamation-circle-fill',
        info: 'info-circle-fill',
        success: 'check-circle-fill',
        alert: 'bell-fill'
    };
    return icons[type] || 'bell';
}

/**
 * Get notification color based on type
 */
function getNotificationColor(type) {
    const colors = {
        attendance: 'primary',
        warning: 'warning',
        info: 'info',
        success: 'success',
        alert: 'danger'
    };
    return colors[type] || 'primary';
}

/**
 * Mark notification as read
 */
async function markNotificationRead(notificationId) {
    try {
        await fetch(`/api/notifications/${notificationId}/read`, { method: 'POST' });
        await loadNotifications();
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
}

/**
 * Search functionality
 */
function setupNavbarSearch() {
    const searchInput = document.querySelector('#navbarContent input[type="search"]');
    if (!searchInput) return;

    searchInput.addEventListener('input', window.debounce(async (e) => {
        const query = e.target.value.trim();
        if (query.length < 2) return;

        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();
            displaySearchResults(results);
        } catch (error) {
            console.error('Search error:', error);
        }
    }, 300));
}

/**
 * Display search results
 */
function displaySearchResults(results) {
    // Implementation for search results dropdown
    console.log('Search results:', results);
}

// Initialize navbar on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initNavbar();
        setupNavbarSearch();
    });
} else {
    initNavbar();
    setupNavbarSearch();
}

// Export for external use
if (typeof window !== 'undefined') {
    window.initNavbar = initNavbar;
    window.updateNavbarForUser = updateNavbarForUser;
    window.loadNotifications = loadNotifications;
}
