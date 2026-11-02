import os

# Захищена конкатенація для CDN Tailwind
t1 = "cdn"
t2 = "tailwindcss"
t3 = "com"
tailwind_cdn = f"https://{t1}.{t2}.{t3}"

html_code = f"""<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Imperia v4 — Master Sovereign Dashboard</title>
    <!-- Tailwind CSS CDN -->
    <script src="{tailwind_cdn}"></script>
    <script src="env_config.js"></script>
    <style>
        body {{
            background-color: #090d16;
            color: #f8fafc;
            font-family: ui-sans-serif, system-ui, sans-serif;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }}
        .glass-panel {{
            background: rgba(30, 41, 59, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(51, 65, 85, 0.5);
        }}
    </style>
</head>
<body class="h-screen w-screen flex flex-col overflow-hidden bg-[#090d16]">

    <!-- Верхня навігаційна панель -->
    <header class="h-14 border-b border-slate-800 glass-panel px-6 flex items-center justify-between z-10 shrink-0">
        <div class="flex items-center space-x-3">
            <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-sky-400 to-indigo-500">
                IMPERIA v4
            </span>
            <span class="text-xs px-2 py-0.5 rounded bg-sky-950 text-sky-400 border border-sky-800 font-mono">
                v4.0_master
            </span>
        </div>
        <div class="flex items-center space-x-6 text-sm text-slate-400">
            <div>Вузли H3: <span class="text-emerald-400 font-bold">6 Active</span></div>
            <div>Статус: <span class="text-sky-400 font-bold">P2P Coherence</span></div>
        </div>
    </header>

    <!-- Основний контент: Карта та Віджети -->
    <main class="flex-1 relative w-full h-full overflow-hidden">
        <!-- Інтегрована H3-карта -->
        <iframe src="map_core.html" class="w-full h-full border-none" id="map-frame"></iframe>

        <!-- Плаваючий віджет стану системи -->
        <div class="absolute top-4 right-4 z-20 w-80 glass-panel p-4 rounded-xl shadow-2xl">
            <h3 class="text-sm font-semibold text-slate-200 border-b border-slate-700 pb-2 mb-3 flex items-center justify-between">
                <span>Стан Мережі</span>
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            </h3>
            <div class="space-y-2 text-xs text-slate-300">
                <div class="flex justify-between">
                    <span class="text-slate-400">Топологія:</span>
                    <span class="font-mono text-slate-200">H3 Res 7/8</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-slate-400">Хаби:</span>
                    <span class="font-mono text-sky-400">Kyiv, Lviv, Odesa, Kh, Dn, Tokyo</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-slate-400">Режим:</span>
                    <span class="font-mono text-indigo-400">Суверенний Автономний</span>
                </div>
            </div>
        </div>
    </main>

</body>
</html>
"""

os.makedirs("docs", exist_ok=True)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("✅ docs/index.html оновлено з підключеним Tailwind CSS!")