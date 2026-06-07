const themeToggle = document.getElementById("dark-mode");

function setTheme(theme) {
    document.body.classList.remove("theme-dark", "theme-light");
    document.body.classList.add(`theme-${theme}`);
    localStorage.setItem("siteTheme", theme);
}

function changeTheme(nextTheme) {
    const directionClass = nextTheme === "light" ? "to-light" : "to-dark";

    document.documentElement.classList.remove("to-light", "to-dark");
    document.documentElement.classList.add(directionClass);

    if (!document.startViewTransition) {
        setTheme(nextTheme);
        document.documentElement.classList.remove("to-light", "to-dark");
        return;
    }

    document.documentElement.classList.add("theme-changing");

    const transition = document.startViewTransition(() => {
        setTheme(nextTheme);
    });

    transition.ready.then(() => {
        document.documentElement.classList.remove("theme-changing");
    });

    transition.finished.then(() => {
        document.documentElement.classList.remove("to-light", "to-dark", "theme-changing");
    });
}

const savedTheme = localStorage.getItem("siteTheme") || "dark";

setTheme(savedTheme);

if (themeToggle) {
    themeToggle.checked = savedTheme === "light";

    themeToggle.addEventListener("change", function () {
        const nextTheme = this.checked ? "light" : "dark";
        changeTheme(nextTheme);
    });
}