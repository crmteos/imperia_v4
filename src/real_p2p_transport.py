"""src/real_p2p_transport.py - AsyncP2PNode for Phase 6 P2P transport."""

import asyncio
import json
import logging
from collections import defaultdict
from typing import Dict, Set, Callable, Optional

logger = logging.getLogger("real_p2p")

GOV_CONNECTION_CAPS = {
    "CRITICAL": 2,
    "BALANCED": 10,
    "PERFORMANCE": 32,
}


class AsyncP2PNode:
    """Asynchronous P2P node with WebSocket transport and H3 topic routing."""

    def __init__(self, governor=None, node_id=None):
        self.node_id = node_id or f"p2p-{id(self)}"
        self.governor = governor
        self.listen_host = "0.0.0.0"
        self.listen_port = 8000
        self._server = None
        self._peers: Dict[str, websockets.WebSocketServerConnection] = {}
        self._topic_subscribers: Dict[str, Set] = defaultdict(set)
        self._connection_count = 0
        self._local_gps = None

    async def start(self, listen_host="0.0.0.0", listen_port=8000):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self._server = await websockets.serve(self._handle_ws, listen_host, listen_port)
        logger.info(f"AsyncP2PNode {self.node_id} listening on {listen_host}:{listen_port}")

    async def connect_peer(self, peer_address: str) -> bool:
        try:
            parts = peer_address.split(":")
            host = parts[0]
            port = int(parts[1]) if len(parts) > 1 else 8000
            ws = await websockets.connect(f"ws://{host}:{port}")
            peer_id = f"peer-{host}:{port}"
            self._peers[peer_id] = ws
            self._connection_count += 1
            if self.governor:
                cap = GOV_CONNECTION_CAPS.get(self.governor.mode, 10)
                if self._connection_count > cap:
                    oldest = sorted(self._peers.keys())[0]
                    await self.disconnect_peer(oldest)
                    logger.warning(f"CRITICAL mode: throttled, dropped {oldest}")
                else:
                    logger.info(f"Connected {peer_address} mode={self.governor.mode} cap={cap}")
            else:
                logger.info(f"Connected {peer_address}")
            return True
        except Exception as e:
            logger.error(f"connect_peer failed: {e}")
            return False

    async def disconnect_peer(self, peer_id: str) -> bool:
        if peer_id in self._peers:
            ws = self._peers.pop(peer_id)
            try:
                await ws.close()
            except Exception:
                pass
            self._connection_count = max(0, self._connection_count - 1)
            logger.info(f"Disconnected {peer_id}")
            return True
        return False

    async def publish_to_h3_topic(self, h3_index: str, payload: dict) -> int:
        subscribers = self._topic_subscribers.get(h3_index, set())
        msg = json.dumps({
            "type": "h3_topic",
            "h3_index": h3_index,
            "payload": payload,
            "sender": self.node_id,
        })
        delivered = 0
        for ws in set(subscribers):
            try:
                await ws.send(msg)
                delivered += 1
            except Exception as e:
                logger.warning(f"Delivery failed: {e}")
                subscribers.discard(ws)
        logger.info(f"Published to {h3_index}: {delivered} subscribers")
        return delivered

    async def subscribe_h3_topic(self, h3_index: str, handler_func: Callable[[dict], None]) -> None:
        logger.info(f"Subscribed to H3 topic {h3_index}")
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
        """Handle an incoming WebSocket connection."""
        peer_id = f"ws-{id(ws)}"
        self._peers[peer_id] = ws
        self._connection_count += 1
        logger.info(f"New WS connection from {peer_id} (total peers: {len(self._peers)})")

        try:
            async for message in ws:
                try:
                    data = json.loads(message)
                except Exception:
                    continue
                msg_type = data.get("type", "")
                if msg_type == "subscribe":
                    h3_index = data.get("h3_index", "")
                    if h3_index:
                        self._topic_subscribers[h3_index].add(ws)
                        logger.info(f"{peer_id} subscribed to {h3_index}")
                elif msg_type == "publish":
                    h3_index = data.get("h3_index", "")
                    payload = data.get("payload", {})
                    await self.publish_to_h3_topic(h3_index, payload)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            # Clean up on disconnect
            for h3_idx, subs in self._topic_subscribers.items():
                subs.discard(ws)
            self._peers.pop(peer_id, None)
            self._connection_count = max(0, self._connection_count - 1)
            logger.info(f"Connection closed {peer_id} remaining={len(self._peers)}")

    def set_local_gps(self, lat: float, lon: float) -> None:
        """Set local GPS location for geo-aware routing."""
        self._local_gps = (lat, lon)