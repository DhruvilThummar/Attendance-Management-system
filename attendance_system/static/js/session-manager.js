/**
 * Browser Session Management
 * Uses localStorage to persist user login data across browser sessions
 */

const SessionManager = {
    /**
     * Key for storing session data in localStorage
     */
    STORAGE_KEY: 'attendance_user_session',

    /**
     * Store user session data in browser localStorage
     * @param {Object} userData - User data to store
     * @param {number} userData.user_id - User ID
     * @param {string} userData.email - User email
     * @param {string} userData.name - User name
     * @param {string} userData.role - User role
     */
    setSession(userData) {
        try {
            const sessionData = {
                user_id: userData.user_id,
                email: userData.email,
                name: userData.name,
                role: userData.role,
                created_at: new Date().toISOString(),
                expires_at: new Date(Date.now() + 30 * 60 * 1000).toISOString() // 30 minutes from now
            };

            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(sessionData));
            console.log('✓ Session stored in localStorage:', sessionData);
            return true;
        } catch (error) {
            console.error('✗ Error storing session:', error);
            return false;
        }
    },

    /**
     * Get user session data from browser localStorage
     * @returns {Object|null} User session data or null if not found/expired
     */
    getSession() {
        try {
            const sessionData = localStorage.getItem(this.STORAGE_KEY);

            if (!sessionData) {
                return null;
            }

            const session = JSON.parse(sessionData);

            // Check if session has expired
            if (new Date(session.expires_at) < new Date()) {
                console.log('Session expired');
                this.clearSession();
                return null;
            }

            return session;
        } catch (error) {
            console.error('✗ Error retrieving session:', error);
            return null;
        }
    },

    /**
     * Check if user is logged in
     * @returns {boolean} True if user has valid session
     */
    isLoggedIn() {
        return this.getSession() !== null;
    },

    /**
     * Get current user ID
     * @returns {number|null} User ID or null if not logged in
     */
    getUserId() {
        const session = this.getSession();
        return session ? session.user_id : null;
    },

    /**
     * Get current user role
     * @returns {string|null} User role or null if not logged in
     */
    getUserRole() {
        const session = this.getSession();
        return session ? session.role : null;
    },

    /**
     * Get current user email
     * @returns {string|null} User email or null if not logged in
     */
    getUserEmail() {
        const session = this.getSession();
        return session ? session.email : null;
    },

    /**
     * Get current user name
     * @returns {string|null} User name or null if not logged in
     */
    getUserName() {
        const session = this.getSession();
        return session ? session.name : null;
    },

    /**
     * Clear user session from browser localStorage
     */
    clearSession() {
        try {
            localStorage.removeItem(this.STORAGE_KEY);
            console.log('✓ Session cleared from localStorage');
            return true;
        } catch (error) {
            console.error('✗ Error clearing session:', error);
            return false;
        }
    },

    /**
     * Refresh session expiration time
     * Extends session by 30 minutes
     */
    refreshSession() {
        const session = this.getSession();
        if (session) {
            session.expires_at = new Date(Date.now() + 30 * 60 * 1000).toISOString();
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(session));
            return true;
        }
        return false;
    },

    /**
     * Display user info in the DOM
     * Updates all elements with class 'user-name', 'user-email', etc.
     */
    displayUserInfo() {
        const session = this.getSession();

        if (!session) {
            return;
        }

        // Update user name
        const nameElements = document.querySelectorAll('[data-user-name]');
        nameElements.forEach(el => {
            el.textContent = session.name;
        });

        // Update user email
        const emailElements = document.querySelectorAll('[data-user-email]');
        emailElements.forEach(el => {
            el.textContent = session.email;
        });

        // Update user role
        const roleElements = document.querySelectorAll('[data-user-role]');
        roleElements.forEach(el => {
            el.textContent = session.role.toUpperCase();
        });

        // Show user info container
        const userInfoContainer = document.getElementById('user-info');
        if (userInfoContainer) {
            userInfoContainer.style.display = 'block';
        }
    },

    /**
     * Protect page - redirect to login if not logged in
     * Call this on pages that require authentication
     */
    protectPage(requiredRole = null) {
        const session = this.getSession();

        if (!session) {
            console.log('Not logged in, redirecting to login page');
            window.location.href = '/login';
            return false;
        }

        if (requiredRole && session.role !== requiredRole) {
            console.log(`Access denied. Required role: ${requiredRole}, Your role: ${session.role}`);
            window.location.href = '/';
            return false;
        }

        return true;
    },

    /**
     * Log out user - clears both server and client sessions
     */
    async logout() {
        try {
            // Clear client-side session first
            this.clearSession();

            // Call server logout endpoint
            const response = await fetch('/logout', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const data = await response.json();
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    window.location.href = '/';
                }
            } else {
                window.location.href = '/';
            }
        } catch (error) {
            console.error('Error during logout:', error);
            // Still redirect even if fetch fails
            window.location.href = '/';
        }
    }
};

/**
 * Auto-refresh session on page activity
 * Extends session if user is active
 */
function initSessionAutoRefresh() {
    const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
    let refreshTimeout;

    const refreshSessionOnActivity = () => {
        clearTimeout(refreshTimeout);

        // Refresh session after 1 minute of detecting activity
        refreshTimeout = setTimeout(() => {
            if (SessionManager.isLoggedIn()) {
                SessionManager.refreshSession();
                console.log('✓ Session refreshed due to user activity');
            }
        }, 60000);
    };

    // Add event listeners
    events.forEach(event => {
        document.addEventListener(event, refreshSessionOnActivity, true);
    });

    console.log('✓ Session auto-refresh initialized');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Display user info if logged in
    if (SessionManager.isLoggedIn()) {
        SessionManager.displayUserInfo();
        initSessionAutoRefresh();
    }
});
