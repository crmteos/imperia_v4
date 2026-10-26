"""src/p2p_transport.py - Simulated P2P transport for Phase 6 compatibility.

Provides a SimulatedP2PNode class that mimics the interface of
real_p2p_transport.AsyncP2PNode for development and testing purposes.
"""

import asyncio
import json
import logging
from collections import defaultdict
from typing import Dict, Set, Callable, Optional

logger = logging.getLogger("simulated_p2p")

GOV_CONNECTION_CAPS = {
    "CRITICAL": 2,
    "BALANCED": 10,
    "PERFORMANCE": 32,
}


class SimulatedP2PNode:
    """Simulated P2P node for development and testing.

    Mimics AsyncP2PNode interface without requiring websockets.
    Useful for unit testing edge_handoff and swarm_inference.
    """

    def __init__(self, governor=None, node_id=None):
        self.node_id = node_id or f"sim-p2p-{id(self)}"
        self.governor = governor
        self.listen_host = "0.0.0.0"
        self.listen_port = 8000
        self._server = None
        self._peers: Dict[str, dict] = {}
        self._topic_subscribers: Dict[str, Set] = defaultdict(set)
        self._connection_count = 0
        self._local_gps = None

    async def start(self, listen_host="0.0.0.0", listen_port=8000) -> None:
        self.listen_host = listen_host
        self.listen_port = listen_port
        logger.info(f"SimulatedP2PNode {self.node_id} listening on {listen_host}:{listen_port}")

    async def connect_peer(self, peer_address: str) -> bool:
        """Simulate connecting to a peer."""
        parts = peer_address.split(":")
        host = parts[0]
        port = int(parts[1]) if len(parts) > 1 else 8000
        peer_id = f"sim-peer-{host}:{port}"
        self._peers[peer_id] = {"address": peer_address, "connected": True}
        self._connection_count += 1
        logger.info(f"Simulated connection to {peer_address} (mode={self.governor.mode if self.governor else 'none'})")
        return True

    async def disconnect_peer(self, peer_id: str) -> bool:
        if peer_id in self._peers:
            self._peers.pop(peer_id)
            self._connection_count = max(0, self._connection_count - 1)
            logger.info(f"Simulated disconnection of {peer_id}")
            return True
        return False

    async def publish_to_h3_topic(self, h3_index: str, payload: dict) -> int:
        subscribers = self._topic_subscribers.get(h3_index, set())
        delivered = len(subscribers) if subscribers else 0
        logger.info(f"Simulated publish to H3 topic {h3_index}: {delivered} subscribers")
        return delivered

    async def subscribe_h3_topic(self, h3_index: str, handler_func: Callable[[dict], None]) -> None:
        logger.info(f"Simulated subscribe to H3 topic {h3_index}")
        self._topic_subscribers[h3_index]

    def get_network_telemetry(self) -> dict:
        return {
            "node_id": self.node_id,
            "mode": self.governor.mode if self.governor else "none",
            "connection_count": self._connection_count,
            "peer_count": len(self._peers),
            "topic_count": len(self._topic_subscribers),
            "local_gps": self._local_gps,
            "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        }

    async def _handle_ws(self, ws, path):
        pass

    def set_local_gps(self, lat: float, lon: float) -> None:
        self._local_gps = (lat, lon)