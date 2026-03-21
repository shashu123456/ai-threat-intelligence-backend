const email = document.getElementById("email");
const password = document.getElementById("password");

const emailError = document.getElementById("emailError");
const bar = document.getElementById("bar");
const text = document.getElementById("strengthText");

// EMAIL VALIDATION
email.addEventListener("input", () => {
    const val = email.value;

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
        emailError.textContent = "Invalid email format";
    } else {
        emailError.textContent = "";
    }
});

// PASSWORD STRENGTH
password.addEventListener("input", () => {
    let val = password.value;
    let score = 0;

    if (val.length >= 8) score++;
    if (/[A-Z]/.test(val)) score++;
    if (/[0-9]/.test(val)) score++;
    if (/[^A-Za-z0-9]/.test(val)) score++;

    const colors = ["red","orange","yellow","green"];
    const labels = ["Weak","Fair","Good","Strong"];

    bar.style.width = (score * 25) + "%";
    bar.style.background = colors[score - 1] || "transparent";
    text.textContent = labels[score - 1] || "";
});