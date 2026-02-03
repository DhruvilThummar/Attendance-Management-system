// College autocomplete data
const colleges = [
    { id: 1, name: "Engineering College Mumbai" },
    { id: 2, name: "Delhi Institute of Technology" },
    { id: 3, name: "IIT Bombay" },
    { id: 4, name: "NIT Trichy" },
    { id: 5, name: "Pune University College" },
    { id: 6, name: "Bangalore Institute of Science" },
    { id: 7, name: "Chennai Engineering College" },
    { id: 8, name: "Hyderabad Tech Institute" },
];

// Initialize login page features
document.addEventListener("DOMContentLoaded", () => {
    initCollegeSearch();
    initFormValidation();
});

// College search autocomplete
function initCollegeSearch() {
    const collegeInput = document.getElementById("college");
    const collegeSuggestions = document.getElementById("collegeSuggestions");

    if (!collegeInput) return;

    collegeInput.addEventListener("input", () => {
        const value = collegeInput.value.toLowerCase().trim();

        if (value.length === 0) {
            collegeSuggestions.innerHTML = "";
            collegeSuggestions.style.display = "none";
            return;
        }

        const filtered = colleges.filter((college) =>
            college.name.toLowerCase().includes(value)
        );

        if (filtered.length === 0) {
            collegeSuggestions.innerHTML = '<div class="suggestion-item text-muted">No colleges found</div>';
            collegeSuggestions.style.display = "block";
            return;
        }

        collegeSuggestions.innerHTML = filtered
            .map(
                (college) =>
                    `<div class="suggestion-item" onclick="selectCollege('${college.name}', '${college.id}')" style="cursor: pointer; padding: 8px 12px; hover: background-color: rgba(37, 99, 235, 0.1);">
                        <i class="bi bi-building"></i> ${college.name}
                    </div>`
            )
            .join("");

        collegeSuggestions.style.display = "block";
    });

    // Hide suggestions when clicking outside
    document.addEventListener("click", (e) => {
        if (e.target !== collegeInput) {
            collegeSuggestions.style.display = "none";
        }
    });
}

// Assign selected college to input + hidden id
function selectCollege(name, id) {
    const collegeInput = document.getElementById("college");
    const collegeIdInput = document.getElementById("collegeId");
    collegeInput.value = name;
    if (collegeIdInput) collegeIdInput.value = id;
    document.getElementById("collegeSuggestions").style.display = "none";
}

// Form validation
function initFormValidation() {
    const form = document.querySelector("form");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const collegeInput = document.getElementById("college");

    if (!form) return;

    // Email validation on input
    if (emailInput) {
        emailInput.addEventListener("blur", validateEmail);
        emailInput.addEventListener("input", validateEmail);
    }

    // Password validation on input
    if (passwordInput) {
        passwordInput.addEventListener("input", validatePassword);
    }

    // College validation
    if (collegeInput) {
        collegeInput.addEventListener("blur", validateCollege);
    }

    // Form submission
    form.addEventListener("submit", (e) => {
        if (!validateForm()) {
            e.preventDefault();
        }
    });
}

// Validate email format
function validateEmail() {
    const emailInput = document.getElementById("email");
    const emailError = document.getElementById("emailError");
    const email = emailInput.value.trim();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (email === "") {
        showError(emailInput, emailError, "Email is required");
        return false;
    }

    if (!emailRegex.test(email)) {
        showError(emailInput, emailError, "Please enter a valid email address");
        return false;
    }

    clearError(emailInput, emailError);
    return true;
}

