/// Imperia v4: Sl8 (Slate Network) Sovereign Gateway & Social Tension Sensor

class SL8Gateway {
  constructor() {
    this.adapterVersion = "1.0.0-sl8-adapter";
    this.apiEndpoint = null;
    this.targetToken = "SSLX";
    this.tenantId = "kassator";
    this.streamListeners = [];
    this.isBroadcasting = false;
  }

  /** Calculate 4D Social Tension Index (E_soc) from Sl8 post stream */
  calculateEsoc(sentimentNoise = 0.3, anomalousVolume = 0.2, regionalDisparity = 0.1) {
    const rawEsoc = (sentimentNoise * 0.4) + (anomalousVolume * 0.35) + (regionalDisparity * 0.25);
    return parseFloat(Math.min(1.0, Math.max(0.0, rawEsoc)).toFixed(3));
  }

  /** Map Sl8 post to H3 Res 7 Spatial Cell */
  mapPostToH3(postData) {
    return {
      postId: postData.id || `sl8-${Date.now()}`,
      h3Index: postData.h3Index || "872b101ffffff",
      authorId: postData.authorId || "anon_author",
      contentQuality: postData.qualityScore || 0.85,
      timestamp: new Date().toISOString()
    };
  }

  /** TELEMETRY_STREAM: Broadcast telemetry event between kassator.html and index.html */
  broadcastTelemetryStream(payload) {
    const event = {
      type: 'TELEMETRY_STREAM',
      tenantId: this.tenantId,
      timestamp: new Date().toISOString(),
      source: 'sl8_gateway.js',
      payload: payload || {}
    };
    this.notifyStreamListeners(event);
    try {
      localStorage.setItem('imperia_telemetry_stream', JSON.stringify(event));
    } catch(e) {}
    return event;
  }

  /** Register a listener for TELEMETRY_STREAM events */
  onTelemetryStream(callback) {
    this.streamListeners.push(callback);
    return () => {
      this.streamListeners = this.streamListeners.filter(cb => cb !== callback);
    };
  }

  /** Notify all stream listeners */
  notifyStreamListeners(event) {
    this.streamListeners.forEach(cb => {
      try { cb(event); } catch(e) { console.error('Stream listener error:', e); }
    });
  }

  /** Start periodic telemetry broadcasting */
  startBroadcasting(intervalMs = 10000) {
    if (this.isBroadcasting) return;
    this.isBroadcasting = true;
    this.broadcastInterval = setInterval(() => {
      this.broadcastTelemetryStream({
        qFactor: Math.round((0.94 + (Math.random() - 0.5) * 0.1) * 100) / 100,
        load: ['light','moderate','heavy'][Math.floor(Math.random() * 3)],
        nodesOnline: 6,
        totalNodes: 6
      });
    }, intervalMs);
  }

  /** Stop broadcasting */
  stopBroadcasting() {
    if (this.broadcastInterval) {
      clearInterval(this.broadcastInterval);
      this.broadcastInterval = null;
    }
    this.isBroadcasting = false;
  }
}

if (typeof window !== 'undefined') {
  window.sl8Gateway = new SL8Gateway();
  window.sl8Gateway.startBroadcasting();
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SL8Gateway;
}