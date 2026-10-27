// Imperia v4: Human-Centric UI Translator Engine

class HumanUITranslator {
  /**
   * Translate raw E_soc value to human-readable tension badge
   */
  getTensionBadge(eSoc) {
    if (eSoc < 0.35) {
      return `<span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-green-900/60 text-green-300 border border-green-500/40">🟢 Спокійний контур (${(eSoc * 100).toFixed(0)}%)</span>`;
    } else if (eSoc < 0.65) {
      return `<span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-yellow-900/60 text-yellow-300 border border-yellow-500/40">🟡 Помірний шум (${(eSoc * 100).toFixed(0)}%)</span>`;
    } else {
      return `<span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-red-900/60 text-red-300 border border-red-500/40">🔴 Підвищена напруга (${(eSoc * 100).toFixed(0)}%)</span>`;
    }
  }

  /**
   * Translate raw Q-Factor to human-readable coherence label
   */
  getCoherenceLabel(qFactor) {
    if (qFactor >= 0.90) return "✨ Максимальна когерентність (Брахман)";
    if (qFactor >= 0.80) return "⚡ Стабільна оркестрація (Кшатрій)";
    if (qFactor >= 0.70) return "📊 Адаптивний ресурс (Вайш'я)";
    return "📡 Базовий сенсор (Шудра)";
  }

  /**
   * Render Human-Centric Regional Passport Card
   */
  renderHumanPassportCard(passport) {
    const badge = this.getTensionBadge(passport.E_soc || 0.25);
    const coherence = this.getCoherenceLabel(passport.qFactor || 0.85);
    
    return `
      <div class="p-4 mb-3 bg-gray-800/80 rounded-xl border border-gray-700/60 shadow-lg hover:border-blue-500/50 transition">
        <div class="flex justify-between items-center mb-2">
          <h4 class="text-base font-bold text-white flex items-center gap-2">
            📍 ${passport.name}
          </h4>
          ${badge}
        </div>
        <p class="text-xs text-gray-300 mb-3">${passport.humanSummary || "Регіональний хаб працює в штатному режимі без системних аномалій."}</p>
        <div class="grid grid-cols-2 gap-2 text-xs bg-gray-900/60 p-2.5 rounded-lg border border-gray-800">
          <div><span class="text-gray-400">Якість когерентності:</span> <div class="font-semibold text-blue-400 mt-0.5">${coherence}</div></div>
          <div><span class="text-gray-400">Q-Індекс:</span> <div class="font-mono text-green-400 mt-0.5">${passport.qFactor || 0.85}</div></div>
        </div>
      </div>
    `;
  }
}

if (typeof window !== 'undefined') {
  window.humanUI = new HumanUITranslator();
}