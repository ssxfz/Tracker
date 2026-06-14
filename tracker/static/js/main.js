const themeToggle = document.getElementById("dark-mode");
const useTimerCheckbox = document.getElementById("id_use_timer");
const timerSettings = document.getElementById("timerSettings");

function updateTimerSettingsVisibility() {
    if (!useTimerCheckbox || !timerSettings) {
        return;
    }

    timerSettings.style.display = useTimerCheckbox.checked
        ? "block"
        : "none";
}

updateTimerSettingsVisibility();

useTimerCheckbox?.addEventListener(
    "change",
    updateTimerSettingsVisibility
);

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
function getCsrfToken() {
    const tokenInput = document.querySelector(
        "input[name='csrfmiddlewaretoken']"
    );

    return tokenInput ? tokenInput.value : "";
}

document.querySelectorAll(".habit-timer").forEach((timerBox) => {
    const startButton = timerBox.querySelector(".start-timer-button");
    const doneButton = timerBox.querySelector(".done-button");
    const timerDisplay = timerBox.querySelector(".timer-display");

    const requiredMinutes = Number(
        timerBox.dataset.requiredMinutes
    );

    const requiredSeconds = requiredMinutes * 60;

    let timerInterval = null;

    function formatTime(totalSeconds) {
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;

        return (
            String(minutes).padStart(2, "0") +
            ":" +
            String(seconds).padStart(2, "0")
        );
    }

    startButton.addEventListener("click", async () => {
        startButton.disabled = true;
        startButton.textContent = "Starting...";

        try {
            const response = await fetch(startButton.dataset.startUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                    "X-Requested-With": "XMLHttpRequest",
                },
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Could not start timer"
                );
            }

            const startedAt = new Date(data.started_at);

            startButton.textContent = "Timer running";

            function updateTimer() {
                const now = new Date();

                const elapsedSeconds = Math.floor(
                    (now.getTime() - startedAt.getTime()) / 1000
                );

                timerDisplay.textContent = formatTime(
                    elapsedSeconds
                );

                if (elapsedSeconds >= requiredSeconds) {
                    doneButton.disabled = false;
                    doneButton.textContent = "Done today";

                    startButton.textContent = "Completed";
                    clearInterval(timerInterval);
                }
            }

            updateTimer();

            timerInterval = setInterval(updateTimer, 1000);
        } catch (error) {
            console.error(error);

            startButton.disabled = false;
            startButton.textContent = "Start timer";

            alert(error.message);
        }
    });
});