// Validate password strength
function validatePassword() {
    const passwordInput = document.getElementById("password");
    const passwordError = document.getElementById("passwordError");
    const password = passwordInput.value;

    if (password === "") {
        showError(passwordInput, passwordError, "Password is required");
        return false;
    }

    if (password.length < 8) {
        showError(passwordInput, passwordError, "Password must be at least 8 characters long");
        return false;
    }

    const hasUpperCase = /[A-Z]/.test(password);
    if (!hasUpperCase) {
        showError(passwordInput, passwordError, "Password must contain at least one uppercase letter (A-Z)");
        return false;
    }

    const hasNumber = /[0-9]/.test(password);
    if (!hasNumber) {
        showError(passwordInput, passwordError, "Password must contain at least one number (0-9)");
        return false;
    }

    const hasSpecialChar = /[!@#$%^&*()_\-+=\[\]{};:'",.<>?/\\|`~]/.test(password);
    if (!hasSpecialChar) {
        showError(passwordInput, passwordError, "Password must contain at least one special character (!@#$%^&*()_)");
        return false;
    }

    clearError(passwordInput, passwordError);
    return true;
}

// Validate college selection
function validateCollege() {
    const collegeInput = document.getElementById("college");
    const collegeError = document.getElementById("collegeError");
    const college = collegeInput.value.trim();

    if (college === "") {
        showError(collegeInput, collegeError, "Please select a college");
        return false;
    }

    const isValidCollege = colleges.some(
        (c) => c.name.toLowerCase() === college.toLowerCase()
    );

    if (!isValidCollege) {
        showError(collegeInput, collegeError, "Please select a valid college from the suggestions");
        return false;
    }

    clearError(collegeInput, collegeError);
    return true;
}

// Validate form before submit
function validateForm() {
    const emailValid = validateEmail();
    const passwordValid = validatePassword();
    const collegeValid = validateCollege();

    return emailValid && passwordValid && collegeValid;
}

// Show error message
function showError(input, errorElement, message) {
    input.classList.add("is-invalid");
    if (errorElement) {
        errorElement.innerHTML = `<i class="bi bi-exclamation-circle"></i> ${message}`;
        errorElement.classList.remove("d-none");
        errorElement.classList.add("error-show");
        input.setAttribute("aria-invalid", "true");
    }
}

// Clear error message
function clearError(input, errorElement) {
    input.classList.remove("is-invalid");
    if (errorElement) {
        errorElement.classList.add("d-none");
        errorElement.classList.remove("error-show");
        input.setAttribute("aria-invalid", "false");
    }
}

// Register page role map
const registerRoleTitles = {
    student: "Student",
    faculty: "Faculty",
    hod: "Head of Department (HOD)",
    college_admin: "College Administrator",
    parent: "Parent/Guardian",
};

let registerModalInstance;

// Initialize register modal + role buttons
document.addEventListener("DOMContentLoaded", () => {
    const registerModal = document.getElementById("registrationModal");
    if (!registerModal) return;

    registerModalInstance = new bootstrap.Modal(registerModal);

    document.querySelectorAll(".role-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const role = btn.getAttribute("data-role");
            selectRole(role);

            document.querySelectorAll(".role-btn").forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");
        });
    });

    registerModal.addEventListener("hidden.bs.modal", () => {
        document.querySelectorAll(".role-btn").forEach((b) => b.classList.remove("active"));
        resetRegistrationForm();
    });
});

// Select role and show modal
function selectRole(role) {
    const selectedRole = document.getElementById("selectedRole");
    if (!selectedRole) return;
    selectedRole.value = role;

    const title = document.getElementById("registrationModalLabel");
    if (title) title.textContent = `Register as ${registerRoleTitles[role]}`;

    ["studentFields", "facultyFields", "hodFields", "collegeAdminFields", "parentFields"].forEach((id) => {
        const section = document.getElementById(id);
        if (section) section.style.display = "none";
    });

    const activeSection = {
        student: "studentFields",
        faculty: "facultyFields",
        hod: "hodFields",
        college_admin: "collegeAdminFields",
        parent: "parentFields",
    }[role];

    if (activeSection) {
        const section = document.getElementById(activeSection);
        if (section) section.style.display = "block";
    }

    if (registerModalInstance) registerModalInstance.show();
}

// Reset register form
function resetRegistrationForm() {
    const form = document.getElementById("registrationForm");
    if (form) form.reset();

    const roleInput = document.getElementById("selectedRole");
    if (roleInput) roleInput.value = "";

    document.querySelectorAll(".error-text").forEach((el) => el.classList.add("d-none"));
    document.querySelectorAll(".form-control").forEach((el) => el.classList.remove("is-invalid"));
}

function markRegisterRequiredFields(fieldIds) {
    fieldIds.forEach((id) => {
        const field = document.getElementById(id);
        if (!field || !field.value.trim()) {
            field.classList.add("is-invalid");
        } else {
            field.classList.remove("is-invalid");
        }
    });
}

function registerValidateEmailValue(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function registerValidatePasswordValue(password) {
    const hasMinLength = password.length >= 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[!@#$%^&*()_\-+=\[\]{};:'",.<>?/\\|`~]/.test(password);
    return hasMinLength && hasUpperCase && hasNumber && hasSpecialChar;
}

function registerShowError(inputId, errorId, message) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);
    if (!input || !error) return;
    showError(input, error, message);
}

