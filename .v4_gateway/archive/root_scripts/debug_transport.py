import sys
sys.path.insert(0, r"c:\imperia_v4\src")

import sys
sys.path.insert(0, r"c:\imperia_v4\src")

from p2p.transport_adapter_fresh import TransportAdapter

a = TransportAdapter(node_id='node-001')
print('node_id:', a.node_id)
print('status before connect:', a.get_status()['connection_status'])
result = a.connect_to_peer('peer-1', '192.168.1.1:8080')
print('connect_to_peer result:', result)
print('status after connect:', a.get_status()['connection_status'])
print('peers:', a.peers)
if result:
    a.send_message('peer-1', {'type': 'heartbeat'})
    print('after send status:', a.get_status()['connection_status'])
    msg = a.receive_message()
    print('msg:', msg)