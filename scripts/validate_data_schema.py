#!/usr/bin/env python3
"""Imperia v4 Schema Validation Script - Part 1: Imports and utilities"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Directories
BASE_DIR = Path(__file__).parent.parent / "data"
MANIFEST_PATH = BASE_DIR / "manifest.json"
REGIONS_PATH = BASE_DIR / "regions.json"
TERRITORIES_DIR = BASE_DIR / "territories"

# Error tracking
errors: List[str] = []
warnings: List[str] = []
passed_checks: int = 0


def log_error(message: str) -> None:
    """Record a validation error."""
    errors.append(message)
    print(f"ERROR: {message}")


def log_warning(message: str) -> None:
    """Record a validation warning."""
    warnings.append(message)
    print(f"WARNING: {message}")


def log_pass(message: str) -> None:
    """Record a passed validation check."""
    global passed_checks
    passed_checks += 1
    print(f"PASS: {message}")


def load_json(path: Path) -> Optional[dict]:
    """Load a JSON file, returning None on failure."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log_error(f"Failed to load {path}: {e}")
        return None


def validate_schema_version(
    data: dict, expected_version: str, path: Path
) -> bool:
    """Validate that the schema_version matches the expected version."""
    actual = data.get("schema_version", "")
    if actual == expected_version:
        log_pass(f"{path.name}: schema_version='{actual}' matches expected")
        return True
    log_error(
        f"{path.name}: schema_version='{actual}' does not match expected '{expected_version}'"
    )
    return False


def validate_integer_primary_keys(
    data: dict, path: Path
) -> bool:
    """Validate that all regions have integer primary keys (region_id)."""
    regions = data.get("regions", [])
    if not isinstance(regions, list):
        log_error(f"{path.name}: 'regions' is not a list")
        return False

    region_ids: List[int] = []
    for i, region in enumerate(regions):
        region_id = region.get("region_id")
        if region_id is None:
            log_error(
                f"{path.name}: Region at index {i} missing 'region_id'"
            )
            return False
        if not isinstance(region_id, int):
            log_error(
                f"{path.name}: Region at index {i} has non-integer region_id: {type(region_id).__name__} = {region_id}"
            )
            return False
        if region_id in region_ids:
            log_error(
                f"{path.name}: Duplicate region_id found: {region_id} (index {i})"
            )
            return False
        region_ids.append(region_id)

    log_pass(
        f"{path.name}: All {len(regions)} regions have unique integer region_id values"
    )
    return True


def validate_required_fields(
    data: dict, required_fields: List[str], path: Path
) -> bool:
    """Validate that all required fields are present in the data."""
    missing = [f for f in required_fields if f not in data]
    if missing:
        log_error(
            f"{path.name}: Missing required fields: {', '.join(missing)}"
        )
        return False
    log_pass(
        f"{path.name}: All required fields present: {', '.join(required_fields)}"
    )
    return True


def validate_cross_references(
    manifest: dict, regions_data: dict, territories_data: List[dict]
) -> bool:
    """Validate cross-entity references between manifest, regions, and territories."""
    refs_ok = True

    # Check territory region_id references
    valid_region_ids: set = {r["region_id"] for r in regions_data.get("regions", [])}

    for t in territories_data:
        region_id = t.get("region_id")
        if region_id is not None and region_id not in valid_region_ids:
            log_error(
                f"territory_id {t.get('territory_id', '?')}: "
                f"region_id={region_id} references unknown region"
            )
            refs_ok = False

        # Check territory_id references in links
        neighbor_ids = t.get("links", {}).get("neighboring_territories", [])
        for nid in neighbor_ids:
            if nid not in valid_region_ids and nid not in [
                t2.get("territory_id") for t2 in territories_data
            ]:
                log.warning(
                    f"territory_id {t.get('territory_id')}: neighboring_territory_id {nid} not found in regions or territories"
                )

    if refs_ok:
        log_pass("Cross-entity references validated")

    return refs_ok


def validate_environment_vector_e(
    data: dict, path: Path
) -> bool:
    """Validate environment vector E has exactly 4 components."""
    vector_data = data.get("environment_vector_e", data.get("osint_parameters", {}).get("vector_e", {}))

    if isinstance(vector_data, dict):
        # Check for E_geo, E_resource, E_coherence, E_temporal keys
        required_keys = ["E_geo", "E_resource", "E_coherence", "E_temporal"]
        missing = [k for k in required_keys if k not in vector_data]
        if missing:
            log_warning(
                f"{path.name}: Missing vector keys: {', '.join(missing)}"
            )

        # Validate each component has magnitude and direction
        for key in required_keys:
            if key in vector_data:
                comp = vector_data[key]
                if not isinstance(comp, dict):
                    log_error(
                        f"{path.name}: {key} is not a dict, got {type(comp).__name__}"
                    )
                    return False
                if "magnitude" not in comp:
                    log_error(
                        f"{path.name}: {key} missing 'magnitude'"
                    )
                    return False
                if "direction" not in comp:
                    log_error(
                        f"{path.name}: {key} missing 'direction'"
                    )
                    return False
                if not isinstance(comp["magnitude"], (int, float)):
                    log_error(
                        f"{path.name}: {key}.magnitude is not a number"
                    )
                    return False

        log_pass(f"{path.name}: environment_vector_e structure valid")
        return True

    elif isinstance(vector_data, list):
        # Legacy list format: [mag_geo, mag_resource, mag_coherence, mag_temporal]
        if len(vector_data) != 4:
            log_error(
                f"{path.name}: environment vector list must have exactly 4 elements, got {len(vector_data)}"
            )
            return False
        for i, v in enumerate(vector_data):
            if not isinstance(v, (int, float)):
                log_error(
                    f"{path.name}: vector element {i} is not a number: {type(v).__name__}"
                )
                return False
        log_pass(f"{path.name}: environment vector list format valid (4 elements)")
        return True

    else:
        log_warning(f"{path.name}: No environment_vector_e field found")
        return True


