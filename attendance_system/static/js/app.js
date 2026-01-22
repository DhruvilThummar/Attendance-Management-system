console.log("Attendance system assets loaded");

document.addEventListener("DOMContentLoaded", () => {
	const loginForms = document.querySelectorAll("[data-login-form]");
	if (!loginForms.length) return;

	const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	const passwordPattern = /^(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).{8,}$/;

	loginForms.forEach((loginForm) => {
		const emailInput = loginForm.querySelector("input[name='email']");
		const passwordInput = loginForm.querySelector("input[name='password']");
		const clientError = loginForm.querySelector("#login-client-error");
		const capsWarning = loginForm.querySelector("#caps-warning");
		const toggleBtn = loginForm.querySelector("[data-password-toggle]");
		const submitBtn = loginForm.querySelector("button[type='submit']");

		const resetSubmitState = () => {
			if (submitBtn) {
				submitBtn.disabled = false;
				submitBtn.innerHTML = `<i class=\"bi bi-box-arrow-in-right me-2\"></i>Continue`;
			}
		};

		loginForm.addEventListener("submit", (event) => {
			const messages = [];
			const email = (emailInput?.value || "").trim();
			const password = (passwordInput?.value || "").trim();

			if (!emailPattern.test(email)) {
				messages.push("Enter a valid email address (e.g., name@example.com).");
			}

			if (!passwordPattern.test(password)) {
				messages.push("Password needs 1 uppercase, 1 number, 1 special character, and 8+ characters.");
			}

			if (messages.length) {
				event.preventDefault();
				if (clientError) {
					clientError.textContent = messages.join(" ");
					clientError.classList.remove("d-none");
					clientError.scrollIntoView({ behavior: "smooth", block: "center" });
				}
				resetSubmitState();
			} else if (clientError) {
				clientError.classList.add("d-none");
			}

			if (!messages.length && submitBtn) {
				submitBtn.disabled = true;
				submitBtn.innerHTML = `<span class=\"spinner-border spinner-border-sm me-2\" role=\"status\" aria-hidden=\"true\"></span>Signing in...`;
			}
		});

		if (toggleBtn && passwordInput) {
			toggleBtn.addEventListener("click", () => {
				const isPassword = passwordInput.type === "password";
				passwordInput.type = isPassword ? "text" : "password";
				toggleBtn.innerHTML = isPassword ? '<i class="bi bi-eye-slash"></i>' : '<i class="bi bi-eye"></i>';
			});
		}

		if (passwordInput && capsWarning) {
			passwordInput.addEventListener("keyup", (e) => {
				const caps = e.getModifierState && e.getModifierState("CapsLock");
				capsWarning.classList.toggle("d-none", !caps);
			});
			passwordInput.addEventListener("blur", () => capsWarning.classList.add("d-none"));
		}

		[emailInput, passwordInput].forEach((el) => {
			if (!el) return;
			el.addEventListener("input", () => {
				resetSubmitState();
				if (clientError) clientError.classList.add("d-none");
			});
		});
	});
});
