# STATE GATEWAY PROTOCOL & ANTI-ILLUSION POLICY (v3.0)

## 1. Інваріант Заборони Ілюзій та Оверпромісінгу

- ЗАБОРОНЕНО вигадувати або обіцяти неіснуючі авто-шлюзи, фонові WebSockets між Gemini Notebook та Cline або авто-синхронізатори без участі людини.
- Gemini Notebook є хмарним архітектором (Event-Driven), Cline є локальним інженером у VS Code.
- Всі міжсесійні стани та обмін даними відбуваються виключно через GitHub-репозиторій: https://github.com/crmteos/imperia_v4 та локальний файл `docs/state_gateway.json`.

## 2. Протокол 1-Click Relay (Взаємодія Власник - Архітектор - Інженер)

1. Cline здійснює локальний кодинг у `C:\imperia_v4`, оновлює `docs/state_gateway.json` та виконує `git push`.
2. Власник надсилає команду в чат Gemini Notebook: "Статус" або "Перевіряй".
3. Gemini Notebook аналізує стан репозиторію та створює новий `CLINE_DIRECTIVES.md`.
4. Власник копіює `CLINE_DIRECTIVES.md` у Cline в один клік.