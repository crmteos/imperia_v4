"""Imperia v4 Swarm Inference Module

Handles distributed inference across the P2P swarm of edge devices.
Coordinates inference using resource governor mode awareness,
H3 geospatial indexing, and stateful RAM for token budget management.
"""

import sys
import os
import time
import json

sys.path.insert(0, r"c:\imperia_v4\src")

from geo.h3_vector import gps_to_h3_index, calculate_environment_vector, calculate_vector_at_resolutions
from governor.resource_governor import ResourceGovernor
from context.stateful_ram import StatefulContextRAM
from p2p.transport_adapter import TransportAdapter


class SwarmInference:
    """Distributed inference coordinator for Imperia v4 edge swarm."""

    def __init__(self, node_id, h3_meso_res7=None, max_token_budget=8192):
        self.node_id = node_id
        self.transport = TransportAdapter(node_id=node_id, h3_meso_res7=h3_meso_res7)
        self.governor = ResourceGovernor()
        self.ram = StatefulContextRAM(max_token_budget=max_token_budget)
        self.peers = {}
        self.inference_queue = []
        self.running = False

    def connect_peer(self, peer_id, address):
        """Establish a connection to a peer node."""
        if self.transport.connect_to_peer(peer_id, address):
            self.peers[peer_id] = {"connected_at": time.time(), "last_seen": time.time()}
            return True
        return False

    def update_inference_context(self, lat, lon):
        """Update inference context with GPS location."""
        env_vec = calculate_environment_vector(lat, lon)
        h3_indices = calculate_vector_at_resolutions(lat, lon, [7, 9])
        self.ram.update_vector_E(
            E_geo=h3_indices["res_7"],
            E_resource=env_vec["E_resource"]["value"],
            E_coherence=env_vec["E_coherence"]["value"],
            E_temporal=int(time.time())
        )
        self.governor.update_metrics(
            battery_pct=self._get_battery_level(),
            temperature_celsius=self._get_temperature()
        )
        return {"environment": env_vec, "h3_indices": h3_indices}

    def _get_battery_level(self):
        return 80

    def _get_temperature(self):
        return 35.0

    def submit_inference_task(self, task_id, data, source_peer=None):
        """Submit an inference task to the swarm."""
        mode = self.governor.mode
        token_count = self.ram.allocate_tokens("state", len(data) // 4)
        task = {
            "id": task_id,
            "data": data,
            "mode": mode,
            "tokens_allocated": token_count,
            "created_at": int(time.time()),
            "source": self.node_id
        }
        self.inference_queue.append(task)
        return task

    def broadcast_to_swarm(self, message):
        """Broadcast a message to all connected peers."""
        if not self.peers:
            return False
        for peer_id in list(self.peers.keys()):
            success = self.transport.send_message(peer_id, message)
            if not success:
                self.transport.disconnect_peer(peer_id)
                self.peers.pop(peer_id, None)
        return True

    def process_inference_cycle(self):
        """Process one inference cycle across the swarm."""
        if not self.running or not self.inference_queue:
            return []
        results = []
        mode = self.governor.mode
        while self.inference_queue:
            task = self.inference_queue.pop(0)
            if mode == "CRITICAL":
                self.ram.allocate_tokens("ephemeral", 5)
                results.append({"task_id": task["id"], "mode": "CRITICAL", "result": "conservative_inference", "tokens_used": 5})
            elif mode == "BALANCED":
                moderate_tokens = self.ram.allocate_tokens("state", 25)
                results.append({"task_id": task["id"], "mode": "BALANCED", "result": "balanced_inference", "tokens_used": moderate_tokens})
            else:
                tokens = self.ram.allocate_tokens("state", 100)
                self.ram.update_vector_E(
                    E_geo=task.get("geo_index", "unknown"),
                    E_resource=0.8,
                    E_coherence=0.9,
                    E_temporal=int(time.time())
                )
                results.append({"task_id": task["id"], "mode": "PERFORMANCE", "result": "full_inference", "tokens_used": tokens})
        return results

    def get_swarm_status(self):
        """Get current swarm status report."""
        return {
            "node_id": self.node_id,
            "governor_mode": self.governor.mode,
            "active_peers": self.transport.get_status()["active_peers"],
            "token_budget": self.ram.get_status(),
            "inference_queue_size": len(self.inference_queue),
        }