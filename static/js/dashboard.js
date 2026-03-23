document.addEventListener("DOMContentLoaded", () => {

    const socket = io();

    const urlInput = document.getElementById("urlInput");
    const chatInput = document.getElementById("chatInput");

    /* DEFAULT PAGE */
    show("scan");

    /* ENTER FIX */
    if (urlInput) {
        urlInput.addEventListener("keydown", e => {
            if (e.key === "Enter") scan();
        });
    }

    if (chatInput) {
        chatInput.addEventListener("keydown", e => {
            if (e.key === "Enter") sendChat();
        });
    }

    /* MAP INIT */
    window.map = L.map('mapBox').setView([20, 78], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
        .addTo(map);

    let userMarker = null;
    let attackerMarker = null;
    let attackLine = null;

    function updateMap(geo) {

        if (!geo) return;

        const user = [12.97, 77.59];
        const attacker = [geo.lat || 0, geo.lon || 0];

        /* REMOVE OLD */
        if (userMarker) map.removeLayer(userMarker);
        if (attackerMarker) map.removeLayer(attackerMarker);
        if (attackLine) map.removeLayer(attackLine);

        /* ADD NEW */
        userMarker = L.marker(user).addTo(map).bindPopup("🟢 User");
        attackerMarker = L.marker(attacker).addTo(map).bindPopup("🔴 Attacker");

        attackLine = L.polyline([user, attacker], {
            color: "red"
        }).addTo(map);

        map.fitBounds([user, attacker]);
    }

    /* SOCKET RESULT */
    socket.on("scan_result", data => {

        const box = document.getElementById("result");

        if (!box) return;

        if (data.prediction === "PHISHING") {

            box.style.background = "#7f1d1d";

            box.innerHTML = `
                🚨 PHISHING <br>
                Risk: ${data.risk}% <br>
                IP: ${data.geo?.ip || "Unknown"}
            `;

        } else {

            box.style.background = "#14532d";

            box.innerHTML = `
                SAFE <br>
                Risk: ${data.risk}%
            `;
        }

        updateMap(data.geo);
    });

});


/* NAV */
function show(id) {

    document.querySelectorAll(".section").forEach(s => {
        s.classList.remove("active");
    });

    const el = document.getElementById(id);
    if (el) el.classList.add("active");

    /* FIX MAP RENDER */
    if (id === "map") {
        setTimeout(() => {
            if (window.map) map.invalidateSize();
        }, 300);
    }
}


/* SCAN */
async function scan() {

    const input = document.getElementById("urlInput");

    if (!input) return;

    const url = input.value.trim();

    if (!url) {
        alert("Enter URL");
        return;
    }

    try {
        await fetch("/scan", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ url })
        });
    } catch (err) {
        console.error("Scan error:", err);
    }
}


/* CHAT */
async function sendChat() {

    const input = document.getElementById("chatInput");
    const box = document.getElementById("chatBox");

    if (!input || !box) return;

    const msg = input.value.trim();

    if (!msg) return;

    /* USER MESSAGE */
    box.innerHTML += `<div style="text-align:right;color:cyan;">You: ${msg}</div>`;

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ message: msg })
        });

        const data = await res.json();

        /* BOT MESSAGE */
        box.innerHTML += `<div style="color:#22c55e;">AI: ${data.reply}</div>`;

        box.scrollTop = box.scrollHeight;

    } catch (err) {
        box.innerHTML += `<div style="color:red;">Error</div>`;
    }

    input.value = "";
}