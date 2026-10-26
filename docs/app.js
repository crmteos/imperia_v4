/* docs/app.js - Imperia v4 GitHub Pages Dashboard (Part 1) */
/* Zero-server client-side JSON fetching from portal_bridge.py telemetry feed */

document.addEventListener("DOMContentLoaded", () => {
  const TELEMETRY_FEED_URL = "/telemetry_feed.json";

  const elements = {
    modeIndicators: {},
    panels: {}
  };

  function initElements() {
    elements.modeIndicators = {
      critical: document.querySelector(".mode-critical"),
      balanced: document.querySelector(".mode-balanced"),
      performance: document.querySelector(".mode-performance"),
    };
    elements.panels = {
      vectorGrid: document.querySelector(".vector-grid"),
      h3Canvas: document.getElementById("h3-canvas"),
      peerList: document.querySelector(".peer-list"),
      signalsSection: document.querySelector(".signal-section"),
      ramPercent: document.getElementById("ram-percent"),
    };
  }

  async function fetchTelemetry() {
    try {
      const response = await fetch(TELEMETRY_FEED_URL);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error("Failed to fetch telemetry feed:", error);
      displayError(error.message);
      return null;
    }
  }

  function displayError(message) {
    const panels = Object.values(elements.panels).filter(p => p);
    panels.forEach(p => {
      p.innerHTML = `<p style="color: var(--warning-color);">Error: ${message}</p>`;
    });
  }

  function updateMode(mode) {
    const modeMap = {
      critical: "mode-critical",
      balanced: "mode-balanced",
      performance: "mode-performance",
    };
    if (elements.modeIndicators.critical) elements.modeIndicators.critical.className = "mode-indicator mode-critical";
    if (elements.modeIndicators.balanced) elements.modeIndicators.balanced.className = "mode-indicator mode-balanced";
    if (elements.modeIndicators.performance) elements.modeIndicators.performance.className = "mode-indicator mode-performance";
    const active = elements.modeIndicators[mode];
    if (active && modeMap[mode]) active.className = `mode-indicator ${modeMap[mode]}`;
  }

  function renderEnvVectors(telemetry) {
    const grid = elements.panels.vectorGrid;
    if (!grid) return;
    if (telemetry && telemetry.telemetry) {
      const e_vector = telemetry.telemetry.e_vector || {};
      const axes = ["E_geo", "E_resource", "E_coherence", "E_temporal"];
      const labels = ["Geo", "Resource", "Coherence", "Temporal"];
      grid.innerHTML = "";
      axes.forEach((axis, i) => {
        const magnitude = (e_vector[axis] && e_vector[axis].magnitude) || 0;
        const div = document.createElement("div");
        div.className = "vector-item";
        div.innerHTML = `<span class="axis">${labels[i]}</span><span class="magnitude">${magnitude.toFixed(2)}</span>`;
        grid.appendChild(div);
      });
    }
  }

  function renderH3Grid(telemetry) {
    const canvas = elements.panels.h3Canvas;
    if (!canvas || !canvas.getContext) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const width = canvas.offsetWidth || 400;
    const height = canvas.offsetHeight || 200;
    canvas.width = width * 2;
    canvas.height = height;
    ctx.scale(2, 2);
    ctx.fillStyle = "#0a0a0f";
    ctx.fillRect(0, 0, width, height);
    if (telemetry && telemetry.telemetry) {
      const peerCount = Math.min((telemetry.telemetry.p2p_topology && telemetry.telemetry.p2p_topology.peer_count) || 0, 30);
      const cols = Math.ceil(Math.sqrt(peerCount)) || 5;
      const cellW = width / cols;
      for (let i = 0; i < peerCount; i++) {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const x = col * cellW + cellW / 2;
        const y = row * cellW + cellW / 2;
        ctx.beginPath();
        ctx.arc(x, y, cellW * 0.35, 0, Math.PI * 2);
        ctx.strokeStyle = "#00d4aa";
        ctx.lineWidth = 1;
        ctx.stroke();
      }
    }
  }

  function renderSignals(telemetry) {
    const { signalsSection } = elements.panels;
    if (!signalsSection) return;
    if (telemetry && telemetry.telemetry) {
      const signals = telemetry.telemetry.signals || {};
      const keys = Object.keys(signals).slice(0, 5);
      signalsSection.innerHTML = `<h4>Active Signals <span class="badge" id="signal-count">${keys.length}</span></h4><div class="signal-list">${keys.map(k => `<span>${k}: ${signals[k] || "—"}</span>`).join("")}</div>`;
    } else {
      signalsSection.innerHTML = "<p>No signal data available</p>";
    }
  }

  function renderRamTelemetry(telemetry) {
    const { ramPercent } = elements.panels;
    if (!ramPercent) return;
    if (telemetry && telemetry.telemetry) {
      const ram_state = telemetry.telemetry.ram_state || {};
      const utilization = ram_state.utilization_percent || 0;
      ramPercent.textContent = `${utilization.toFixed(1)}%`;
      parent = ramPercent.parentElement;
      parent.style.color = utilization > 75 ? "#ff6b6b" : utilization > 50 ? "#ffd93d" : "#6bcb77";
    }
  }

  async function updateDashboard() {
    const telemetry = await fetchTelemetry();
    if (telemetry) {
      const resourceMode = telemetry.telemetry.ram_state?.utilization_percent || 0;
      if (resourceMode > 90) updateMode("critical");
      else if (resourceMode > 70) updateMode("balanced");
      else updateMode("performance");
      renderEnvVectors(telemetry);
      renderH3Grid(telemetry);
      renderP2PTopology(telemetry);
      renderSignals(telemetry);
      renderRamTelemetry(telemetry);
    }
  }

  initElements();
  updateDashboard();

  setInterval(updateDashboard, 15000);
};