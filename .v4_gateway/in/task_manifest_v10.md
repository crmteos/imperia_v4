### Task Manifest v10: Step E Hotfix — Dashboard Widgets Rendering & Relative Fetch Fix

#### Objective

Fix the empty widgets issue on the GitHub Pages dashboard (crmteos.github.io/imperia\_v4/) caused by absolute fetch paths (404 Not Found for /telemetry\_feed.json) and missing DOM fallback rendering in docs/app.js.

#### Action Items

* **Fix Path Resolution in**  **docs/app.js** :  
* Change fetch('/telemetry\_feed.json') to relative path fetch('./telemetry\_feed.json') or fetch('telemetry\_feed.json').  
* Ensure the fetch works across root and subdirectory deployments on GitHub Pages.  
* **Add Hardcoded Fallback & DOM Guards** :  
* Embed DEFAULT\_TELEMETRY in docs/app.js with non-zero values (RAM: 42%, P2P Topology: 12 nodes, Coherence: 0.94, 5 regional passports, active OSINT signals).  
* In .catch() block, trigger rendering with DEFAULT\_TELEMETRY so widgets never display as empty (--%).  
* **Align Element IDs** :  
* Verify that IDs in docs/index.html (ram-usage, vectors-e-spatial, vectors-e-resonance, regional-passports-grid, osint-signals-stream) exactly match the selectors in docs/app.js.  
* **Re-run Simulation & Push** :  
* Run python scripts/run\_live\_simulation.py to regenerate telemetry.  
* Commit and push to GitHub: git add . git commit \-m "imperia\_v4: Hotfix dashboard widgets rendering and relative fetch path" git push origin main

