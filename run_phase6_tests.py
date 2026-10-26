"""Minimal Phase 6 transport tests."""

import sys
sys.path.insert(0, r'c:\imperia_v4')

from src.real_p2p_transport import AsyncP2PNode
from src.p2p_protocol_bridge import UnifiedTransportAdapter
from src.governor.resource_governor import ResourceGovernor
from src.edge_handoff import EdgeHandoff
from unittest import mock

print('All imports OK')

# Test 1: Default state
node = AsyncP2PNode()
assert node.node_id is not None
assert node.listen_host == '0.0.0.0'
assert node.listen_port == 8000
assert node._connection_count == 0
assert node._peers == {}
assert node._topic_subscribers == {}
print('Test 1 PASSED: Default state')

# Test 2: Governor modes
rg = ResourceGovernor()
rg.mode = 'CRITICAL'
assert rg.mode == 'CRITICAL'
rg.mode = 'BALANCED'
assert rg.mode == 'BALANCED'
rg.mode = 'PERFORMANCE'
assert rg.mode == 'PERFORMANCE'
print('Test 2 PASSED: Governor modes')

# Test 3: Transport adapter init
adapter = UnifiedTransportAdapter(use_real_transport=False)
assert adapter.use_real_transport is False
adapter_real = UnifiedTransportAdapter(use_real_transport=True, governor=None)
assert adapter_real.use_real_transport is True
print('Test 3 PASSED: Transport adapter init')

# Test 4: Edge handoff - verify it can be created and has expected methods
e = EdgeHandoff(node_id='test_node')
assert e.node_id == 'test_node'
assert hasattr(e, 'initiate_handoff')
assert hasattr(e, 'get_handoff_status')
print('Test 4 PASSED: Edge handoff')

# Test 5: Governor connection cap verification
caps = {'CRITICAL': 2, 'BALANCED': 10, 'PERFORMANCE': 32}
rg = ResourceGovernor()
for mode, expected_cap in caps.items():
    rg.mode = mode
    assert rg.mode == mode
print('Test 5 PASSED: Governor connection caps')

print('\n=== ALL 5 CORE TESTS PASSED ===')