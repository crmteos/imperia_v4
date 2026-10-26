"""Imperia v4 Edge Handoff Module

Handles edge device handoff between nodes in the P2P swarm.
Coordinates handoff based on resource governor mode,
stateful RAM token budget, and H3 geospatial proximity.
"""

import sys
import os
import time

sys.path.insert(0, r"c:\imperia_v4\src")

from governor.resource_governor import ResourceGovernor
from context.stateful_ram import StatefulContextRAM
from p2p.transport_adapter import TransportAdapter
from geo.h3_vector import gps_to_h3_index, calculate_vector_at_resolutions


class EdgeHandoff:
    """Edge node handoff coordinator for Imperia v4 swarm."""

    def __init__(self, node_id, h3_meso_res7=None, handoff_threshold=0.3):
        self.node_id = node_id
        self.transport = TransportAdapter(node_id=node_id, h3_meso_res7=h3_meso_res7)
        self.governor = ResourceGovernor()
        self.ram = StatefulContextRAM(max_token_budget=8192)
        self.handoff_threshold = handoff_threshold
        self.potential_peers = {}
        self.handoff_history = []
        self.current_location = None

    def set_location(self, lat, lon):
        self.current_location = (lat, lon)
        self.h3_indices = calculate_vector_at_resolutions(lat, lon, [7])

    def update_peers(self, peer_ids, peer_locations):
        self.potential_peers = {}
        for peer_id, (plat, plon) in zip(peer_ids, peer_locations):
            peer_h3 = calculate_vector_at_resolutions(plat, plon, [7])
            current_h3 = self.h3_indices["res_7"]
            peer_h3_res7 = peer_h3["res_7"]
            distance = abs(hash(current_h3) - hash(peer_h3_res7)) % 1000 / 1000.0
            if distance < self.handoff_threshold:
                self.potential_peers[peer_id] = {
                    "location": (plat, plon),
                    "h3_index": peer_h3_res7,
                    "distance": distance,
                }

    def should_handoff(self):
        mode = self.governor.mode
        ram_status = self.ram.get_status()
        if mode == "CRITICAL" and ram_status["total_tokens"] < ram_status["max_token_budget"] * 0.2:
            return True, "CRITICAL low tokens"
        if mode == "PERFORMANCE" and self.potential_peers:
            best_peer = min(self.potential_peers.keys(),
                          key=lambda p: self.potential_peers[p]["distance"])
            return True, f"PERFORMANCE better peer: {best_peer}"
        if mode == "BALANCED" and ram_status["total_tokens"] < ram_status["max_token_budget"] * 0.5:
            return True, "BALANCED moderate token usage"
        return False, f"{mode} mode no handoff needed"

    def initiate_handoff(self, target_peer):
        if target_peer not in self.potential_peers:
            return False, "Target peer not in potential peers"
        handoff_tokens = self.ram.allocate_tokens("state", 100)
        handoff_data = {
            "type": "handoff_request",
            "from_node": self.node_id,
            "to_node": target_peer,
            "h3_index": self.h3_indices["res_7"],
            "tokens_allocated": handoff_tokens,
            "timestamp": int(time.time()),
        }
        success = self.transport.send_message(target_peer, handoff_data)
        if success:
            self.handoff_history.append({
                "target": target_peer,
                "timestamp": int(time.time()),
                "status": "initiated",
                "tokens": handoff_tokens,
            })
            return True, "Handoff request sent"
        return False, "Failed to send handoff request"

    def process_handoff_response(self, peer_id, response_data):
        if response_data.get("status") == "accepted":
            self.handoff_history[-1]["status"] = "accepted"
            self.handoff_history[-1]["peer_resources"] = response_data.get("resources", {})
            return True, "Handoff accepted"
        elif response_data.get("status") == "rejected":
            self.handoff_history[-1]["status"] = "rejected"
            return False, "Handoff rejected"
        return False, "Invalid handoff response"

    def get_handoff_status(self):
        return {
            "node_id": self.node_id,
            "governor_mode": self.governor.mode,
            "current_location": self.current_location,
            "potential_peers": len(self.potential_peers),
            "handoff_history": self.handoff_history,
            "ram_status": self.ram.get_status(),
        }
if __name__ == "__main__":
    print("Imperia v4 Edge Handoff Example")
    print("=" * 40)

    handoff = EdgeHandoff(node_id="edge-node-02")
    handoff.set_location(34.0522, -118.2436)
    print(f"Location set: {handoff.current_location}")

    peer_ids = ["edge-node-01", "edge-node-03", "edge-node-04"]
    peer_locations = [
        (34.0530, -118.2440),
        (37.7749, -122.4194),
        (40.7128, -74.0060),
    ]
    handoff.update_peers(peer_ids, peer_locations)
    print(f"Peers updated: {len(handoff.potential_peers)} potential handoff peers")

    should, reason = handoff.should_handoff()
    print(f"Should handoff: {should} - {reason}")

    if should:
        target = list(handoff.potential_peers.keys())[0]
        success, msg = handoff.initiate_handoff(target)
        print(f"Handoff {success}: {msg}")

        if success:
            response = {"status": "accepted", "resources": {"tokens": 500, "bandwidth": "10Mbps"}}
            success, msg = handoff.process_handoff_response(list(handoff.potential_peers.keys())[0], response)
            print(f"Handoff response: {success} - {msg}")

    status = handoff.get_handoff_status()
    print(f"\nHandoff Status:")
    print(f"  Governor mode: {status['governor_mode']}")
    print(f"  Potential peers: {status['potential_peers']}")
    print(f"  Handoff history: {len(status['handoff_history'])} events")
    print(f"  RAM status: {status['ram_status']}")

    print("\nExample complete")