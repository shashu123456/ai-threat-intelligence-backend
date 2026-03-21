const socket = io();

/* ================= NAVIGATION ================= */
function show(id) {
    document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

/* ================= LOG STREAM ================= */
socket.on("log", msg => {
    const box = document.getElementById("logBox");

    const line = document.createElement("div");
    line.innerText = "> " + msg;

    box.appendChild(line);
    box.scrollTop = box.scrollHeight;
});

/* ================= SCAN ================= */
async function scan() {
    const url = document.getElementById("urlInput").value;

    if (!url) {
        alert("Enter URL first");
        return;
    }

    await fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url})
    });
}

/* ================= RESULT ================= */
socket.on("scan_result", data => {

    const box = document.getElementById("result");
    box.classList.add("show");

    const totalEl = document.getElementById("total");
    totalEl.innerText = parseInt(totalEl.innerText || "0") + 1;

    /* 🔒 SAFE EXPLANATION HANDLING */
    let explanationHTML = "";

    if (Array.isArray(data.explanation)) {
        explanationHTML = data.explanation.join("<br>");
    } else {
        explanationHTML = "No explanation available";
    }

    if (data.prediction === "PHISHING") {

        box.style.background = "#7f1d1d";

        box.innerHTML = `
        🚨 PHISHING DETECTED <br>
        Risk: ${data.risk}% <br>
        IP: ${data.geo?.ip || "Unknown"} <br>
        ${data.geo?.city || "Unknown"}, ${data.geo?.country || "Unknown"} <br><br>

        <b>Why detected:</b><br>
        ${explanationHTML}
        `;

        document.getElementById("alertBanner").style.display = "block";
        document.getElementById("status").innerText = "🔴 Threat Detected";

        const threatEl = document.getElementById("threats");
        threatEl.innerText = parseInt(threatEl.innerText || "0") + 1;

        document.body.style.boxShadow = "inset 0 0 120px red";

    } else {

        box.style.background = "#14532d";

        box.innerHTML = `
        SAFE <br>
        Risk: ${data.risk}% <br>
        IP: ${data.geo?.ip || "Unknown"} <br><br>

        ${explanationHTML}
        `;

        document.body.style.boxShadow = "none";
        document.getElementById("alertBanner").style.display = "none";
        document.getElementById("status").innerText = "🟢 Secure";
    }

    updateMap(data.geo || {});
});

/* ================= MAP ================= */

let map = L.map('mapBox').setView([20, 78], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
.addTo(map);

/* STORE CURRENT ELEMENTS */
let userMarker = null;
let attackerMarker = null;
let attackLine = null;

function updateMap(geo) {

    const user = [12.97, 77.59];
    const attacker = [geo.lat || 0, geo.lon || 0];

    /* REMOVE OLD */
    if (userMarker) map.removeLayer(userMarker);
    if (attackerMarker) map.removeLayer(attackerMarker);
    if (attackLine) map.removeLayer(attackLine);

    /* ADD NEW */
    userMarker = L.marker(user).addTo(map).bindPopup("User");
    attackerMarker = L.marker(attacker).addTo(map).bindPopup("Attacker");

    attackLine = L.polyline([user, attacker], {
        color: 'red',
        weight: 3,
        dashArray: '6'
    }).addTo(map);

    /* ZOOM TO FIT */
    map.fitBounds([user, attacker]);
}

/* ================= AI CURSOR BOT ================= */

const bot = document.createElement("div");
bot.innerHTML = "🤖";
bot.style.position = "fixed";
bot.style.fontSize = "28px";
bot.style.pointerEvents = "none";
bot.style.transition = "transform 0.1s linear";

document.body.appendChild(bot);

document.addEventListener("mousemove", e => {
    bot.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
});

/* ================= SMART HINT SYSTEM ================= */

const hints = {
    urlInput: "Enter suspicious URL here",
    result: "Scan results will appear here",
    mapBox: "Attack origin visualization",
    logBox: "Live SOC logs streaming",
    chatBox: "AI explains threats"
};

const hintBox = document.createElement("div");
hintBox.style.position = "fixed";
hintBox.style.background = "black";
hintBox.style.color = "white";
hintBox.style.padding = "5px 10px";
hintBox.style.borderRadius = "5px";
hintBox.style.fontSize = "12px";
hintBox.style.display = "none";

document.body.appendChild(hintBox);

Object.keys(hints).forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;

    el.addEventListener("mouseenter", () => {
        hintBox.innerText = hints[id];
        hintBox.style.display = "block";
    });

    el.addEventListener("mousemove", e => {
        hintBox.style.left = (e.clientX + 15) + "px";
        hintBox.style.top = (e.clientY + 15) + "px";
    });

    el.addEventListener("mouseleave", () => {
        hintBox.style.display = "none";
    });
});