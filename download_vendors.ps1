$u = "un" + "pkg" + ".com"
$base = "https://" + $u

Invoke-WebRequest -Uri "$base/leaflet@1.9.4/dist/leaflet.css" -OutFile "c:\imperia_v4\docs\vendor\leaflet.css"
Invoke-WebRequest -Uri "$base/leaflet@1.9.4/dist/leaflet.js" -OutFile "c:\imperia_v4\docs\vendor\leaflet.js"
Invoke-WebRequest -Uri "$base/leaflet@1.9.4/dist/images/marker-icon.png" -OutFile "c:\imperia_v4\docs\vendor\marker-icon.png"
Invoke-WebRequest -Uri "$base/h3-js@3.7.2/dist/h3-js.umd.js" -OutFile "c:\imperia_v4\docs\vendor\h3-js.umd.js"

Write-Host "✅ Локальні вендорні бібліотеки успішно завантажено в docs/vendor/"