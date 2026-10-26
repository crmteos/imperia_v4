### Task Manifest v10: Step E Hotfix — Dashboard Widgets Rendering & Relative Fetch Fix

#### Objective

Fix empty widgets on https\://crmteos.github.io/imperia\_v4/ by fixing path resolution in docs/app.js, aligning DOM IDs in docs/index.html, and embedding instant fallback telemetry data.

#### Action Items

* **Fix Fetch Path in**  **docs/app.js** :  
* Replace absolute /telemetry\_feed.json with relative ./telemetry\_feed.json or telemetry\_feed.json.  
* Add .catch() handler that falls back to DEFAULT\_TELEMETRY if fetch fails or returns 404\.  
* **Embed**  **DEFAULT\_TELEMETRY**  **Fallback in**  **docs/app.js** :  
* Define full telemetry object with non-zero metrics:  
* RAM: 42%  
* P2P Topology: 12 nodes active  
* Vectors E: Spatial Coherence 0.94, Resonance 0.88  
* Regions: Kyiv (101), Lviv (102), Odesa (103), Kharkiv (104), Dnipro (105)  
* Signals: 3 active OSINT signals with timestamps  
* **Verify DOM Element IDs in**  **docs/index.html** :  
* Ensure containers for system metrics, vector indicators, region grid, and signal ticker match app.js querySelectors.  
* **Re-generate & Deploy** :  
* Run python scripts/run\_live\_simulation.py to refresh docs/telemetry\_feed.json.  
* Commit and push to main: git add . && git commit \-m "imperia\_v4: Hotfix dashboard widgets rendering and relative fetch path" && git push origin main

