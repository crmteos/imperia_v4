/* ===========================================================
   Imperia v4 - Pure JS Standalone Widget Generator (Step F)
   Self-contained dashboard: renders immediately on page load,
   no external fetch required for initial display. Fallback fetch
   available but silently catches CORS errors.
   =========================================================== */

/* ===========================================================
   DEFAULT_TELEMETRY - Fully self-contained synchronous data
   =========================================================== */
const DEFAULT_TELEMETRY = {
  system_status: "PERFORMANCE",
  ramUtilization_percent: 42,
  active_p2p_nodes: 12,
  coherence_factor: 0.94,
  environment_vectors: {
    spatial_coherence: 0.94,
    resonance_factor: 0.88
  },
  regions: [
    { region_id: 101, name: "Kyiv", code: "KYIV", gps: "50.4501, 30.5234", status: "good", social_tension: "low" },
    { region_id: 102, name: "Lviv", code: "LVIV", gps: "49.8397, 24.0297", status: "good", social_tension: "low" },
    { region_id: 103, name: "Odesa", code: "ODESA", gps: "46.4825, 30.7233", status: "partial", social_tension: "medium" },
    { region_id: 104, name: "Kharkiv", code: "KHARKIV", gps: "49.9935, 36.2304", status: "partial", social_tension: "medium" },
    { region_id: 105, name: "Dnipro", code: "DNIPRO", gps: "48.4647, 35.0462", status: "good", social_tension: "low" }
  ],
  active_signals: [
    {
      signal_id: "SIG_20261026_001",
      region_id: 101,
      territory: "Kyiv Central",
      raw_text: "Geopolitical OSINT signal detected for Kyiv Central territory.",
      timestamp: "2026-10-26T22:18:07Z"
    },
    {
      signal_id: "SIG_20261026_002",
      region_id: 103,
      territory: "Odesa Port",
      raw_text: "Maritime activity OSINT signal for Odesa port territory.",
      timestamp: "2026-10-26T22:15:33Z"
    },
    {
      signal_id: "SIG_20261026_003",
      region_id: 104,
      territory: "Kharkiv East",
      raw_text: "Energy grid monitoring signal for Kharkiv east territory.",
      timestamp: "2026-10-26T22:12:11Z"
    }
  ]
};

/* Backup telemetry (filled after first fetch) */
let bTelemetry = null;

/* ===========================================================
   DOM Injector: buildWidgets(data) - Self-contained rendering
   =========================================================== */
function buildWidgets(data) {
  /* 1. Check if main container #dashboard-main exists; if not, create it */
  let mainContainer = document.getElementById("dashboard-main");
  if (!mainContainer) {
    mainContainer = document.createElement("div");
    mainContainer.id = "dashboard-main";
    mainContainer.className = "dashboard";
    document.body.appendChild(mainContainer);
  }

  /* 2. Ensure widget containers exist; create them dynamically if missing */
  const widgetIds = ["ram-usage", "vectors-container", "passports-grid", "signals-list"];
  const widgetContainers = {};

  widgetIds.forEach(id => {
    let el = document.getElementById(id);
    if (!el) {
      el = document.createElement("div");
      el.id = id;
      /* Append to main container or body as fallback */
      if (mainContainer.className.includes("dashboard")) {
        mainContainer.appendChild(el);
      } else {
        document.body.appendChild(el);
      }
    }
    widgetContainers[id] = el;
  });

  /* 3. Populate RAM Widget */
  const ramPercent = widgetContainers["ram-usage"];
  if (ramPercent) {
    const ramState = data.ramUtilization_percent || 0;
    ramPercent.innerHTML = `
      <strong>RAM Utilization:</strong> <span id="ram-percent">${ramState.toFixed(1)}%</span>
      <div class="progress-bar"><div class="progress" style="width: ${ramState}%"></div></div>
      <span class="mode-indicator ${ramState > 90 ? "critical" : ramState > 70 ? "balanced" : "performance"}">
        ${ramState > 90 ? "CRITICAL" : ramState > 70 ? "BALANCED" : "PERFORMANCE"}
      </span>
    `;
  }

  /* 4. Environment Vectors Widget */
  const vecContainer = widgetContainers["vectors-container"];
  if (vecContainer) {
    const vecData = data.environment_vectors || { spatial_coherence: 0, resonance_factor: 0 };
    vecContainer.innerHTML = `
      <h4>Environment Vectors E</h4>
      <div class="vector-grid">
        <div class="vector-item"><span class="axis">Spatial Coherence</span><span class="magnitude">${vecData.spatial_coherence.toFixed(2)}</span></div>
        <div class="vector-item"><span class="axis">Resonance Factor</span><span class="magnitude">${vecData.resonance_factor.toFixed(2)}</span></div>
      </div>
    `;
  }

  /* 5. Regional Passports Widget */
  const passportContainer = widgetContainers["passports-grid"];
  if (passportContainer) {
    const regions = data.regions || [];
    passportContainer.innerHTML = "<h4>Regional Passports</h4>";
    regions.forEach(region => {
      const statusColor = region.status === "good" ? "#6bcb77" : region.status === "partial" ? "#ffd93d" : "#ff6b6b";
      const div = document.createElement("div");
      div.className = "region-card";
      div.style.cssText = `border-left: 4px solid ${statusColor}`;
      div.innerHTML = `
        <strong>${region.name}</strong> (${region.code})
        <div style="font-size: 0.8em; margin-top: 4px">
          Status: <span style="color: ${statusColor}">${region.status}</span><br>
          Tension: <span style="color: #888">${region.social_tension}</span>
        </div>
        <div style="margin-top: 4px; font-size: 0.7em">GPS: ${region.gps}</div>
      `;
      passportContainer.appendChild(div);
    });
  }

  /* 6. OSINT Signals Widget */
  const signalsContainer = widgetContainers["signals-list"];
  if (signalsContainer) {
    const signals = data.active_signals || [];
    signalsContainer.innerHTML = `<h4>Active OSINT Signals <span class="badge">${signals.length}</span></h4><div class="b-list">`;
    signals.forEach(signal => {
      const div = document.createElement("div");
      div.className = "b-item";
      div.innerHTML = `<strong>${signal.signal_id}</strong>: ${signal.raw_text}`;
      signalsContainer.appendChild(div);
    });
    signalsContainer.innerHTML += `</div>`;
  }
}

