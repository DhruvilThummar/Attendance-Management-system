// Profile Management JavaScript

document.addEventListener('DOMContentLoaded', function () {
    initializeProfile();
});

function initializeProfile() {
    const endpoints = getProfileEndpoints();

    // Edit Profile Modal
    const editProfileBtn = document.getElementById('editProfileBtn');
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', openEditProfileModal);
    }

    const editProfileForm = document.getElementById('editProfileForm');
    if (editProfileForm) {
        editProfileForm.addEventListener('submit', function (event) {
            handleProfileUpdate(event, endpoints.profile);
        });
    }

    // Change Password Modal
    const changePasswordBtn = document.getElementById('changePasswordBtn');
    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', openPasswordModal);
    }

    // Avatar Upload (view only, no actual upload for superadmin)
    const avatarInput = document.getElementById('avatarInput');
    if (avatarInput) {
        avatarInput.addEventListener('change', function (event) {
            handleAvatarUpload(event, endpoints.avatar);
        });
    }

    // Form Submissions
    const changePasswordForm = document.getElementById('changePasswordForm');
    if (changePasswordForm) {
        changePasswordForm.addEventListener('submit', function (event) {
            handlePasswordChange(event, endpoints.password);
        });
    }
}

function getProfileEndpoints() {
    const container = document.querySelector('.profile-container');
    return {
        profile: container?.dataset?.profileEndpoint || '',
        password: container?.dataset?.passwordEndpoint || '',
        avatar: container?.dataset?.avatarEndpoint || ''
    };
}

function openEditProfileModal() {
    const modal = new bootstrap.Modal(document.getElementById('editProfileModal'));
    modal.show();
}

function openPasswordModal() {
    const modal = new bootstrap.Modal(document.getElementById('changePasswordModal'));
    modal.show();
}

function handleAvatarUpload(event, avatarEndpoint) {
    const file = event.target.files[0];
    if (file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            showAlert('Please select a valid image file', 'danger');
            return;
        }

        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            showAlert('Image size should be less than 5MB', 'danger');
            return;
        }

        // Preview image
        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.getElementById('avatarPreview');
            if (preview) {
                preview.src = e.target.result;
            }
            const profileAvatar = document.querySelector('.profile-avatar');
            if (profileAvatar) {
                profileAvatar.src = e.target.result;
            }
        };
        reader.readAsDataURL(file);

        if (!avatarEndpoint) {
            showAlert('Avatar upload is not available', 'warning');
            return;
        }

        // Auto-upload avatar
        uploadAvatar(file, avatarEndpoint);
    }
}

function uploadAvatar(file, endpoint) {
    const formData = new FormData();
    formData.append('avatar', file);

    showLoading(true);

    fetch(endpoint, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            showLoading(false);
            if (data.success) {
                showAlert('Profile picture updated successfully!', 'success');
            } else {
                showAlert(data.message || 'Failed to upload avatar', 'danger');
            }
        })
        .catch(error => {
            showLoading(false);
            console.error('Error:', error);
            showAlert('An error occurred while uploading avatar', 'danger');
        });
}

function handlePasswordChange(event, endpoint) {
    event.preventDefault();

    if (!endpoint) {
        showAlert('Password change is not available for this profile', 'warning');
        return;
    }

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    // Validate passwords
    if (data.new_password !== data.confirm_password) {
        showAlert('New passwords do not match', 'danger');
        return;
    }

    if (data.new_password.length < 8) {
        showAlert('Password must be at least 8 characters long', 'danger');
        return;
    }

    showLoading(true);

    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            current_password: data.current_password,
            new_password: data.new_password
        })
    })
        .then(response => response.json())
        .then(data => {
            showLoading(false);
            if (data.success) {
                showAlert('Password changed successfully!', 'success');
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
                modal.hide();
                // Reset form
                event.target.reset();
            } else {
                showAlert(data.message || 'Failed to change password', 'danger');
            }
        })
        .catch(error => {
            showLoading(false);
            console.error('Error:', error);
            showAlert('An error occurred while changing password', 'danger');
        });
}

function handleProfileUpdate(event, endpoint) {
    event.preventDefault();

    if (!endpoint) {
        showAlert('Profile update is not available for this profile', 'warning');
        return;
    }

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    if (!validateProfileData(data)) {
        return;
    }

    showLoading(true);

    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: data.name,
            email: data.email,
            mobile: data.mobile
        })
    })
        .then(response => response.json())
        .then(data => {
            showLoading(false);
            if (data.success) {
                showAlert('Profile updated successfully!', 'success');
                const modal = bootstrap.Modal.getInstance(document.getElementById('editProfileModal'));
                if (modal) {
                    modal.hide();
                }
                setTimeout(() => {
                    location.reload();
                }, 1200);
            } else {
                showAlert(data.message || 'Failed to update profile', 'danger');
            }
        })
        .catch(error => {
            showLoading(false);
            console.error('Error:', error);
            showAlert('An error occurred while updating profile', 'danger');
        });
}

function validateProfileData(data) {
    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
        showAlert('Please enter a valid email address', 'danger');
        return false;
    }

    // Validate mobile
    const mobileRegex = /^[0-9]{10}$/;
    if (data.mobile && !mobileRegex.test(data.mobile)) {
        showAlert('Please enter a valid 10-digit mobile number', 'danger');
        return false;
    }

    return true;
}

function showLoading(show) {
    const spinner = document.querySelector('.loading-spinner');
    if (spinner) {
        if (show) {
            spinner.classList.add('active');
        } else {
            spinner.classList.remove('active');
        }
    }
}

function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert-custom');
    existingAlerts.forEach(alert => alert.remove());

    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show alert-custom`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    // Insert at top of profile container
    const container = document.querySelector('.profile-container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Password strength indicator
function checkPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;

    return strength;
}

// Add password strength indicator on input
document.addEventListener('DOMContentLoaded', function () {
    const newPasswordInput = document.getElementById('new_password');
    if (newPasswordInput) {
        newPasswordInput.addEventListener('input', function () {
            const strength = checkPasswordStrength(this.value);
            const strengthIndicator = document.getElementById('passwordStrength');

            if (strengthIndicator) {
                let strengthText = '';
                let strengthClass = '';

                if (strength < 2) {
                    strengthText = 'Weak';
                    strengthClass = 'text-danger';
                } else if (strength < 4) {
                    strengthText = 'Medium';
                    strengthClass = 'text-warning';
                } else {
                    strengthText = 'Strong';
                    strengthClass = 'text-success';
                }

                strengthIndicator.textContent = strengthText;
                strengthIndicator.className = strengthClass;
            }
        });
    }
});
