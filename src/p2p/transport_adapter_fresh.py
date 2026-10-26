"""src/p2p/transport_adapter.py - P2P Transport Adapter"""

import json
import time


class TransportAdapter:
    """P2P transport adapter for edge device communication."""

    def __init__(self, node_id: str = None, h3_meso_res7: str = None):
        """Initialize the transport adapter.

        Args:
            node_id: Identifier for the edge node
            h3_meso_res7: H3 meso resolution 7 index used to construct topic
        """
        self.node_id = node_id
        self.h3_meso_res7 = h3_meso_res7
        self.peers = {}
        self.message_buffer = []
        self.max_buffer_size = 1000
        self.connection_status = "disconnected"
        self.last_heartbeat = 0
        if h3_meso_res7:
            self.topic = f"/v4/h3/{h3_meso_res7}"
        else:
            self.topic = None

    def connect_to_peer(self, peer_id: str, address: str) -> bool:
        """Establish a P2P connection with a peer node."""
        try:
            self.peers[peer_id] = {
                "address": address,
                "connected_at": time.time(),
                "last_seen": time.time(),
                "status": "connected"
            }
            self.connection_status = "connected"
            return True
        except Exception:
            return False

    def disconnect_peer(self, peer_id: str) -> bool:
        """Disconnect from a peer node."""
        if peer_id in self.peers:
            self.peers[peer_id]["status"] = "disconnected"
            del self.peers[peer_id]
            if not self.peers:
                self.connection_status = "disconnected"
            return True
        return False

    def send_message(self, peer_id: str, message: dict) -> bool:
        """Send a message to a peer via P2P."""
        if peer_id not in self.peers or self.peers[peer_id]["status"] != "connected":
            return False
        message["_id"] = __import__('hashlib').md5(
            f"{self.node_id}:{peer_id}:{time.time()}".encode()
        ).hexdigest()[:16]
        message["_timestamp"] = time.time()
        self.message_buffer.append(message)
        if len(self.message_buffer) > self.max_buffer_size:
            self.message_buffer.pop(0)
        return True

    def receive_message(self) -> dict:
        """Receive the next message from the buffer."""
        if self.message_buffer:
            return self.message_buffer.pop(0)
        return {}

    def update_heartbeat(self) -> None:
        """Update heartbeat timestamp."""
        self.last_heartbeat = time.time()

    def get_status(self) -> dict:
        """Get current transport adapter status."""
        active_peers = sum(
            1 for p in self.peers.values() if p["status"] == "connected"
        )
        return {
            "node_id": self.node_id,
            "connection_status": self.connection_status,
            "active_peers": active_peers,
            "total_peers": len(self.peers),
            "buffer_size": len(self.message_buffer),
            "last_heartbeat": self.last_heartbeat
        }


if __name__ == "__main__":
    print("P2P Transport Adapter Example")
    print("=" * 40)

    # Example with an H3 meso index
    adapter = TransportAdapter(h3_meso_res7="8a1b2c3d4e5f67890")

    print(f"Topic: {adapter.topic}")
    print(f"Pattern: /v4/h3/{{h3_meso_res7}}")

    # Subscribe
    result = adapter.subscribe() if hasattr(adapter, 'subscribe') else "subscribe not implemented"
    print(f"Subscribe: {result}")

    # Publish a message
    publish_result = adapter.publish({"type": "h3_quanta", "data": "test_message", "source": "node_core"})
    print(f"Publish: {publish_result}")

    # Get status
    status = adapter.get_status()
    print(f"Status: {status}")

    # Unsubscribe
    if hasattr(adapter, 'unsubscribe'):
        unsubscribe_result = adapter.unsubscribe()
        print(f"Unsubscribe: {unsubscribe_result}")

    print("Example complete")