def validate_h3_resolution(data: dict, path: Path) -> bool:
    """Validate H3 resolution is within valid range (0-15)."""
    h3_res = data.get("h3_resolution")
    if h3_res is None:
        log_warning(f"{path.name}: No h3_resolution field found")
        return True  # Not required for all passports

    try:
        h3_res_int = int(h3_res)
    except (ValueError, TypeError):
        log_error(f"{path.name}: h3_resolution is not an integer: {h3_res}")
        return False

    if h3_res_int < 0 or h3_res_int > 15:
        log_error(
            f"{path.name}: h3_resolution out of valid range (0-15): {h3_res}"
        )
        return False

    log_pass(f"{path.name}: h3_resolution={h3_res_int} is within valid range (0-15)")
    return True


def validate_all_territories(
    territories_dir: Path, manifest_version: str
) -> bool:
    """Validate all JSON files in the territories directory."""
    territory_files = sorted(territories_dir.glob("*.json"))
    territories_loaded: List[dict] = []

    if not territory_files:
        log_error(f"{territories_dir.name}: No JSON territory files found")
        return False

    log_pass(f"Found {len(territory_files)} territory passport file(s)")

    for tf in territory_files:
        data = load_json(tf)
        if data is None:
            continue  # Already logged error

        territories_loaded.append(data)

        # Validate schema version
        if not validate_schema_version(data, manifest_version, tf):
            pass  # Errors already logged

        # Validate required fields for territory passports
        required_t = [
            "territory_id",
            "region_id",
            "name",
            "h3_resolution",
        ]
        if not validate_required_fields(data, required_t, tf):
            pass  # Errors already logged

        # Validate H3 resolution
        if not validate_h3_resolution(data, tf):
            pass  # Errors already logged

        # Validate environment vector E
        if not validate_environment_vector_e(data, tf):
            pass  # Errors already logged

    return True


def main() -> int:
    """Main entry point for schema validation."""
    global passed_checks

    print("=" * 60)
    print("Imperia v4 - Schema Validation Script")
    print("=" * 60)
    print(f"Version: v4.0.0-step_b")
    print()

    # Load and validate central manifest
    print("--- Validating Central Manifest ---")
    manifest_data = load_json(MANIFEST_PATH)
    if manifest_data is None:
        print("\nValidation failed: Could not load central manifest.")
        return 1

    if not validate_schema_version(manifest_data, "v4.0.0-step_b", MANIFEST_PATH):
        pass

    # Validate required fields in manifest
    manifest_required = ["schema_version", "key_space", "entities", "validation_constraints"]
    if not validate_required_fields(manifest_data, manifest_required, MANIFEST_PATH):
        pass

    # Validate integer primary keys in regions
    print("\n--- Validating Regional Registry ---")
    regions_data = load_json(REGIONS_PATH)
    if regions_data is None:
        print("\nValidation failed: Could not load regional registry.")
        return 1

    if not validate_schema_version(regions_data, "v4.0.0-step_b", REGIONS_PATH):
        pass

    if not validate_integer_primary_keys(regions_data, REGIONS_PATH):
        pass

    # Validate all territory passports
    print("\n--- Validating Territorial Passports ---")
    result = validate_all_territories(TERRITORIES_DIR, "v4.0.0-step_b")
    if not result:
        pass  # Errors logged inside

    # Cross-reference validation
    print("\n--- Validating Cross-Entity References ---")
    regions_list = regions_data.get("regions", []) if regions_data else []
    territories_passports = (
        [load_json(f) for f in sorted(TERRITORIES_DIR.glob("*.json"))]
        if regions_list
        else []
    )

    # Only validate references if we have both regions and territories
    if regions_list and territories_passports:
        refs_ok = validate_cross_references(manifest_data, regions_data, territories_passports)
        if not refs_ok:
            pass  # Errors already logged

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Passed checks: {passed_checks}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print("\nERRORS DETAIL:")
        for e in errors:
            print(f"  - {e}")

    if warnings:
        print("\nWARNINGS DETAIL:")
        for w in warnings:
            print(f"  - {w}")

    if not errors:
        print("\nAll validation checks passed!")
        return 0
    else:
        print("\nValidation failed with errors present.")
        return 1


if __name__ == "__main__":
    sys.exit(main())