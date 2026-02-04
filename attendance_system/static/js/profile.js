// Profile Management JavaScript

document.addEventListener('DOMContentLoaded', function () {
    initializeProfile();
});

function initializeProfile() {
    // Edit Profile Modal
    const editProfileBtn = document.getElementById('editProfileBtn');
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', openEditModal);
    }

    // Change Password Modal
    const changePasswordBtn = document.getElementById('changePasswordBtn');
    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', openPasswordModal);
    }

    // Avatar Upload
    const avatarInput = document.getElementById('avatarInput');
    if (avatarInput) {
        avatarInput.addEventListener('change', handleAvatarUpload);
    }

    // Form Submissions
    const editProfileForm = document.getElementById('editProfileForm');
    if (editProfileForm) {
        editProfileForm.addEventListener('submit', handleProfileUpdate);
    }

    const changePasswordForm = document.getElementById('changePasswordForm');
    if (changePasswordForm) {
        changePasswordForm.addEventListener('submit', handlePasswordChange);
    }
}

function openEditModal() {
    const modal = new bootstrap.Modal(document.getElementById('editProfileModal'));
    modal.show();
}

function openPasswordModal() {
    const modal = new bootstrap.Modal(document.getElementById('changePasswordModal'));
    modal.show();
}

function handleAvatarUpload(event) {
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

        // Auto-upload avatar
        uploadAvatar(file);
    }
}

function uploadAvatar(file) {
    const formData = new FormData();
    formData.append('avatar', file);

    showLoading(true);

    fetch('/profile/upload-avatar', {
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

function handleProfileUpdate(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    // Validate form data
    if (!validateProfileData(data)) {
        return;
    }

    showLoading(true);

    fetch('/profile/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            showLoading(false);
            if (data.success) {
                showAlert('Profile updated successfully!', 'success');
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('editProfileModal'));
                modal.hide();
                // Reload page to show updated data
                setTimeout(() => location.reload(), 1500);
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

function handlePasswordChange(event) {
    event.preventDefault();

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

    fetch('/profile/change-password', {
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
