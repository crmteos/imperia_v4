/** Imperia v4: Interactive P2P Topology Simulator Engine */
class P2PTopologySimulator {
  constructor() {
    this.nodes = [
      { id: "node-101", name: "Kyiv-Brahman-01", qFactor: 0.95, role: "Brahman", ramMb: 16384, status: "Active" },
      { id: "node-102", name: "Lviv-Brahman-02", qFactor: 0.94, role: "Brahman", ramMb: 16384, status: "Active" },
      { id: "node-103", name: "Odesa-Kshatriya-01", qFactor: 0.92, role: "Kshatriya", ramMb: 8192, status: "Active" },
      { id: "node-104", name: "Kharkiv-Vaishya-01", qFactor: 0.91, role: "Vaishya", ramMb: 4096, status: "Active" },
      { id: "node-105", name: "Dnipro-Shudra-01", qFactor: 0.90, role: "Shudra", ramMb: 2048, status: "Active" }
    ];
    this.swarmLoad = 0.0; // 0% initial load - fully calibrated
    this.breathingMode = 'cuboctahedron'; // cuboctahedron (Янь/Out-Wave) or tetrahedron (Інь/In-Wave)
    this.qTarget = 0.94; // Minimum Q-factor threshold
  }

  // Q-динаміка: dQ_node/dt = alpha * (Q_target - Q_node) - beta * Jitter + gamma * Feedback
  updateQFactor(nodeId, alpha = 0.05, beta = 0.01, gamma = 0.02) {
    const node = this.nodes.find(n => n.id === nodeId);
    if (!node) return;
    
    const jitter = Math.random() * 0.02; // Random jitter in [0, 0.02)
    const feedback = this.computeFeedback();
    const dQ = alpha * (this.qTarget - node.qFactor) - beta * jitter + gamma * feedback;
    
    node.qFactor = Math.min(0.99, Math.max(this.qTarget, node.qFactor + dQ));
    this.recalculateTopology();
  }

  computeFeedback() {
    const activeQs = this.nodes.filter(n => n.status === "Active").map(n => n.qFactor);
    if (activeQs.length === 0) return 0;
    const meanQ = activeQs.reduce((a, b) => a + b) / activeQs.length;
    // Feedback pushes toward mean coherence
    return (0.95 - meanQ) * 0.1;
  }

  // Динаміка Джиттербагу Фуллера: перемикання між Cuboctahedron та Tetrahedron
  setBreathingMode(mode) {
    const validModes = ['cuboctahedron', 'tetrahedron'];
    if (!validModes.includes(mode)) {
      console.error(`Invalid breathing mode: ${mode}. Must be one of ${validModes}`);
      return;
    }
    this.breathingMode = mode;
    const statusEl = document.getElementById('breathing-mode');
    if (statusEl) statusEl.innerText = mode;
    this.recalculateTopology();
  }

  // Регіональна матриця вузлів з точними Q-факторами з Direktvи
  // Kyiv: Q = 0.95 (Brahman Node, Swarm Master)
  // Lviv: Q = 0.94 (Brahman Node, Failover Backup)
  // Odesa: Q = 0.92 (Kshatriya Node, Execution Gateway)
  // Kharkiv: Q = 0.91 (Vaishya Node, DAG Data Pool)
  // Dnipro: Q = 0.90 (Shudra Node, Edge Sensor Hub)
  getRegionQ(nodeName) {
    const qMap = {
      'Kyiv': 0.95,
      'Lviv': 0.94,
      'Odesa': 0.92,
      'Kharkiv': 0.91,
      'Dnipro': 0.90
    };
    return qMap[nodeName] || 0.90;
  }

  recalculateTopology() {
    const activeNodes = this.nodes.filter(n => n.status === "Active");
    const meanQ = activeNodes.reduce((acc, n) => acc + n.qFactor, 0) / (activeNodes.length || 1);
    const coherence = Math.max(0.1, meanQ * (1 - this.swarmLoad * 0.15));
    
    // Render updates to DOM if elements exist
    const nodesCountEl = document.getElementById('p2p-nodes');
    if (nodesCountEl) nodesCountEl.innerText = `${activeNodes.length} Active Nodes`;
    const cohEl = document.getElementById('coherence-val');
    if (cohEl) cohEl.innerText = coherence.toFixed(2);
    const p2pListEl = document.getElementById('p2p-nodes-list');
    if (p2pListEl) {
      p2pListEl.innerHTML = activeNodes.map(n => `
        <div class="p-2 mb-1.5 bg-gray-900 rounded border border-gray-700 flex justify-between items-center text-xs">
          <div>
            <span class="font-bold text-blue-400">${n.name}</span>
            <span class="text-gray-400 ml-2">(${n.role} | RAM: ${n.ramMb}MB)</span>
          </div>
          <div class="text-green-400 font-mono">Q: ${n.qFactor}</div>
        </div>`).join('');
    }
    
    // Update breathing status display
    const breathingEl = document.getElementById('breathing-mode');
    if (breathingEl) breathingEl.innerText = this.breathingMode;
  }
  
  // Simulate Fuller's breathing - Cuboctahedron <-> Tetrahedron transition
  breathe() {
    if (this.breathingMode === 'cuboctahedron') {
      this.setBreathingMode('tetrahedron');
      // During tetrahedron mode, Q-factor stabilizes at or above 0.95
      this.nodes.forEach(n => { if (n.status === 'Active') n.qFactor = Math.min(0.99, n.qFactor + 0.01); });
    } else {
      this.setBreathingMode('cuboctahedron');
    }
    this.recalculateTopology();
  }
}
window.p2pSim = new P2PTopologySimulator();
document.addEventListener('DOMContentLoaded', () => { 
  window.p2pSim.recalculateTopology(); 
  // Auto-breathing cycle every 10 seconds
  setInterval(() => { window.p2pSim.breathe(); }, 10000); 
});