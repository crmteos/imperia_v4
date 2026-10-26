from kancelyariya_facade import (
    vector_to_ui_signal,
    format_ram_telemetry,
    format_p2p_topology,
    export_telemetry,
    render_dashboard_data,
    format_signal_manifest,
)
from portal_bridge import (
    get_schema_registry,
    generate_telemetry_endpoint,
    generate_passport_endpoint,
    generate_signals_endpoint,
)
from unittest import mock
from src.real_p2p_transport import AsyncP2PNode
from src.governor.resource_governor import ResourceGovernor
from src.edge_handoff import EdgeHandoff
from src.stateful_ram import StatefulRAM