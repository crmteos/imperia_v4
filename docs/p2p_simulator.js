/**
 * Imperia v4: Interactive P2P Topology Simulator Engine
 */
class P2PTopologySimulator {
  constructor() {
    this.nodes = [
      { id: "node-101", name: "Kyiv-Brahman-01", qFactor: 0.94, role: "Brahman", ramMb: 16384, status: "Active" },
      { id: "node-102", name: "Lviv-Kshatriya-01", qFactor: 0.88, role: "Kshatriya", ramMb: 8192, status: "Active" },
      { id: "node-103", name: "Odesa-Vaishya-01", qFactor: 0.74, role: "Vaishya", ramMb: 4096, status: "Active" },
      { id: "node-104", name: "Kharkiv-Shudra-01", qFactor: 0.68, role: "Shudra", ramMb: 2048, status: "Active" },
      { id: "node-105", name: "Dnipro-Kshatriya-02", qFactor: 0.81, role: "Kshatriya", ramMb: 8192, status: "Active" }
    ];
    this.swarmLoad = 0.42; // 42% initial load
  }

  addNode(role = "Brahman") {
    const newId = `node-${Date.now().toString().slice(-4)}`;
    const isBrahman = role === "Brahman";
    const newNode = {
      id: newId,
      name: `Swarm-${role}-${this.nodes.length + 1}`,
      qFactor: isBrahman ? 0.91 : 0.45,
      role: role,
      ramMb: isBrahman ? 16384 : 2048,
      status: "Active"
    };
    this.nodes.push(newNode);
    this.recalculateTopology();
    return newNode;
  }

  removeNode() {
    if (this.nodes.length > 2) {
      const removed = this.nodes.pop();
      this.recalculateTopology();
      return removed;
    }
    return null;
  }

  triggerInferenceSpike() {
    this.swarmLoad = Math.min(0.98, parseFloat((this.swarmLoad + 0.25).toFixed(2)));
    this.recalculateTopology();
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
        </div>
      `).join('');
    }
  }
}
window.p2pSim = new P2PTopologySimulator();
document.addEventListener('DOMContentLoaded', () => { window.p2pSim.recalculateTopology(); });