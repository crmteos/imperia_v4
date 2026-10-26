"""src/signal_collector.py - OSINT Signal Collector.

OSINT signal collector that parses incoming external feeds, sanitizes input,
and links verified signals to integer primary key regions in data/regions.json
and territory passports in data/territories/.
"""
import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger("signal_collector")


class SignalCollector:
    """OSINT signal collector for parsing, validating, and ingesting signals."""

    def __init__(self, regions_data: dict, territories_dir: str = "data/territories/") -> None:
        self.regions_data = regions_data
        self.territories_dir = Path(territories_dir)

        # Build valid region ID set
        self.valid_region_ids: set[int] = set()
        if "regions" in regions_data:
            for region in regions_data["regions"]:
                rid = region.get("region_id")
                if rid is not None:
                    self.valid_region_ids.add(int(rid))

        logger.info(
            f"SignalCollector initialized with {len(self.valid_region_ids)} valid region IDs"
        )

    def validate_region_id(self, region_id: int) -> bool:
        """Validate that a region ID exists in the registered regions."""
        if region_id in self.valid_region_ids:
            return True
        logger.warning(f"Region ID {region_id} not found in registered regions")
        return False

    def sanitize_signal(self, signal: dict) -> dict:
        """Sanitize and validate an incoming OSINT signal.

        Args:
            signal: Raw signal dict from external source.

        Returns:
            Sanitized signal dict if valid, raises ValueError if invalid.
        """
        if not isinstance(signal, dict):
            raise ValueError("Signal must be a dictionary")

        # Required fields
        required = ["signal_type", "region_id", "summary", "source", "confidence"]
        missing = [f for f in required if f not in signal]
        if missing:
            raise ValueError(f"Missing required signal fields: {', '.join(missing)}")

        # Validate region_id is a valid integer from our regions
        try:
            rid = int(signal["region_id"])
            if not self.validate_region_id(rid):
                raise ValueError(f"Invalid region_id: {rid}")
            signal["region_id"] = rid
        except (ValueError, TypeError):
            raise ValueError(f"region_id must be an integer: {signal.get('region_id')}")

        # Validate confidence is a number between 0 and 1
        try:
            conf = float(signal["confidence"])
            if not (0 <= conf <= 1):
                raise ValueError(f"Confidence must be between 0 and 1: {conf}")
            signal["confidence"] = conf
        except (ValueError, TypeError):
            raise ValueError(f"Confidence must be a number: {signal.get('confidence')}")

        # Ensure summary is a string
        if not isinstance(signal["summary"], str):
            signal["summary"] = str(signal["summary"])

        # Ensure source is a string
        if not isinstance(signal["source"], str):
            signal["source"] = str(signal["source"])

        # Validate signal_type
        valid_types = ["geopolitical", "resource", "security", "environment", "demographic"]
        if signal["signal_type"] not in valid_types:
            logger.warning(
                f"Unsignal_type '{signal['signal_type']}' not in standard types: {valid_types}"
            )

        logger.debug(f"Signal sanitized: {signal['signal_type']} for region {signal['region_id']}")
        return signal

    async def ingest_signal(self, signal: dict) -> Optional[dict]:
        """Ingest a verified signal and append it to the appropriate territory passport.

        Args:
            signal: Sanitized signal dict.

        Returns:
            Dict with ingestion result, or None if ingestion failed.
        """
        try:
            sanitized = self.sanitize_signal(signal)
        except ValueError as e:
            logger.error(f"Signal validation failed: {e}")
            return {"status": "validation_error", "error": str(e)}

        region_id = sanitized["region_id"]

        # Find the territory passport file for this region
        territory_file = None
        territory_data = None

        # Look through existing territory passports
        if self.territories_dir.exists():
            for tf in self.territories_dir.glob("*.json"):
                try:
                    with open(tf, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if data.get("region_id") == region_id:
                        territory_file = tf
                        territory_data = data
                        break
                except (json.JSONDecodeError, KeyError, OSError) as e:
                    logger.warning(f"Failed to read {tf}: {e}")
                    continue

        # If no existing territory found, create a new one based on region data
        if territory_data is None:
            territory_data = self._create_default_territory(region_id)
            territory_file = self.territories_dir / f"territory_{region_id}.json"

        # Append the signal to the territory's OSINT signals list
        if "osint_signals" not in territory_data:
            territory_data["osint_signals"] = []

        # Check if signal already exists (by source + summary hash)
        existing_signals = territory_data.get("osint_signals", [])
        for existing in existing_signals:
            if existing.get("source") == sanitized["source"]:
                logger.info(f"Signal already exists for region {region_id}: {signal['source']}")
                return {"status": "duplicate", "region_id": region_id}

        # Add the new signal
        territory_data["osint_signals"].append(sanitized)

        # Save the updated territory passport
        try:
            self.territories_dir.mkdir(parents=True, exist_ok=True)
            with open(territory_file, "w", encoding="utf-8") as f:
                json.dump(territory_data, f, indent=2, ensure_ascii=False)

            logger.info(
                f"Ingested OSINT signal '{sanitized['signal_type']}' for region {region_id} "
                f"into {territory_file.name}"
            )

            return {
                "status": "success",
                "region_id": region_id,
                "territory_file": territory_file.name,
                "signal_type": sanitized["signal_type"],
            }

        except OSError as e:
            logger.error(f"Failed to write territory file {territory_file}: {e}")
            return {"status": "write_error", "error": str(e)}

    def _create_default_territory(self, region_id: int) -> dict:
        """Create a default territory passport for a given region ID.

        Args:
            region_id: The region integer primary key.

        Returns:
            Default territory dict structure.
        """
        # Look up region info
        region_info = None
        if "regions" in self.regions_data:
            for r in self.regions_data["regions"]:
                if r.get("region_id") == region_id:
                    region_info = r
                    break

        region_name = f"Region {region_id}"
        region_code = f"R-{region_id:02d}"
        if region_info:
            region_name = region_info.get("region_name", region_name)
            region_code = region_info.get("region_code", region_code)

        return {
            "territory_id": f"TERR-{region_id}",
            "region_id": region_id,
            "name": region_name,
            "region_code": region_code,
            "h3_resolution": 9,
            "operational_status": "active",
            "environment_vector_e": {
                "E_geo": 0.5,
                "E_resource": 0.5,
                "E_coherence": 0.5,
                "E_temporal": 0.5,
            },
            "risk_assessment": "low",
            "osint_signals": [],
            "created": __import__("datetime").datetime.now(
                __import__("datetime").timezone.utc
            ).isoformat(),
        }