if __name__ == "__main__":
    print("Stateful Context RAM Manager")
    print("=" * 40)
    ram = StatefulContextRAM(max_token_budget=8192)
    print(f"Max token budget: {ram.max_token_budget}")
    print(f"Initial status: {ram.get_status()}")

    print("\nUpdating vector E...")
    ram.update_vector_E(
        E_geo="8a1b2c3d4e5f67890",
        E_resource=0.75,
        E_coherence=0.88,
        E_temporal=int(time.time())
    )
    print(f"Status after vector update: {ram.get_status()}")

    print("\nAdding items to ephemeral queue...")
    for i in range(5):
        success = ram.add_to_ephemeral({
            "sensor_id": f"sensor_{i}",
            "reading": 20.0 + i,
            "timestamp": int(time.time())
        })
        print(f"  Added sensor_{i}: {'Success' if success else 'Failed'}")

    print(f"Status after additions: {ram.get_status()}")

    print("\nRetrieving from FIFO queue:")
    for i in range(5):
        result = ram.get_ephemeral_oldest()
        print(f"  Retrieved: {result['data']}")

    print(f"Status after retrieval: {ram.get_status()}")
    """Context window structure as Stateful RAM with 8192 token budget."""

    def __init__(self, max_token_budget: int = 8192):
        self.max_token_budget = max_token_budget
        self.total_tokens = 0

        self.invariants_block = {
            "max_token_budget": max_token_budget,
            "framework_version": "4.0.0",
            "architecture_paradigm": "Stateful Context Engineering & P2P Edge Swarm",
            "anthropomorphism_level": 0,
            "source_of_truth": "v2.0 Master Framework"
        }
        self.invariants_token_count = 0

        self.state_block = {
            "vector_E": {
                "E_geo": None,
                "E_resource": 0.0,
                "E_coherence": 0.0,
                "E_temporal": None
            },
            "local_node_state": {
                "node_id": None,
                "last_update": None,
                "connection_status": "disconnected"
            }
        }
        self.state_tokens = 0

        self.ephemeral_queue = deque(maxlen=max_token_budget // 100)
        self.ephemeral_tokens = 0

    def allocate_tokens(self, block: str, token_count: int) -> bool:
        if token_count <= 0:
            return False
        available = self._get_available_tokens(block)
        if token_count > available:
            return False
        if block == "invariants":
            self.invariants_token_count = min(
                self.invariants_token_count + token_count,
                self.max_token_budget
            )
            return True
        elif block == "state":
            self.state_tokens = min(
                self.state_tokens + token_count,
                self.max_token_budget
            )
            self.total_tokens = self.state_tokens + self.ephemeral_tokens
            return True
        elif block == "ephemeral":
            self.ephemeral_tokens = min(
                self.ephemeral_tokens + token_count,
                self.max_token_budget
            )
            self.total_tokens = self.state_tokens + self.ephemeral_tokens
            self.ephemeral_queue.append({
                "tokens": token_count,
                "timestamp": time.time(),
                "data": None
            })
            return True
        return False

    def _get_available_tokens(self, block: str) -> int:
        if block == "invariants":
            return self.max_token_budget - self.invariants_token_count
        elif block == "state":
            return self.max_token_budget - self.state_tokens
        elif block == "ephemeral":
            return self.max_token_budget - self.ephemeral_tokens
        return 0

    def update_vector_E(self, E_geo: str = None, E_resource: float = None,
                        E_coherence: float = None, E_temporal: int = None) -> dict:
        vector_E = self.state_block["vector_E"]
        if E_geo is not None:
            vector_E["E_geo"] = E_geo
        if E_resource is not None:
            vector_E["E_resource"] = max(0.0, min(1.0, E_resource))
        if E_coherence is not None:
            vector_E["E_coherence"] = E_coherence
        if E_temporal is not None:
            vector_E["E_temporal"] = E_temporal
        self.state_block["local_node_state"]["last_update"] = time.time()
        return vector_E

    def add_to_ephemeral(self, data: dict) -> bool:
        if self.total_tokens >= self.max_token_budget:
            return False
        estimated_tokens = len(str(data)) // 100 + 1
        estimated_tokens = max(estimated_tokens, 1)
        if self.allocate_tokens("ephemeral", estimated_tokens):
            return True
        return False

    def get_ephemeral_next(self) -> dict:
        if self.ephemeral_queue:
            return {
                "data": self.ephemeral_queue[0],
                "queue_size": len(self.ephemeral_queue),
                "total_tokens": self.total_tokens
            }
        return {
            "data": None,
            "queue_size": 0,
            "total_tokens": self.total_tokens
        }

    def get_ephemeral_oldest(self) -> dict:
        if self.ephemeral_queue:
            data = self.ephemeral_queue.popleft()
            self.ephemeral_tokens = max(0, self.ephemeral_tokens - 1)
            self.total_tokens = self.state_tokens + self.ephemeral_tokens
            return {
                "data": data,
                "queue_size": len(self.ephemeral_queue),
                "total_tokens": self.total_tokens
            }
        return {
            "data": None,
            "queue_size": 0,
            "total_tokens": self.total_tokens
        }

    def get_status(self) -> dict:
        return {
            "max_token_budget": self.max_token_budget,
            "total_tokens": self.total_tokens,
            "state_tokens": self.state_tokens,
            "ephemeral_tokens": self.ephemeral_tokens,
            "invariants_tokens": self.invariants_token_count,
            "is_at_capacity": self.total_tokens >= self.max_token_budget
        }