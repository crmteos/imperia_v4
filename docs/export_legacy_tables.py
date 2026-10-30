#!/usr/bin/env python3
"""
Imperia v4: Python Supabase Legacy Tables Archiver
Використовує лише стандартні бібліотеки Python для вивантаження 13 таблиць у docs/legacy_archive/
"""
import os
import re
import json
import urllib.request

LEGACY_TABLES = [
    "archivist_chronicles", "futurology_forecasts", "imperial_news",
    "media_nodes", "orchestra_knowledge", "raw_sources",
    "regions_register", "secretary_chat_history", "territory_passports",
    "treasury_balances", "vagon_ahtungs", "worker_instructions", "worldview_knowledge"
]

def parse_env_config():
    config_path = os.path.join(os.path.dirname(__file__), "env_config.js")
    if not os.path.exists(config_path):
        return None, None
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    url_match = re.search(r"SUPABASE_URL\s*:\s*['\"]([^'\"]+)['\"]", content)
    key_match = re.search(r"SUPABASE_ANON_KEY\s*:\s*['\"]([^'\"]+)['\"]", content)

    url = url_match.group(1) if url_match else None
    key = key_match.group(1) if key_match else None
    return url, key

def archive_tables():
    url, key = parse_env_config()
    out_dir = os.path.join(os.path.dirname(__file__), "legacy_archive")
    os.makedirs(out_dir, exist_ok=True)

    print(f"=== Imperia v4: Archiving {len(LEGACY_TABLES)} Legacy Tables ===")
    if not url or not key or "YOUR_SUPABASE" in url:
        print("[NOTICE] Valid Supabase credentials not found in env_config.js.")
        print("Use docs/export_legacy_tables.sql directly in Supabase SQL Editor.")
        return

    for table in LEGACY_TABLES:
        endpoint = f"{url}/rest/v1/{table}?select=*"
        req = urllib.request.Request(endpoint, headers={
            "apikey": key,
            "Authorization": f"Bearer {key}"
        })
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                file_path = os.path.join(out_dir, f"{table}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"[SUCCESS] Archived {table} ({len(data)} rows) -> {file_path}")
        except Exception as e:
            print(f"[ERROR] Failed to fetch {table}: {e}")

if __name__ == "__main__":
    archive_tables()