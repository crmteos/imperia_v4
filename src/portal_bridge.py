"""src/portal_bridge.py - Client-side HTTP/JSON portal adapter.

Exposes schema registry and territorial passports for static web rendering
(GitHub Pages / local web gateway). Zero human bias, deterministic output.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

from kancelyariya_facade import export_telemetry, format_signal_manifest

logger = logging.getLogger("portal_bridge")


# ── Schema Registry ──────────────────────────────────────────────────────


SCHEMA_REGISTRY = {
    "version": "4.1.0",
    "description": "Imperia v4 telemetry and signal schema",
    "endpoints": {
        "telemetry": "/.well-known/telemetry.json",
        "passport": "/.well-known/passport.json",
        "signals": "/.well-known/signals.json",
    },
}


def get_schema_registry() -> dict:
    """Expose the schema registry for static frontend consumption."""
    return SCHEMA_REGISTRY


# ── Static JSON Endpoints ───────────────────────────────────────────────


def generate_telemetry_endpoint(e_vector: dict, ram: Any, node: Any) -> dict:
    """Generate the /telemetry.json endpoint data.

    Calls the kancelyariya_facade export_telemetry to produce the
    standardized telemetry payload.
    """
    try:
        data = export_telemetry(e_vector, ram, node)
        return data
    except Exception as e:
        logger.error(f"Failed to generate telemetry endpoint: {e}")
        return {"error": str(e), "schema_version": "4.1.0"}


def generate_passport_endpoint(e_vector: dict, ram: Any, node: Any) -> dict:
    """Generate the /passport.json endpoint data.

    Contains the node's regional intelligence passport with
    resource mode, vector signals, and P2P topology summary.
    """
    try:
        telemetry = generate_telemetry_endpoint(e_vector, ram, node)
        signals = format_signal_manifest(ram, node)
        passport = {
            "node_id": getattr(node, "node_id", "unknown") if node else "unknown",
            "resource_mode": telemetry.get("ram_state", {}).get("utilization_percent", 0),
            "vector_signals": telemetry.get("vector_signals", {}).get("signals", {}),
            "p2p_summary": {
                "peer_count": telemetry.get("p2p_topology", {}).get("peer_count", 0),
                "mode": telemetry.get("p2p_topology", {}).get("mode", "unknown"),
            },
            "signals": signals,
            "generated_at": telemetry.get("export_timestamp", datetime.now(timezone.utc).isoformat()),
        }
        return passport
    except Exception as e:
        logger.error(f"Failed to generate passport endpoint: {e}")
        return {"error": str(e), "schema_version": "4.1.0"}


def generate_signals_endpoint(ram: Any, node: Any) -> dict:
    """Generate the /signals.json endpoint data.

    Contains the active user-facing signals formatted from Context RAM.
    """
    try:
        signals = format_signal_manifest(ram, node)
        return {"signals": signals, "generated_at": datetime.now(timezone.utc).isoformat(), "schema_version": "4.1.0"}
    except Exception as e:
        logger.error(f"Failed to generate signals endpoint: {e}")
        return {"error": str(e), "schema_version": "4.1.0"}


def generate_telemetry_feed(e_vector: dict, ram: Any, node: Any) -> None:
    """Generate and write live system telemetry to docs/telemetry_feed.json.

    This function:
    1. Calls export_telemetry from kancelyariya_facade to get the full telemetry payload
    2. Writes the result to docs/telemetry_feed.json for GitHub Pages dashboard
    3. Uses zero-server client-side JSON fetching pattern

    The output format is compatible with the Step A GitHub Pages dashboard
    which fetches this file via relative URL /telemetry_feed.json or
    /.well-known/telemetry_feed.json.
    """
    try:
        telemetry = generate_telemetry_endpoint(e_vector, ram, node)

        # Augment with feed metadata for dashboard consumption
        feed = {
            "schema_version": "4.1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "feed_type": "imperia_v4_system_telemetry",
            "telemetry": telemetry,
        }

        # Ensure docs directory exists
        DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
        TELEMETRY_FEED_PATH = os.path.join(DOCS_DIR, "telemetry_feed.json")
        os.makedirs(DOCS_DIR, exist_ok=True)

        # Write to docs/telemetry_feed.json with pretty-printed JSON
        # This file is consumed client-side via fetch('/telemetry_feed.json')
        with open(TELEMETRY_FEED_PATH, "w", encoding="utf-8") as f:
            json.dump(feed, f, indent=2, ensure_ascii=False)

        logger.info(f"Telemetry feed written to {TELEMETRY_FEED_PATH}")
    except Exception as e:
        logger.error(f"Failed to generate telemetry feed: {e}")
        # Write error state so dashboard doesn't crash on missing data
        error_feed = {
            "schema_version": "4.1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "feed_type": "imperia_v4_system_telemetry",
            "error": str(e),
        }
        with open(TELEMETRY_FEED_PATH, "w", encoding="utf-8") as f:
            json.dump(error_feed, f, indent=2, ensure_ascii=False)


def get_schema_registry() -> dict:
    """Expose the schema registry for static frontend consumption."""
    SCHEMA_REGISTRY = {
        "version": "4.1.0",
        "description": "Imperia v4 telemetry and signal schema",
        "endpoints": {
            "telemetry": "/.well-known/telemetry.json",
            "passport": "/.well-known/passport.json",
            "signals": "/.well-known/signals.json",
            "telemetry_feed": "/telemetry_feed.json",
        },
    }
    return SCHEMA_REGISTRY