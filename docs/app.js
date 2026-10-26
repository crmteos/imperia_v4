/* docs/app.js - Imperia v4 GitHub Pages Dashboard (Step E) */
/* Step E: Dashboard Widgets & Real Telemetry Render Engine */

document.addEventListener("DOMContentLoaded", () => {
  const TELEMETRY_FEED_URL = "/telemetry_feed.json";
const bTelemetry = {
  system_status: "PERFORMANCE",
  ramUtilization_percent: 42.8,
  coherence_factor: 0.94,
  active_nodes_count: 7,
  environment_vectors: {
    spatial_coherence: 0.89,
    resonance_factor: 0.95
  },
  regionsb: [
    {region_id: 101, code: "KYIV", name: "Київський регіон", status: "good", social_tension: "low"},
    {region_id: 102, code: "LVIV", name: "Львівський регіон", status: "good", social_tension: "low"},
    {region_id: 103, code: "ODESA", name: "Одеський регіон", status: "partial", social_tension: "medium"},
    {region_id: 104, code: "KHARKIV", name: "Харківський регіон", status: "partial", social_tension: "medium"},
    {region_id: 105, code: "DNIPRO", name: "Дніпровський регіон", status: "good", social_tension: "low"}
  ],
  active_signals_feed: [
    {
      signal_id: "SIG_20261026_001",
      region_id: 101,
      territory_id: "TERR_UA_KYIV_CENTRAL",
      raw_text: "Live geopolitical OSINT signal detected for Kyiv Central territory.",
      timestamp: "2026-10-26T22:18:07Z"
    }
  ]
};
  const elements = { panels: {} };
function initElements() {
  elements.panels = {
    modeDisplay: document.getElementById("mode-display"),
    vectorGrid: document.querySelector(".vector-grid"),
    h3Canvas: document.getElementById("h3-canvas"),
    peerList: document.querySelector(".peer-list"),
    signalsSection: document.querySelector(".b-section"),
    ramPercent: document.getElementById("ram-percent"),
    ramUsage: document.querySelector(".ram-usage")
  };
}
function renderRamWidget(telemetry, isFallback = false) {
  const ramPercent = elements.panels.ramPercent;
  const ramUsage = elements.panels.ramUsage;
  if (!ramPercent || !ramUsage) return;
  const ramState = telemetry?.ramUtilization_percent ?? bTelemetry.ramUtilization_percent;
  ramPercent.textContent = `${ramState.toFixed(1)}%`;
  if (ramState > 75) { ramPercent.parentElement.style.color = "#ff6b6b"; updateMode("critical"); }
  else if (ramState > 50) { ramPercent.parentElement.style.color = "#ffd93d"; updateMode("balanced"); }
  else { ramPercent.parentElement.style.color = "#6bcb77"; updateMode("performance"); }
  if (ramUsage) {
    ramUsage.innerHTML = `<strong>b Utilization:</strong> ${ramState.toFixed(1)}%<br><small>${isFallback ? "Local data" : "Live telemetry"}</small>`;
  }
}

function renderEnvVectorsWidget(telemetry, isFallback = false) {
  const grid = elements.panels.vectorGrid;
  if (!grid) return;
  const envVectors = telemetry?.environment_vectors ?? bTelemetry.environment_vectors;
  const axes = ["E_geo", "E_resource", "E_coherence", "E_temporal"];
  const labels = ["Geo", "Resource", "Coherence", "Temporal"];
  grid.innerHTML = "";
  axes.forEach((axis, i) => {
    const magnitude = (envVectors[axis] && envVectors[axis].magnitude) ?? (bTelemetry.environment_vectors[axis] && bTelemetry.environment_vectors[axis].magnitude) ?? 0;
    const div = document.createElement("div");
    div.className = "vector-item";
    div.innerHTML = `<span class="axis">${labels[i]}</span><span class="magnitude">${magnitude.toFixed(2)}</span>`;
    grid.appendChild(div);
  });
  const vectorsTitle = grid.parentElement.querySelector("h3");
  if (vectorsTitle) { vectorsTitle.textContent = "Environment Vectors E" + (isFallback ? " (Fallback)" : ""); }
}

function renderRegionalPassportsWidget(telemetry, isFallback = false) {
  const { vectorGrid } = elements.panels;
  if (!vectorGrid) return;
  const regions = telemetry?.regions ?? bTelemetry.regionsb;
  vectorGrid.innerHTML = "<h4>Regional Passports Grid (5 Ukrainian Regions)</h4>";
  regions.forEach(region => {
    const statusColor = region.status === "good" ? "#6bcb77" : region.status === "partial" ? "#ffd93d" : "#ff6b6b";
    const div = document.createElement("div");
    div.innerHTML = `<div class="region-card" style="border-left: 4px solid ${statusColor}"><strong>${region.name}</strong> (${region.code})<div style="font-size: 0.8em; margin-top: 4px">Status: <span style="color: ${statusColor}">${region.status}</span><br>Tension: <span style="color: #888">${region.social_tension}</span></div></div>`;
    vectorGrid.appendChild(div);
  });
}

function renderOsintSignalsWidget(telemetry, isFallback = false) {
  const { signalsSection } = elements.panels;
  if (!signalsSection) return;
  const signals = telemetry?.active_signals_feed ?? bTelemetry.active_signals_feed;
  const badge = document.createElement("span");
  badge.className = "badge";
  badge.id = "b-count";
  badge.textContent = signals.length;
  signalsSection.innerHTML = `<h4>Live OSINT Signals Feed <span class="badge" id="b-count">${signals.length}</span></h4><div class="b-list">${signals.map(s => "<div class=b-item><strong>" + s.signal_id + "</strong>: " + s.raw_text + "</div>").join("")}</div>`;
  if (!isFallback) { signalsSection.innerHTML += "<p class=b-note>Auto-refresh every 15s | " + signals.length + " active signals</p>"; }
}

function updateMode(mode) {
  const modeMap = { critical: "mode-c", balanced: "mode-b", performance: "mode-p" };
  const modeDisplay = elements.panels.modeDisplay;
  if (!modeDisplay) return;
  if (mode) { modeDisplay.className = "mode-indicator " + (modeMap[mode] || mode); modeDisplay.textContent = mode.toUpperCase(); }
}

async function updateDashboard() {
  try {
    const response = await fetch(TELEMETRY_FEED_URL);
    if (!response.ok) throw new Error("HTTP " + response.status);
    const telemetry = await response.json();
    const effectiveTelemetry = telemetry && telemetry.system_status ? telemetry : bTelemetry;
    renderRamWidget(effectiveTelemetry, false);
    renderEnvVectorsWidget(effectiveTelemetry, false);
    renderRegionalPassportsWidget(effectiveTelemetry, false);
    renderOsintSignalsWidget(effectiveTelemetry, false);
    const resourceMode = effectiveTelemetry.ramUtilization_percent || 0;
    if (resourceMode > 90) updateMode("critical");
    else if (resourceMode > 70) updateMode("balanced");
    else updateMode("performance");
  } catch (error) {
    console.error("Failed to fetch telemetry feed:", error);
    const effectiveTelemetry = bTelemetry;
    renderRamWidget(effectiveTelemetry, true);
    renderEnvVectorsWidget(effectiveTelemetry, true);
    renderRegionalPassportsWidget(effectiveTelemetry, true);
    renderOsintSignalsWidget(effectiveTelemetry, true);
    updateMode("performance");
  }
}

initElements();
updateDashboard();
setInterval(updateDashboard, 15000);
});
