/**
 * UI Interactions Module
 * Handles visual toggles, warnings, and alerts.
 */

export function initPasswordToggles() {
    document.querySelectorAll("[data-password-toggle]").forEach(btn => {
        btn.addEventListener("click", function () {
            const inputGroup = this.closest(".position-relative, .input-group");
            if (!inputGroup) return;

            const input = inputGroup.querySelector("input");
            const icon = this.querySelector("i");

            if (input.type === "password") {
                input.type = "text";
                icon.classList.replace("bi-eye", "bi-eye-slash");
            } else {
                input.type = "password";
                icon.classList.replace("bi-eye-slash", "bi-eye");
            }
        });
    });
}

export function initCapsLockWarning() {
    document.querySelectorAll("input[type='password']").forEach(input => {
        const warning = input.closest("form")?.querySelector("#caps-warning");
        if (!warning) return;

        input.addEventListener("keydown", (e) => {
            if (e.getModifierState("CapsLock")) {
                warning.classList.remove("d-none");
            } else {
                warning.classList.add("d-none");
            }
        });
    });
}

export function initAutoDismiss() {
    document.querySelectorAll(".alert-dismissible").forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}
