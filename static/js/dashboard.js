/* ═══════════════════════════════════════════════════════════════════
   CyberShield CTI — Dashboard JavaScript
   Production-grade: SocketIO, Leaflet, Scanner, Chatbot, Logs, Map
   ═══════════════════════════════════════════════════════════════════ */

"use strict";

// ── State ─────────────────────────────────────────────────────────────────────
const State = {
  lastScanResult: null,
  scanStats: { total: 0, phishing: 0, safe: 0, riskSum: 0 },
  logCount: 0,
  mapMarkers: [],
  mapLines: [],
  currentFilter: "all",
  userLocation: { lat: 37.7749, lon: -122.4194, label: "San Francisco, US" }, // fallback
};

// ── DOM Refs ──────────────────────────────────────────────────────────────────
const $ = (id) => document.getElementById(id);

// ── Socket ────────────────────────────────────────────────────────────────────
const socket = io({ transports: ["websocket", "polling"] });

socket.on("connect", () => setConnectionStatus(true));
socket.on("disconnect", () => setConnectionStatus(false));

socket.on("scan_result", (data) => {
  State.lastScanResult = data;
  renderScanResult(data);
  updateStats(data);
  addMapMarker(data);
});

socket.on("scan_log", (data) => {
  appendTerminalLog(data.level, data.message);
});

socket.on("new_log", (data) => {
  appendLogEntry(data);
  incrementLogBadge();
});

socket.on("high_risk_alert", (data) => {
  showAlertBanner(data.message);
  setThreatLevel("critical");
});

// ── Clock ─────────────────────────────────────────────────────────────────────
function updateClock() {
  const now = new Date();
  const ts = now.toUTCString().replace("GMT", "UTC");
  $("topbarClock").textContent = ts.slice(5, 25);
}
setInterval(updateClock, 1000);
updateClock();

// ── Navigation ────────────────────────────────────────────────────────────────
document.querySelectorAll(".nav-item").forEach((item) => {
  item.addEventListener("click", () => {
    const section = item.dataset.section;
    navigateTo(section, item);
  });
});

function navigateTo(section, navItem) {
  document.querySelectorAll(".nav-item").forEach((i) => i.classList.remove("active"));
  document.querySelectorAll(".content-section").forEach((s) => s.classList.remove("active"));

  if (navItem) navItem.classList.add("active");
  const el = $(`section-${section}`);
  if (el) el.classList.add("active");

  const labels = {
    scanner: "URL Scanner",
    map: "Attack Map",
    logs: "Threat Logs",
    assistant: "AI Assistant",
  };
  $("currentSection").textContent = labels[section] || section;

  // Reset log badge when visiting logs
  if (section === "logs") {
    $("logBadge").textContent = "0";
    $("logBadge").style.display = "none";
    State.logCount = 0;
    loadLogs();
  }

  // Init map on first view
  if (section === "map" && !window._mapInitialised) {
    initMap();
    window._mapInitialised = true;
  }
}

$("sidebarToggle").addEventListener("click", () => {
  document.getElementById("sidebar").classList.toggle("open");
});

// ── Scanner ───────────────────────────────────────────────────────────────────
$("urlInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter") startScan();
});

async function startScan() {
  const url = $("urlInput").value.trim();
  if (!url) {
    shakeInput();
    return;
  }

  setScanningState(true);
  showProgress();

  try {
    const resp = await fetch("/api/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.error || "Scan failed");
    }
    // Result handled via socket event `scan_result`
  } catch (err) {
    showScanError(err.message);
  } finally {
    setScanningState(false);
    hideProgress();
  }
}

function setScanningState(scanning) {
  const btn = $("scanBtn");
  const btnText = btn.querySelector(".btn-text");
  const btnLoading = btn.querySelector(".btn-loading");
  btn.disabled = scanning;
  btnText.style.display = scanning ? "none" : "flex";
  btnLoading.style.display = scanning ? "flex" : "none";
}

function showProgress() {
  const prog = $("scanProgress");
  const fill = $("progressFill");
  const steps = $("progressSteps");
  prog.style.display = "block";

  const stages = [
    "Extracting URL features...",
    "Running ML prediction...",
    "Resolving domain to IP...",
    "Querying threat intelligence...",
    "Generating risk score...",
  ];

  let i = 0;
  const pct = [15, 35, 55, 80, 100];
  window._progressInterval = setInterval(() => {
    if (i >= stages.length) {
      clearInterval(window._progressInterval);
      return;
    }
    fill.style.width = pct[i] + "%";
    steps.innerHTML = `<span class="step"><i class="fa-solid fa-circle-notch fa-spin"></i> ${stages[i]}</span>`;
    i++;
  }, 600);
}

function hideProgress() {
  clearInterval(window._progressInterval);
  setTimeout(() => {
    $("scanProgress").style.display = "none";
    $("progressFill").style.width = "0%";
  }, 500);
}

