document.addEventListener("DOMContentLoaded", () => {
    // Show or hide the password in the field linked to each toggle button.
    document.querySelectorAll(".toggle-password").forEach((button) => {
        const input = document.getElementById(button.dataset.target);

        button.addEventListener("click", () => {
            const isHidden = input.type === "password";
            input.type = isHidden ? "text" : "password";
            button.textContent = isHidden ? "Hide" : "Show";
            button.setAttribute("aria-pressed", String(isHidden));
        });
    });

    const passwordInput = document.getElementById("password");
    const confirmInput = document.getElementById("confirm_password");
    const confirmFeedback = document.getElementById("confirm-feedback");
    const ruleItems = document.querySelectorAll(".password-rules li");

    // Mark each password rule as met while the user types.
    function updatePasswordRules() {
        const value = passwordInput.value;
        const checks = {
            length: value.length >= 8,
            letter: /[A-Za-z]/.test(value),
            number: /\d/.test(value),
        };
        ruleItems.forEach((item) => {
            item.classList.toggle("is-met", checks[item.dataset.rule]);
        });
    }

    // Tell the user whether the confirmation matches the password.
    function updateConfirmFeedback() {
        if (!confirmInput.value) {
            confirmFeedback.textContent = "";
            confirmFeedback.className = "field-feedback";
            return;
        }
        const matches = confirmInput.value === passwordInput.value;
        confirmFeedback.textContent = matches ? "Passwords match." : "Passwords do not match.";
        confirmFeedback.className = "field-feedback " + (matches ? "is-valid" : "is-invalid");
    }

    if (passwordInput && ruleItems.length) {
        passwordInput.addEventListener("input", () => {
            updatePasswordRules();
            if (confirmInput) {
                updateConfirmFeedback();
            }
        });
    }

    if (confirmInput && confirmFeedback) {
        confirmInput.addEventListener("input", updateConfirmFeedback);
    }
});
