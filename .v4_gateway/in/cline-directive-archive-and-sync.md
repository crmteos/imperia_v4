# 🏛️ DIRECTIVE: Archiving Legacy v3.0 Files & Syncing Master Architecture Spec v4.0

- **Target Role:** Local Senior Python Engineer / System Architect
- **Context Baseline:** `imperia-v4-master-architecture-spec.md`, `SYSTEM_ENVIRONMENT.md`
- **Execution Mode:** File Cleanup, Relocation & Git Synchronization

---

## 📐 1. Мета Завдання
Очистити робочу директорію проєкту від застарілих специфікацій версії 3.0 шляхом їх перенесення до архівного каталогу `.v4_gateway/archive/v3_legacy/`, а також зафіксувати новий Канонічний Маніфест `imperia-v4-master-architecture-spec.md` у версійному контролі Git.

---

## 📁 2. Покроковий Алгоритм Дій

### Крок 1: Створення архівного каталогу
Створити директорію (якщо вона ще не існує):
```bash
mkdir -p .v4_gateway/archive/v3_legacy/
```

### Крок 2: Переміщення застарілих специфікацій v3.0
Перемістити наступні файли (та їх варіанти) з кореня або робочих папок у `.v4_gateway/archive/v3_legacy/`:
- `1.Єдиний_Фреймворк_Джерела_Правди_v3.0_Master_Framework.md` (або `1.*.md`)
- `2.Зведений_Реєстр_Документації*.md` (або `2.*.md`)
- `4.Специфікація_та_Співвідношення_Парадигм*.md` (або `4.*.md`)

*Примітка:* Якщо деякі з цих файлів уже відсутні в коріння або мають модифіковані назви, перемісти будь-які файли специфікацій v3.0 до `.v4_gateway/archive/v3_legacy/`.

### Крок 3: Синхронізація нового Джерела Правди 4.0
Переконатися, що канонічний файл `imperia-v4-master-architecture-spec.md` розміщено у папці `.v4_gateway/docs/` (або в корені проєкту).

---

## 🧪 3. Запечатування в Git
Після переміщення файлів виконати підсумкову синхронізацію:
```bash
git add .
git commit -m "refactor(docs): archive legacy v3.0 specs to archive/v3_legacy and sync v4.0 master architecture spec"
git push origin main
```
