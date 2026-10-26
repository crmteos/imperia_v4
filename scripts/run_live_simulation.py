#!/usr/bin/env python3
import json, os, urllib.request
from datetime import datetime, timezone

TERRITORY_FILE = "data/territories/TERR_UA_KYIV_CENTRAL.json"
CONFIG_FILE = "config/telegram_config.json"
TELEMETRY_FEED = "docs/telemetry_feed.json"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ingest_signal(territory, region_id, summary, source="live_sim", confidence=0.85):
    sig = {"signal_type": "geopolitical", "region_id": region_id, "summary": summary, 
           "source": source, "confidence": confidence, "timestamp": datetime.now(timezone.utc).isoformat()}
    existing = [s.get("summary") for s in territory.get("osint_signals", [])]
    if summary not in existing:
        territory.setdefault("osint_signals", []).append(sig)
        print(f"Signal ingested: {summary}")
    return sig

def update_passport(territory, sig):
    territory["osint_signals"].append(sig)
    territory["last_signal_timestamp"] = sig["timestamp"]
    territory["updated"] = datetime.now(timezone.utc).isoformat()
    print(f"Passport updated: {territory['territory_id']}")
    return territory

def refresh_telemetry():
    data = {"status": "live_broadcast", "timestamp": datetime.now(timezone.utc).isoformat(),
            "territory": "TERR_UA_KYIV_CENTRAL", "message": "Live feed refreshed"}
    save_json(TELEMETRY_FEED, data)
    print("Telemetry feed refreshed")

def send_telegram_broadcast(token, chat_id, message, parse_mode="Markdown"):
    if not token or not chat_id or chat_id == "<ВАШ_CHAT_ID>":
        print("Telegram token or chat_id missing or placeholder, skipping live broadcast")
        return False
    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": parse_mode}
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(api_url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        if result.get("ok"):
            print(f"Live broadcast sent to Telegram chat {chat_id}")
            return True
        else:
            print(f"Telegram API error: {result}")
            return False
    except Exception as e:
        print(f"Failed to send Telegram broadcast: {e}")
        return False

def main():
    print("=" * 60)
    print("Imperia v4 - Step D: Live Telegram Broadcast Simulation")
    print("=" * 60)
    
    # Load configuration
    print("\n[1/5] Loading configuration...")
    config = load_json(CONFIG_FILE)
    dry_run = config.get("dry_run", True)
    token = config.get("telegram_bot_token")
    chat_id = config.get("telegram_chat_id")
    
    if dry_run:
        print("⚠️  Dry-run mode: no live Telegram broadcast will be sent")
    
    # Load territory passport
    print("\n[2/5] Loading territory passport...")
    territory_data = load_json(TERRITORY_FILE)
    print(f"  Territory: {territory_data['territory_id']} ({territory_data['name']})")
    
    # Ingest OSINT signal
    print("\n[3/5] Ingesting OSINT signal...")
    signal = ingest_signal(
        territory_data, 
        region_id=territory_data.get("region_id", 1),
        summary="Live geopolitical OSINT signal - Step D simulation",
        source="live_simulation",
        confidence=0.88
    )
    
    # Update territory passport
    print("\n[4/5] Updating territory passport...")
    update_passport(territory_data, signal)
    save_json(TERRITORY_FILE, territory_data)
    
    # Refresh telemetry feed
    print("\n[5/5] Refreshing telemetry feed...")
    refresh_telemetry()
    
    # Send live broadcast to Telegram (if not dry run)
    print("\n" + "=" * 60)
    if not dry_run and token and chat_id and chat_id != "<ВАШ_CHAT_ID>":
        print("Sending live broadcast to Telegram...")
        timestamp_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        message = "[Step D] Live geopolitical OSINT signal detected for " + territory_data['name'] + " territory. Timestamp: " + timestamp_str
        send_telegram_broadcast(token, chat_id, message, parse_mode="Markdown")
    elif dry_run:
        print("(Dry-run mode - Telegram broadcast skipped)")
    else:
        print("⚠️  Telegram credentials not configured - broadcast skipped")
        print("   Set telegram_bot_token and telegram_chat_id in config/telegram_config.json")
    
    print("=" * 60)
    print("Step D simulation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()