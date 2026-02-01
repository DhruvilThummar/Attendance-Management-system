/**
 * Profile Management Module
 */

class ProfileManager {
    constructor() {
        this.user = null;
    }

    async init() {
        await this.loadProfile();
        this.setupEventListeners();
    }

    async loadProfile() {
        try {
            this.user = window.AppState?.user;
            if (!this.user) {
                const data = await window.apiRequest('/api/auth/me');
                this.user = data.user;
            }
            this.renderProfile();
        } catch (error) {
            window.showAlert('Error loading profile', 'danger');
        }
    }

    renderProfile() {
        const container = document.getElementById('profileContainer');
        if (!container || !this.user) return;

        container.innerHTML = `
            <div class="row">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body text-center">
                            <div class="profile-avatar-large mx-auto mb-3">
                                ${this.user.name.charAt(0).toUpperCase()}
                            </div>
                            <h4>${this.user.name}</h4>
                            <p class="text-muted">${this.user.role_name}</p>
                            <p class="small text-muted">${this.user.email}</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">Profile Information</h5>
                        </div>
                        <div class="card-body">
                            <form id="profileForm">
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Full Name</label>
                                        <input type="text" class="form-control" id="name" value="${this.user.name}">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Email</label>
                                        <input type="email" class="form-control" id="email" value="${this.user.email}" readonly>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Phone</label>
                                        <input type="text" class="form-control" id="phone" value="${this.user.phone || ''}">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">College</label>
                                        <input type="text" class="form-control" value="${this.user.college_name || ''}" readonly>
                                    </div>
                                </div>
                                <button type="submit" class="btn btn-primary">Update Profile</button>
                            </form>
                        </div>
                    </div>

                    <div class="card mt-3">
                        <div class="card-header">
                            <h5 class="mb-0">Change Password</h5>
                        </div>
                        <div class="card-body">
                            <form id="passwordForm">
                                <div class="mb-3">
                                    <label class="form-label">Current Password</label>
                                    <input type="password" class="form-control" id="currentPassword" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">New Password</label>
                                    <input type="password" class="form-control" id="newPassword" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Confirm New Password</label>
                                    <input type="password" class="form-control" id="confirmPassword" required>
                                </div>
                                <button type="submit" class="btn btn-warning">Change Password</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    setupEventListeners() {
        document.addEventListener('submit', async (e) => {
            if (e.target.id === 'profileForm') {
                e.preventDefault();
                await this.updateProfile();
            } else if (e.target.id === 'passwordForm') {
                e.preventDefault();
                await this.changePassword();
            }
        });
    }

    async updateProfile() {
        try {
            const data = {
                name: document.getElementById('name').value,
                phone: document.getElementById('phone').value
            };

            await window.apiRequest('/api/profile', {
                method: 'PUT',
                body: JSON.stringify(data)
            });

            window.showAlert('Profile updated successfully', 'success');
            await this.loadProfile();
        } catch (error) {
            window.showAlert('Error updating profile', 'danger');
        }
    }

    async changePassword() {
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (newPassword !== confirmPassword) {
            window.showAlert('Passwords do not match', 'danger');
            return;
        }

        try {
            const data = {
                current_password: document.getElementById('currentPassword').value,
                new_password: newPassword
            };

            await window.apiRequest('/api/profile/password', {
                method: 'POST',
                body: JSON.stringify(data)
            });

            window.showAlert('Password changed successfully', 'success');
            document.getElementById('passwordForm').reset();
        } catch (error) {
            window.showAlert('Error changing password', 'danger');
        }
    }
}

// Initialize
let profileManager;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        profileManager = new ProfileManager();
        profileManager.init();
    });
} else {
    profileManager = new ProfileManager();
    profileManager.init();
}
