document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("theme-toggle");
    const icon = document.getElementById("theme-icon");
    const body = document.body;

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        body.classList.add("dark-theme");
        if (icon) {
            icon.classList.remove("bi-moon-stars-fill");
            icon.classList.add("bi-sun-fill");
        }
    }

    if (toggleButton) {
        toggleButton.addEventListener("click", function () {
            body.classList.toggle("dark-theme");

            const isDark = body.classList.contains("dark-theme");
            localStorage.setItem("theme", isDark ? "dark" : "light");

            if (icon) {
                icon.classList.toggle("bi-moon-stars-fill", !isDark);
                icon.classList.toggle("bi-sun-fill", isDark);
            }
        });
    }
});