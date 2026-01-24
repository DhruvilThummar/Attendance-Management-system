/**
 * Attendify Application Logic
 * Handles global interactions like password toggling, form validation, and toast notifications.
 */

document.addEventListener("DOMContentLoaded", () => {
	console.log("Attendify JS loaded");

	// 1. Password Visibility Toggle
	// Selects all buttons with data-password-toggle attribute
	const toggleButtons = document.querySelectorAll("[data-password-toggle]");

	toggleButtons.forEach(btn => {
		btn.addEventListener("click", function () {
			// Find the sibling input
			const inputGroup = this.closest(".position-relative, .input-group");
			if (!inputGroup) return;

			const passwordInput = inputGroup.querySelector("input");
			const icon = this.querySelector("i");

			if (passwordInput.type === "password") {
				passwordInput.type = "text";
				icon.classList.remove("bi-eye");
				icon.classList.add("bi-eye-slash");
			} else {
				passwordInput.type = "password";
				icon.classList.remove("bi-eye-slash");
				icon.classList.add("bi-eye");
			}
		});
	});

	// 2. Client-side Form Validation (Bootstrap style)
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

	// 3. Login Form Enhancements (Caps Lock & Pattern Check)
	const loginForms = document.querySelectorAll("[data-login-form]");

	loginForms.forEach(form => {
		const passwordInput = form.querySelector("input[name='password']");
		const capsWarning = form.querySelector("#caps-warning");
		const clientError = form.querySelector("#login-client-error");

		// Caps Lock Warning
		if (passwordInput && capsWarning) {
			passwordInput.addEventListener("keydown", (e) => {
				if (e.getModifierState("CapsLock")) {
					capsWarning.classList.remove("d-none");
				} else {
					capsWarning.classList.add("d-none");
				}
			});
		}

		// Simple client-side submit check
		form.addEventListener("submit", (e) => {
			// Basic length check example
			if (passwordInput && passwordInput.value.length < 4) {
				// Let backend handle robust auth, but prevent obvious empty/short submits
				// e.preventDefault();
				// if (clientError) {
				//     clientError.textContent = "Password too short.";
				//     clientError.classList.remove("d-none");
				// }
			}
		});
	});

	// 4. Auto-dismiss alerts
	const alerts = document.querySelectorAll(".alert-dismissible");
	alerts.forEach(alert => {
		setTimeout(() => {
			const bsAlert = new bootstrap.Alert(alert);
			bsAlert.close();
		}, 5000);
	});
});