function registerClearError(inputId, errorId) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);
    if (!input || !error) return;
    clearError(input, error);
}

// Handle register form submission
function submitRegistration(e) {
    e.preventDefault();

    const role = document.getElementById("selectedRole")?.value;
    const password = document.getElementById("password")?.value || "";
    const confirmPassword = document.getElementById("confirmPassword")?.value || "";
    const terms = document.getElementById("terms")?.checked;

    let isValid = true;

    // Validate role-based email
    const emailMap = {
        college_admin: { field: "adminEmail", error: "adminEmailError" },
        hod: { field: "hodEmail", error: "hodEmailError" },
        faculty: { field: "facultyEmail", error: "facultyEmailError" },
        student: { field: "studentEmail", error: "studentEmailError" },
        parent: { field: "parentEmail", error: "parentEmailError" },
    };

    if (role && emailMap[role]) {
        const emailField = emailMap[role].field;
        const emailError = emailMap[role].error;
        const emailValue = document.getElementById(emailField)?.value || "";

        if (!emailValue || !registerValidateEmailValue(emailValue)) {
            registerShowError(emailField, emailError, emailValue ? "Invalid email format" : "Email is required");
            isValid = false;
        } else {
            registerClearError(emailField, emailError);
        }
    }

    // Validate password
    if (!password) {
        registerShowError("password", "passwordError", "Password is required");
        isValid = false;
    } else if (!registerValidatePasswordValue(password)) {
        registerShowError(
            "password",
            "passwordError",
            "Password must have: 8+ chars, 1 uppercase, 1 number, 1 special char"
        );
        isValid = false;
    } else {
        registerClearError("password", "passwordError");
    }

    // Confirm password
    if (!confirmPassword) {
        registerShowError("confirmPassword", "confirmPasswordError", "Please confirm your password");
        isValid = false;
    } else if (password !== confirmPassword) {
        registerShowError("confirmPassword", "confirmPasswordError", "Passwords do not match");
        isValid = false;
    } else {
        registerClearError("confirmPassword", "confirmPasswordError");
    }

    // Validate terms
    if (!terms) {
        alert("Please agree to the Terms & Conditions");
        isValid = false;
    }

    // Role-specific required fields
    if (role === "college_admin") {
        const required = ["adminCollege", "adminEmail"];
        markRegisterRequiredFields(required);
        required.forEach((id) => {
            if (!document.getElementById(id)?.value.trim()) isValid = false;
        });
    } else if (role === "hod") {
        const required = ["hodCollege", "hodDepartment", "hodEmail", "hodName", "hodPhone"];
        markRegisterRequiredFields(required);
        required.forEach((id) => {
            if (!document.getElementById(id)?.value.trim()) isValid = false;
        });
    } else if (role === "faculty") {
        const required = ["facultyCollege", "facultyDepartment", "facultyEmail", "facultyName", "facultyPhone"];
        markRegisterRequiredFields(required);
        required.forEach((id) => {
            if (!document.getElementById(id)?.value.trim()) isValid = false;
        });
    } else if (role === "student") {
        const required = [
            "studentName",
            "studentCollege",
            "studentDepartment",
            "studentEnrollment",
            "studentSemester",
            "studentDivision",
            "studentPhone",
            "studentEmail",
            "studentMentor",
        ];
        markRegisterRequiredFields(required);
        required.forEach((id) => {
            if (!document.getElementById(id)?.value.trim()) isValid = false;
        });
    } else if (role === "parent") {
        const required = [
            "parentEmail",
            "parentCollege",
            "parentStudentEnrollment",
            "parentBranch",
            "parentDivision",
            "parentRollNo",
        ];
        markRegisterRequiredFields(required);
        required.forEach((id) => {
            if (!document.getElementById(id)?.value.trim()) isValid = false;
        });
    }

    if (isValid) {
        const formData = new FormData(document.getElementById("registrationForm"));

        console.log("Form Data:", {
            role: formData.get("role"),
            password: "***",
        });

        alert(
            `Registration form submitted for ${registerRoleTitles[role]}!\n\nEmail: ${formData.get("email")}\nRole: ${registerRoleTitles[role]}`
        );

        if (registerModalInstance) registerModalInstance.hide();
    }
}
