"""P2P Transport Adapter Module"""

import time
import hashlib
import json


class TransportAdapter:
    """P2P transport adapter for edge device communication."""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.peers = {}
        self.message_buffer = []
        self.max_buffer_size = 1000
        self.connection_status = "disconnected"
        self.last_heartbeat = 0

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
        message["_id"] = hashlib.md5(
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
    print("P2P Transport Adapter Demo")
    print("=" * 40)
    adapter = TransportAdapter(node_id="node-001")
    print(f"Initial status: {adapter.get_status()}")

    print("\nConnecting to peers...")
    adapter.connect_to_peer("peer-1", "192.168.1.1:8080")
    adapter.connect_to_peer("peer-2", "192.168.1.2:8080")
    print(f"After connections: {adapter.get_status()}")

    print("\nSending messages...")
    adapter.send_message("peer-1", {"type": "heartbeat", "data": "alive"})
    adapter.send_message("peer-2", {"type": "inference_request", "model": "slm-base"})
    print(f"Buffer size: {adapter.get_status()['buffer_size']}")

    print("\nReceiving messages...")
    msg = adapter.receive_message()
    print(f"Received: {msg}")

    print("\nDisconnecting peer...")
    adapter.disconnect_peer("peer-1")
    print(f"After disconnection: {adapter.get_status()}")