function renderScanResult(data) {
  const card = $("resultCard");
  card.style.display = "block";
  card.scrollIntoView({ behavior: "smooth", block: "nearest" });

  const isPhishing = data.prediction === "phishing";
  const score = Math.round(data.risk_score);

  // Verdict header
  $("verdictTitle").textContent = isPhishing ? "⚠ THREAT DETECTED" : "✓ SAFE";
  $("verdictTitle").style.color = isPhishing
    ? "var(--accent-red)"
    : "var(--accent-green)";
  $("verdictUrl").textContent = truncateUrl(data.url, 60);

  const icon = $("verdictIcon");
  icon.className = "verdict-icon " + (isPhishing ? "phishing" : "safe");
  icon.innerHTML = isPhishing
    ? '<i class="fa-solid fa-skull-crossbones"></i>'
    : '<i class="fa-solid fa-shield-check"></i>';

  // Score ring
  animateScoreRing(score);

  // Explanation
  const expl = $("resultExplanation");
  expl.textContent = data.explanation;
  expl.className =
    "result-explanation " + (isPhishing ? "phishing-explanation" : "");

  // Tiles
  const geo = data.geo_data || {};
  const threat = data.threat_data || {};

  $("tileCountry").textContent =
    geo.country && geo.city
      ? `${geo.city}, ${geo.country}`
      : geo.country || "Unknown";
  $("tileIP").textContent = data.ip_address || "Unresolved";
  $("tileConfidence").textContent =
    (data.confidence * 100).toFixed(1) + "%";
  $("tileThreatIntel").textContent = threat.flagged
    ? "⚠ Flagged by " + (threat.sources || []).join(", ")
    : threat.note
    ? "No API keys"
    : "✓ Clean";

  // Features
  if (data.features) populateFeaturesGrid(data.features);
}

function animateScoreRing(score) {
  const fill = $("ringFill");
  const val = $("scoreValue");
  const circumference = 251.2;

  fill.className = "ring-fill " + getRiskClass(score);

  let current = 0;
  const step = score / 40;
  const interval = setInterval(() => {
    current = Math.min(current + step, score);
    val.textContent = Math.round(current);
    const offset = circumference - (current / 100) * circumference;
    fill.style.strokeDashoffset = offset;
    if (current >= score) clearInterval(interval);
  }, 25);
}

function getRiskClass(score) {
  if (score >= 80) return "critical";
  if (score >= 60) return "high";
  if (score >= 40) return "medium";
  return "";
}

function populateFeaturesGrid(features) {
  const grid = $("featuresGrid");
  grid.innerHTML = "";

  const display = {
    url_length: ["URL Length", (v) => [v, v > 100]],
    domain_entropy: ["Domain Entropy", (v) => [v.toFixed(2), v > 3.5]],
    has_https: ["HTTPS", (v) => [v ? "Yes" : "No", !v]],
    has_ip: ["IP in URL", (v) => [v ? "Yes" : "No", !!v]],
    has_at_symbol: ["@ Symbol", (v) => [v ? "Yes" : "No", !!v]],
    is_shortened: ["Shortened URL", (v) => [v ? "Yes" : "No", !!v]],
    has_suspicious_tld: ["Suspicious TLD", (v) => [v ? "Yes" : "No", !!v]],
    has_brand_keyword: ["Brand Keyword", (v) => [v ? "Yes" : "No", !!v]],
    num_subdomains: ["Subdomains", (v) => [v, v > 3]],
    num_hyphens: ["Hyphens", (v) => [v, v > 3]],
    has_port: ["Non-std Port", (v) => [v ? "Yes" : "No", !!v]],
    digit_ratio: ["Digit Ratio", (v) => [(v * 100).toFixed(0) + "%", v > 0.3]],
    special_char_ratio: ["Special Chars", (v) => [(v * 100).toFixed(0) + "%", v > 0.2]],
  };

  Object.entries(display).forEach(([key, [label, fn]]) => {
    if (!(key in features)) return;
    const [displayVal, flagged] = fn(features[key]);
    const item = document.createElement("div");
    item.className = "feature-item";
    item.innerHTML = `
      <span class="feature-name">${label}</span>
      <span class="feature-value ${flagged ? "flagged" : "ok"}">${displayVal}</span>
    `;
    grid.appendChild(item);
  });
}

function toggleFeatures() {
  const grid = $("featuresGrid");
  const btn = document.querySelector(".features-toggle");
  const visible = grid.style.display !== "none";
  grid.style.display = visible ? "none" : "grid";
  btn.innerHTML = visible
    ? '<i class="fa-solid fa-code"></i> Show Feature Analysis'
    : '<i class="fa-solid fa-code"></i> Hide Feature Analysis';
}

function updateStats(data) {
  const s = State.scanStats;
  s.total++;
  s.riskSum += data.risk_score;
  if (data.prediction === "phishing") s.phishing++;
  else s.safe++;

  $("statTotal").textContent = s.total;
  $("statPhishing").textContent = s.phishing;
  $("statSafe").textContent = s.safe;
  $("statAvgRisk").textContent = (s.riskSum / s.total).toFixed(0);
}

