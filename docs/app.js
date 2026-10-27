document.addEventListener('DOMContentLoaded', () => {
  const DEFAULT_TELEMETRY = {
    system: { ram: "42%", nodes: 12, coherence: 0.94 },
    vectors: { spatial: 0.94, resonance: 0.88 },
    regions: [
      { name: "Київ Central", code: "101", status: "Active", tension: "Low", gps: "50.4501, 30.5234" },
      { name: "Львів West", code: "102", status: "Active", tension: "Low", gps: "49.8397, 24.0297" },
      { name: "Одеса South", code: "103", status: "Active", tension: "Medium", gps: "46.4825, 30.7233" },
      { name: "Харків East", code: "104", status: "Active", tension: "Medium", gps: "49.9935, 36.2304" },
      { name: "Дніпро Center", code: "105", status: "Active", tension: "Low", gps: "48.4647, 35.0462" }
    ],
    signals: [
      { timestamp: "2026-10-26 22:18:07 UTC", region: "Kyiv Central", text: "Geopolitical OSINT signal ingested for TERR_UA_KYIV_CENTRAL" },
      { timestamp: "2026-10-26 22:25:09 UTC", region: "Kyiv Central", text: "Broadcast delivered to Imperial Chancery Telegram Channel" },
      { timestamp: "2026-10-26 22:25:39 UTC", region: "Lviv West", text: "Resonance vector E adjusted for Lviv Hub" }
    ]
  };

  function renderDashboard(data) {
    const ramEl = document.getElementById('ram-usage');
    if (ramEl) ramEl.innerHTML = '<div class="w-full bg-gray-700 h-2 rounded"><div class="bg-blue-500 h-2 rounded" style="width: ' + data.system.ram + '"></div></div><span class="text-xs text-blue-400 mt-1 block">' + data.system.ram + ' Utilization</span>';

    const nodesEl = document.getElementById('p2p-nodes');
    if (nodesEl) nodesEl.innerText = data.system.nodes + ' Active Nodes';

    const cohEl = document.getElementById('coherence-val');
    if (cohEl) cohEl.innerText = data.system.coherence;

    const vecEl = document.getElementById('vectors-container');
    if (vecEl) {
      vecEl.innerHTML = '<div class="mb-2"><div class="flex justify-between text-xs"><span>Spatial Coherence</span><span>' + data.vectors.spatial + '</span></div><div class="w-full bg-gray-700 h-1.5 rounded"><div class="bg-green-500 h-1.5 rounded" style="width: ' + data.vectors.spatial * 100 + '%"></div></div></div>' + '<div><div class="flex justify-between text-xs"><span>Resonance</span><span>' + data.vectors.resonance + '</span></div><div class="w-full bg-gray-700 h-1.5 rounded"><div class="bg-purple-500 h-1.5 rounded" style="width: ' + data.vectors.resonance * 100 + '%"></div></div></div>';
    }

    const regEl = document.getElementById('passports-grid');
    if (regEl) {
      regEl.innerHTML = data.regions.map(r => '<div class="p-3 bg-gray-800 rounded border border-gray-700"><div class="flex justify-between items-center mb-1"><span class="font-bold text-sm text-white">' + r.name + '</span><span class="text-xs px-2 py-0.5 bg-green-900 text-green-300 rounded">' + r.status + '</span></div><div class="text-xs text-gray-400">Code: ' + r.code + ' | GPS: ' + r.gps + '</div><div class="text-xs text-yellow-400 mt-1">Tension: ' + r.tension + '</div></div>').join('');
    }

    const sigEl = document.getElementById('signals-list');
    if (sigEl) {
      sigEl.innerHTML = data.signals.map(s => '<div class="p-2 mb-2 bg-gray-900 rounded border-l-2 border-blue-500 text-xs"><div class="text-gray-500">' + s.timestamp + ' [' + s.region + ']</div><div class="text-gray-200 mt-0.5">' + s.text + '</div></div>').join('');
    }
  }

  renderDashboard(DEFAULT_TELEMETRY);
fetch('./telemetry_feed.json') .then(r => r.json()) .then(data => renderDashboard(data)) .catch(e => console.log('Using default telemetry:', e));
