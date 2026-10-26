### Task Manifest v9: Step E — Dashboard Widgets & Real Telemetry Render Engine

#### Objective

Implement interactive dashboard widgets for P2P Swarm Core telemetry, Environment Vectors, 5 Regional Passports (Kyiv, Lviv, Odesa, Kharkiv, Dnipro), and live OSINT signals stream, ensuring immediate rendering without empty \--% indicators.

#### Action Items

* **Update**  **docs/telemetry\_feed.json** :  
* Populate with real/simulated telemetry metrics for P2P Swarm Core (RAM usage, coherence, node count).  
* Add spatial and resonance Environment Vectors E.  
* Include 5 regional passports (TERR\_UA\_KYIV\_CENTRAL, TERR\_UA\_LVIV\_CENTRAL, TERR\_UA\_ODESA\_CENTRAL, TERR\_UA\_KHARKIV\_CENTRAL, TERR\_UA\_DNIPRO\_CENTRAL).  
* Append active OSINT signal stream history.  
* **Update**  **docs/index.html**  **&**  **docs/app.js** :  
* Render Widget 1: System & RAM Utilization State.  
* Render Widget 2: Environment Vectors E Progress Gauges.  
* Render Widget 3: Regional Passports Grid (5 Ukrainian Regions).  
* Render Widget 4: Live OSINT Signals Feed.  
* Add client-side fallback data so dashboard displays valid metrics even if fetch fails or runs locally.  
* **Execution & Push** :  
* Run python scripts/run\_live\_simulation.py.  
* Commit all updated files: git add . && git commit \-m "imperia\_v4: Step E Dashboard Widgets & Real Telemetry Render Engine deployed".  
* Push to main branch on GitHub.  
* Update .v4\_gateway/out/execution\_state.json.

