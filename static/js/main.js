document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.querySelector(".nav-toggle");
    const navMenu = document.querySelector(".nav-menu");

    // Open and close the navigation menu on small screens.
    navToggle.addEventListener("click", () => {
        const isOpen = navMenu.classList.toggle("is-open");
        navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    // Close the menu when the Escape key is pressed.
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && navMenu.classList.contains("is-open")) {
            navMenu.classList.remove("is-open");
            navToggle.setAttribute("aria-expanded", "false");
            navToggle.focus();
        }
    });

    // Remove a flash message when its close button is pressed.
    document.querySelectorAll(".flash-close").forEach((button) => {
        button.addEventListener("click", () => button.closest(".flash").remove());
    });
});
