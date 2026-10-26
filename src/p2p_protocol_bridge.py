"""src/p2p_protocol_bridge.py - UnifiedTransportAdapter bridging simulated and real P2P transport."""

import asyncio
import json
import logging
from typing import Dict, Optional, Any

logger = logging.getLogger("p2p_protocol_bridge")


class UnifiedTransportAdapter:
    """Bridge unifying simulated p2p_transport.py and real_p2p_transport.py seamlessly
    for edge_handoff and swarm_inference.

    Supports both simulated and real network transport modes. edge_handoff.py can
    serialize context snapshots and transmit them over active WebSocket/socket sessions.
    """

    def __init__(self, use_real_transport: bool = False, governor=None):
        self.use_real_transport = use_real_transport
        self.governor = governor
        self._local_peers: Dict[str, Any] = {}
        self._quantum_callbacks: list = []

        if use_real_transport:
            from real_p2p_transport import AsyncP2PNode
            self.transport = AsyncP2PNode(governor=governor)
        else:
            from p2p_transport import SimulatedP2PNode
            self.transport = SimulatedP2PNode(governor=governor)

    async def broadcast_quantum(self, quantum_data: dict) -> bool:
        """Broadcast quantum data to all active peers.

        Args:
            quantum_data: Dictionary containing quantum state data to broadcast.

        Returns:
            True if broadcast was sent to at least one peer.
        """
        if not self.transport._peers:
            logger.warning("No active peers for quantum broadcast")
            return False

        msg = json.dumps({
            "type": "quantum_broadcast",
            "data": quantum_data,
            "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "sender": self.transport.node_id,
        })

        sent = 0
        for ws in list(self.transport._peers.values()):
            try:
                await ws.send(msg)
                sent += 1
            except Exception as e:
                logger.warning(f"Failed to send quantum to peer: {e}")

        logger.info(f"Broadcast quantum to {sent} peers")
        return sent > 0

    async def handshake_handoff(self, target_peer_id: str, context_snapshot: dict) -> bool:
        """Perform a handshake handoff to a target peer, transmitting context snapshot.

        Args:
            target_peer_id: Identifier of the target peer.
            context_snapshot: Serialized context snapshot to transmit.

        Returns:
            True if handoff handshake succeeded.
        """
        if target_peer_id not in self.transport._peers:
            logger.warning(f"Peer {target_peer_id} not found for handoff")
            return False

        ws = self.transport._peers[target_peer_id]
        msg = json.dumps({
            "type": "handoff_handshake",
            "target": target_peer_id,
            "context": context_snapshot,
            "timestamp": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            "sender": self.transport.node_id,
        })

        try:
            await ws.send(msg)
            logger.info(f"Handshake handoff sent to {target_peer_id}")
            return True
        except Exception as e:
            logger.error(f"Handshake handoff failed to {target_peer_id}: {e}")
            return False