function showScanError(msg) {
  const card = $("resultCard");
  card.style.display = "block";
  card.innerHTML = `
    <div style="padding:28px;text-align:center;color:var(--accent-red);">
      <i class="fa-solid fa-triangle-exclamation fa-2x" style="margin-bottom:12px;"></i>
      <p style="font-weight:600;">Scan Error</p>
      <p style="font-size:12px;color:var(--text-muted);margin-top:6px;">${msg}</p>
    </div>
  `;
}

function shakeInput() {
  const input = $("urlInput");
  input.style.animation = "none";
  input.offsetHeight; // force reflow
  input.style.animation = "shake 0.4s ease";
  setTimeout(() => (input.style.animation = ""), 400);
}

// Inject shake keyframe dynamically
const shakeStyle = document.createElement("style");
shakeStyle.textContent = `@keyframes shake {
  0%,100% { transform: translateX(0); }
  20%,60% { transform: translateX(-6px); }
  40%,80% { transform: translateX(6px); }
}`;
document.head.appendChild(shakeStyle);

function truncateUrl(url, max) {
  return url.length > max ? url.slice(0, max) + "…" : url;
}

// ── Map ───────────────────────────────────────────────────────────────────────
let map;
let threatCount = 0;

function initMap() {
  map = L.map("attackMap", {
    center: [20, 0],
    zoom: 2,
    zoomControl: true,
    attributionControl: false,
  });

  L.tileLayer(
    "[{s}.basemaps.cartocdn.com](https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png)",
    { maxZoom: 18, subdomains: "abcd" }
  ).addTo(map);

  // Add user marker
  const userIcon = L.divIcon({
    className: "",
    html: `<div style="
      width:14px;height:14px;border-radius:50%;
      background:var(--accent-cyan);
      box-shadow:0 0 12px var(--accent-cyan),0 0 24px rgba(0,212,255,0.4);
      border:2px solid rgba(255,255,255,0.8);
    "></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  });

  L.marker([State.userLocation.lat, State.userLocation.lon], { icon: userIcon })
    .addTo(map)
    .bindPopup(
      `<b style="color:#00d4ff">🛡 Your Location</b><br>${State.userLocation.label}`
    );

  // Load existing scans onto map
  fetch("/api/scans/recent")
    .then((r) => r.json())
    .then((scans) => scans.forEach(addMapMarker));
}

function addMapMarker(data) {
  if (!map || !window._mapInitialised) return;

  const geo = data.geo_data || {};
  if (!geo.lat || !geo.lon || (geo.lat === 0 && geo.lon === 0)) return;

  const isPhishing = data.prediction === "phishing";
  const color = isPhishing ? "#ff2d55" : "#00ff9d";
  const glowColor = isPhishing
    ? "rgba(255,45,85,0.5)"
    : "rgba(0,255,157,0.4)";

  const icon = L.divIcon({
    className: "",
    html: `<div style="
      width:10px;height:10px;border-radius:50%;
      background:${color};
      box-shadow:0 0 10px ${glowColor},0 0 20px ${glowColor};
      border:1px solid rgba(255,255,255,0.6);
    "></div>`,
    iconSize: [10, 10],
    iconAnchor: [5, 5],
  });

  const marker = L.marker([geo.lat, geo.lon], { icon }).addTo(map);
  marker.bindPopup(`
    <div style="font-family:'JetBrains Mono',monospace;font-size:11px;line-height:1.6;">
      <b style="color:${color}">${isPhishing ? "⚠ THREAT" : "✓ SAFE"}</b><br>
      <b>IP:</b> ${data.ip_address || "—"}<br>
      <b>Location:</b> ${geo.city || ""}, ${geo.country || "Unknown"}<br>
      <b>Risk:</b> ${Math.round(data.risk_score)}/100<br>
      <b>ISP:</b> ${geo.isp || "—"}<br>
      <b>URL:</b> ${truncateUrl(data.url, 40)}
    </div>
  `);

  // Animated line from threat to defender
  if (isPhishing) {
    const line = L.polyline(
      [
        [geo.lat, geo.lon],
        [State.userLocation.lat, State.userLocation.lon],
      ],
      {
        color: "#ff2d55",
        weight: 1.5,
        opacity: 0.6,
        dashArray: "4 6",
      }
    ).addTo(map);
    State.mapLines.push(line);
    animateLineFade(line);
  }

  State.mapMarkers.push(marker);
  threatCount++;
  $("mapThreatCount").textContent = `${threatCount} threat${threatCount !== 1 ? "s" : ""} mapped`;
}

function animateLineFade(line) {
  let opacity = 0.6;
  const interval = setInterval(() => {
    opacity -= 0.01;
    if (opacity <= 0.1) {
      clearInterval(interval);
      line.setStyle({ opacity: 0.1 });
      return;
    }
    line.setStyle({ opacity });
  }, 80);
}

// ── Logs ──────────────────────────────────────────────────────────────────────
function loadLogs() {
  fetch("/api/logs?limit=100")
    .then((r) => r.json())
    .then((logs) => {
      $("logStream").innerHTML = "";
      logs.reverse
