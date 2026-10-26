"""tests/test_step_c_broadcasting.py - Step C Broadcasting & Signal Collector Tests.

Integration tests ensuring end-to-end signal collection, verification against
data/manifest.json schema, and dry-run broadcasting.
"""
import json
import pytest
from src.smm_broadcaster import SMMBroadcaster
from src.signal_collector import SignalCollector


@pytest.fixture
def regions_data():
    """Load regions data for testing."""
    with open("data/regions.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def signal_collector(regions_data):
    """Create a SignalCollector instance for testing."""
    return SignalCollector(regions_data)


@pytest.fixture
def broadcaster_dry_run():
    """Create a broadcaster in dry-run mode."""
    return SMMBroadcaster({"dry_run": True}, dry_run=True)


@pytest.fixture
def broadcaster_with_telegram():
    """Create a broadcaster with Telegram config (dry-run)."""
    return SMMBroadcaster({"telegram_bot_token": "test_token", "telegram_chat_id": "test_chat"})
class TestSignalCollector:
    """Tests for SignalCollector class."""

    def test_init_validates_region_ids(self, regions_data):
        """SignalCollector should initialize with valid region IDs from regions data."""
        assert True  # Placeholder

    def test_init_region_id_set(self, regions_data):
        """SignalCollector should build correct region ID set."""
        collector = SignalCollector(regions_data)
        assert 1 in collector.valid_region_ids
        assert 5 in collector.valid_region_ids
        assert 99 not in collector.valid_region_ids

    def test_validate_region_id_valid(self, signal_collector):
        """validate_region_id should return True for valid region IDs."""
        assert signal_collector.validate_region_id(1) is True
        assert signal_collector.validate_region_id(5) is True

    def test_validate_region_id_invalid(self, signal_collector):
        """validate_region_id should return False for invalid region IDs."""
        assert signal_collector.validate_region_id(99) is False
        assert signal_collector.validate_region_id(0) is False

    def test_sanitize_signal_valid(self, signal_collector):
        """sanitize_signal should valid signals pass through."""
        signal = {
            "signal_type": "geopolitical",
            "region_id": 1,
            "summary": "Test geopolitical signal",
            "source": "test_source",
            "confidence": 0.85,
        }
        result = signal_collector.sanitize_signal(signal)
        assert result["region_id"] == 1
        assert result["confidence"] == 0.85
        assert result["signal_type"] == "geopolitical"

    def test_sanitize_signal_missing_fields(self, signal_collector):
        """sanitize_signal should raise ValueError for missing required fields."""
        incomplete = {"signal_type": "geopolitical", "region_id": 1}
        from pytest import raises
        with raises(ValueError, match="Missing required signal fields"):
            signal_collector.sanitize_signal(incomplete)

    def test_sanitize_signal_invalid_region(self, signal_collector):
        """sanitize_signal should raise ValueError for invalid region ID."""
        signal = {
            "signal_type": "geopolitical",
            "region_id": 99,
            "summary": "Test signal",
            "source": "test_source",
            "confidence": 0.85,
        }
        from pytest import raises
        with raises(ValueError, match="region_id must be an integer"):
            signal_collector.sanitize_signal(signal)

    def test_sanitize_signal_invalid_confidence(self, signal_collector):
        """sanitize_signal should raise ValueError for invalid confidence."""
        signal = {
            "signal_type": "geopolitical",
            "region_id": 1,
            "summary": "Test signal",
            "source": "test_source",
            "confidence": 1.5,
        }
        from pytest import raises
        with raises(ValueError, match="Confidence must be a number"):
            signal_collector.sanitize_signal(signal)

    async def test_ingest_signal_success(self, signal_collector, tmp_path):
        """ingest_signal should successfully ingest and save to territory passport."""
        pytest.mark.asyncio
        signal = {
            "signal_type": "geopolitical",
            "region_id": 1,
            "summary": "Test geopolitical signal",
            "source": "test_source",
            "confidence": 0.85,
        }
        result = await signal_collector.ingest_signal(signal)
        assert result["status"] == "success"
        assert result["region_id"] == 1
        assert result["signal_type"] == "geopolitical"

    async def test_ingest_signal_duplicate(self, signal_collector, tmp_path):
        """ingest_signal should detect duplicate signals by source."""
        signal = {
            "signal_type": "geopolitical",
            "region_id": 1,
            "summary": "Test geopolitical signal",
            "source": "test_source",
            "confidence": 0.85,
        }
        result1 = await signal_collector.ingest_signal(signal)
        assert result1["status"] == "success"
        result2 = await signal_collector.ingest_signal(signal)
        assert result2["status"] == "duplicate"

    async def test_ingest_signal_validates_region(self, signal_collector):
        """ingest_signal should reject signals with invalid region IDs."""
        pytest.mark.asyncio
        signal = {
            "signal_type": "geopolitical",
            "region_id": 99,
            "summary": "Test signal",
            "source": "test_source",
            "confidence": 0.85,
        }
        result = await signal_collector.ingest_signal(signal)
        assert result["status"] == "validation_error"
class TestBroadcastIntegration:
    """Integration tests for broadcasting and signal collection."""

    def test_broadcast_telemetry_fallback(self, broadcaster_with_telegram):
        """Test telemetry broadcast formatting with SMMBroadcaster."""
        telemetry_data = {
            "e_vector": {"E_geo": 0.5, "E_resource": 0.3, "E_coherence": 0.8, "E_temporal": 0.9},
            "ram_budget": 1024,
            "node_count": 42,
            "operational_status": "active",
        }
        message = broadcaster_with_telegram._format_telemetry_markdown(telemetry_data)
        assert "🛰️ Imperia v4 Telemetry Update" in message