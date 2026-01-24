/**
 * Form Validation Module
 */

export function initFormValidation() {
    // Bootstrap validation style
    const forms = document.querySelectorAll(".needs-validation");
    Array.from(forms).forEach(form => {
        form.addEventListener("submit", event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add("was-validated");
        }, false);
    });

    // Custom Signup/Login Validation
    const signupForm = document.getElementById("signup-form");
    if (signupForm) {
        const emailInput = signupForm.querySelector("input[name='email']");
        const passwordInput = signupForm.querySelector("input[name='password']");

        // Email Regex: Basic format name@domain.tld
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        // Password Regex: 1 Upper, 1 Number, 8+ Chars, 1 Special Char
        const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

        if (emailInput) {
            emailInput.addEventListener("input", function () {
                if (emailRegex.test(this.value)) {
                    this.setCustomValidity("");
                    this.classList.remove("is-invalid");
                    this.classList.add("is-valid");
                } else {
                    this.setCustomValidity("Invalid email format");
                    this.classList.remove("is-valid");
                    this.classList.add("is-invalid");
                }
            });
        }

        if (passwordInput) {
            passwordInput.addEventListener("input", function () {
                // We can separate checks for detailed feedback if needed
                if (passwordRegex.test(this.value)) {
                    this.setCustomValidity("");
                    this.classList.remove("is-invalid");
                    this.classList.add("is-valid");
                } else {
                    this.setCustomValidity("Password requirements not met");
                    this.classList.remove("is-valid");
                    this.classList.add("is-invalid");
                }
            });
        }

        signupForm.addEventListener("submit", (e) => {
            let valid = true;
            if (!emailRegex.test(emailInput.value)) {
                emailInput.classList.add("is-invalid");
                valid = false;
            }
            if (!passwordRegex.test(passwordInput.value)) {
                passwordInput.classList.add("is-invalid");
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    }
}
