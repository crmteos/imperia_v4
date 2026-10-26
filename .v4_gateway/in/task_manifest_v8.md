### Task Manifest v8: Step D — Live Simulation, Territory Passports Verification & Telegram Integration

#### Objective

Execute an end-to-end live simulation connecting all 4 layers of Imperia v4: OSINT signal ingestion, territory passport persistence, P2P core state update, telemetry export (docs/telemetry\_feed.json), and live Telegram broadcasting via @ImperialChanceryBot.

#### Action Items

* **Verify Territory Passports** :  
* Run python scripts/validate\_data\_schema.py or scripts/verify\_territory\_passports.py.  
* Ensure data/territories/TERR\_UA\_KYIV\_CENTRAL.json exists and is schema-valid.  
* **Configure Telegram Integration (**  **config/telegram\_config.json**  **)** :  
* Create config/telegram\_config.json with active bot settings:

{  
  "dry\_run": false,  
  "telegram\_bot\_token": "8680343291:AAEl-um1UGMy4memLKQybK3MN-w8hYig21c",  
  "telegram\_chat\_id": "AUTO\_FETCH\_OR\_USER\_CHAT\_ID"  
}

* **Implement & Execute Live Simulation Script (**  **scripts/run\_live\_simulation.py**  **)** :  
* Ingest sample OSINT signal via SignalCollector.  
* Update territory passport TERR\_UA\_KYIV\_CENTRAL.json on disk.  
* Refresh system telemetry feed docs/telemetry\_feed.json for GitHub Pages Dashboard.  
* Dispatch formatted Markdown report to Telegram via SMMBroadcaster.  
* **Git Operations & Execution State** :  
* Run simulation: python scripts/run\_live\_simulation.py.  
* Verify updated territory data and docs/telemetry\_feed.json.  
* Commit: git commit \-m "imperia\_v4: Step D Live Telegram Broadcast complete".  
* Push to main branch on GitHub.  
* Update .v4\_gateway/out/execution\_state.json.

