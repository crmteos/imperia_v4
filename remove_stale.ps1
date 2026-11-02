Remove-Item -Force -ErrorAction SilentlyContinue 'c:\imperia_v4\docs\index.html', 'c:\imperia_v4\docs\map_core.html', 'c:\imperia_v4\index.html'
Write-Host "✅ Stale files removed"