/**
 * Login Page JavaScript
 * Handles login form submission and session management
 */

document.addEventListener('DOMContentLoaded', function () {
    // Get form elements
    const loginForm = document.getElementById('loginForm');

    if (!loginForm) {
        return;
    }

    // Handle form submission
    loginForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const rememberMe = document.getElementById('remember').checked;

        // Validation
        if (!email || !password) {
            alert('Please fill in all fields');
            return;
        }

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    email: email,
                    password: password,
                    remember: rememberMe ? 'on' : 'off'
                })
            });

            const contentType = response.headers.get('content-type');

            if (contentType && contentType.includes('application/json')) {
                // JSON response from AJAX endpoint
                const data = await response.json();
                if (data.success) {
                    // Store session in browser storage
                    SessionManager.setSession({
                        user_id: data.user.user_id,
                        email: data.user.email,
                        name: data.user.name,
                        role: data.user.role
                    });

                    // Long-lived session if remember me is checked
                    if (rememberMe) {
                        localStorage.setItem('remember_me', 'true');
                    }

                    // Show success message
                    console.log('✓ Login successful');

                    // Use redirect URL from server response
                    const redirectUrl = data.redirect || '/';
                    setTimeout(() => {
                        window.location.href = redirectUrl;
                    }, 500);
                } else {
                    // Show error message
                    alert('❌ ' + (data.message || 'Login failed'));
                }
            } else {
                // HTML response (fallback)
                const text = await response.text();
                document.body.innerHTML = text;
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });

});
