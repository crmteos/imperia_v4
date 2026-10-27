/**
 * Imperia v4: Cognitive-Theoretical Math & Telemetry Engine
 */

/**
 * Calculate Quality Factor (Q) differential adaptation step
 * dQ/dt = alpha * (Q_target - Q_node) - beta * Jitter + gamma * Feedback
 */
function computeQNodeStep(qNode, qTarget, jitter, feedback, alpha = 0.1, beta = 0.05, gamma = 0.08) {
  const dQ = alpha * (qTarget - qNode) - beta * jitter + gamma * feedback;
  const updatedQ = Math.max(0, Math.min(1.0, qNode + dQ));
  return parseFloat(updatedQ.toFixed(4));
}

/**
 * Calculate DAG Tokenomics Reward (PoI / PoC)
 * Reward = Tokens_processed * Q_node * K_H3_density
 */
function computeDAGReward(tokensProcessed, qNode, kH3Density = 1.2) {
  const reward = tokensProcessed * qNode * kH3Density;
  return parseFloat(reward.toFixed(2));
}

/**
 * Determine Synarchy Varna Role & M-f Scale Axis
 * Based on Q-factor, NPU power, and Resource Governor state
 */
function evaluateVarnaRole(qNode, isPluggedIn = true, ramMb = 8192) {
  if (qNode >= 0.85 && isPluggedIn && ramMb >= 8192) {
    return { role: "Brahman", varna: "Collective Consciousness / Orchestrator", scaleAxis: "Meso-2 (10^6 cm)", status: "High Q Amplifier" };
  } else if (qNode >= 0.65) {
    return { role: "Kshatriya", varna: "Governance & Regional Router", scaleAxis: "Meso-1 (10^4 cm)", status: "Active Node" };
  } else if (qNode >= 0.35) {
    return { role: "Vaishya", varna: "P2P Data & Resource Exchange", scaleAxis: "Micro (10^2 cm)", status: "Data Trader" };
  } else {
    return { role: "Shudra", varna: "Physical Telemetry / Edge Sensor", scaleAxis: "Micro (10^2 cm)", status: "Low Q Saver" };
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { computeQNodeStep, computeDAGReward, evaluateVarnaRole };
}