const themeToggle = document.getElementById("dark-mode");

function setTheme(theme) {
    document.body.classList.remove("theme-dark", "theme-light");
    document.body.classList.add(`theme-${theme}`);
    localStorage.setItem("siteTheme", theme);
}

function animateThemeChange(nextTheme) {
    const wipeClass = nextTheme === "light"
        ? "theme-wipe-to-light"
        : "theme-wipe-to-dark";

    document.body.classList.remove(
        "theme-wipe-to-light",
        "theme-wipe-to-dark",
        "theme-wipe-reset"
    );

    // 1. Запускаємо лінію переходу
    document.body.classList.add(wipeClass);

    // 2. Майже одразу міняємо тему під рухомою лінією
    setTimeout(() => {
        setTheme(nextTheme);
    }, 80);

    // 3. Коли лінія дійшла до краю, прибираємо її без зворотної анімації
    setTimeout(() => {
        document.body.classList.add("theme-wipe-reset");

        requestAnimationFrame(() => {
            document.body.classList.remove(wipeClass);

            setTimeout(() => {
                document.body.classList.remove("theme-wipe-reset");
            }, 30);
        });
    }, 650);
}

const savedTheme = localStorage.getItem("siteTheme") || "dark";

setTheme(savedTheme);

if (themeToggle) {
    themeToggle.checked = savedTheme === "light";

    themeToggle.addEventListener("change", function () {
        const nextTheme = this.checked ? "light" : "dark";
        animateThemeChange(nextTheme);
    });
}