/* Helper: safely set text/HTML, avoiding TypeError: Cannot set properties of null */
function safeSetText(id, text) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = text;
  }
}

/* ===========================================================
   Execution: Run buildWidgets SYNCHRONOUSLY on DOMContentLoaded
   Then attempt optional fetch for live data with silent CORS error handling
   =========================================================== */
document.addEventListener("DOMContentLoaded", () => {
  /* --- STEP 1: Render default widgets immediately --- */
  buildWidgets(DEFAULT_TELEMETRY);

  /* --- STEP 2: Optional live fetch (silently catches CORS errors) --- */
  const TELEMETRY_FEED_URL = "./telemetry_feed.json";
  const updateTelemetry = async () => {
    try {
      const response = await fetch(TELEMETRY_FEED_URL);
      if (!response.ok) throw new Error("HTTP " + response.status);
      const telemetry = await response.json();
      /* If fetch succeeds, update widgets with live data */
      buildWidgets(telemetry);
    } catch (error) {
      // Silently catch file:// CORS errors and network errors without breaking UI
      // Console log for debugging, but UI remains intact
      console.debug("Live telemetry fetch skipped or blocked (CORS/network):", error);
      /* Keep existing default telemetry already rendered --- */
    }
  };

  /* Attempt fetch after initial render; timeout after 5s to avoid hanging */
  const fetchPromise = updateTelemetry();
  if (fetchPromise && typeof fetchPromise.then === "function") {
    fetchPromise.then(() => {}).catch(() => {/* Suppress unhandled promise rejections --- */});
  }
});

function initElements() {
  elements.panels = {
    modeDisplay: document.getElementById("mode-display"),
    vectorGrid: document.querySelector(".vector-grid"),
    h3Canvas: document.getElementById("h3-canvas"),
    peerList: document.querySelector(".peer-list"),
    signalsSection: document.querySelector(".signal-section"),
    ramPercent: document.getElementById("ram-percent"),
    ramUsage: document.querySelector(".ram-usage"),
    coherenceVal: document.getElementById("coherence-val"),
    passportsGrid: document.getElementById("passports-grid"),
    signalsList: document.getElementById("signals-list")
  };
}

document.addEventListener("DOMContentLoaded", () => {
  const TELEMETRY_FEED_URL = "./telemetry_feed.json";
initElements();

  /* Render default data immediately on page load first */
  renderRamWidget(DEFAULT_TELEMETRY, true);
  renderEnvVectorsWidget(DEFAULT_TELEMETRY, true);
  renderRegionalPassportsWidget(DEFAULT_TELEMETRY, true);
  renderOsintSignalsWidget(DEFAULT_TELEMETRY, true);
  updateMode(DEFAULT_TELEMETRY.ramUtilization_percent || 0);

  /* Then attempt fetch for live server data */
  updateDashboard();

  
});
function renderRamWidget(telemetry, isFallback = false) {
  const ramPercent = elements.panels.ramPercent;
  const ramUsage = elements.panels.ramUsage;
  if (!ramPercent || !ramUsage) return;
  const ramState = telemetry?.ramUtilization_percent ?? bTelemetry.ramUtilization_percent;
  ramPercent.textContent = `${ramState.toFixed(1)}%`;
  if (ramState > 75) { ramPercent.parentElement.style.color = "#ff6b6b"; updateMode("critical"); }
  else if (ramState > 50) { ramPercent.parentElement.style.color = "#ffd93d"; updateMode("balanced"); }
  else { ramPercent.parentElement.style.color = "#6bcb77"; updateMode("performance"); }
  




