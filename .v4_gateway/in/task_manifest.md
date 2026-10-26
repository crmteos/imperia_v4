# Інструкція для ШІ-клієнта у VS Code (v4 Core Executor)

## Мета
Розгорнути ядро локального вузла **Edge SLM (Node Core)** у папці проекту `C:\imperia_v4` відповідно до декларативної специфікації `.v4_gateway/in/ARCHITECT_SPEC.json`.

---

## Принцип розробки
1. **0% антропоморфізму**: Жодних чиновників, ієрархій, ролей або інституцій у коді ядра.
2. **Stateful Context Engineering**: Контекстне вікно моделі є оперативною пам'яттю (RAM), де системний інваріант є непорушним блоком, а вектор середовища $\vec{E}$ — активним станом.
3. **P2P Edge Swarm**: Вузол працює локально та обмінюється квантами через P2P-мережу (libp2p / WebRTC).

---

## Завдання для виправлення та створення файлів (`src/`)

### 1. `src/geo/h3_vector.ts` (або `.py`)
- Реалізувати обчислення H3-індексів (Res 4, Res 7, Res 9) за координатами GPS.
- Сформувати вектор середовища $\vec{E} = [E_{geo}, E_{resource}, E_{coherence}, E_{temporal}]$.

### 2. `src/governor/resource_governor.ts` (або `.py`)
- Моніторити показники пристрою (батарея, мережа, температура).
- Реалізувати авто-перемикання режимів: `CRITICAL` (<15% battery), `BALANCED` (<30% battery), `PERFORMANCE`.

### 3. `src/context/stateful_ram.ts` (або `.py`)
- Створити менеджер контекстного вікна з лімітом 8192 токенів.
- Забезпечити строгу розділеність блоків: `invariants_block` (Read-Only), `state_block` (Read-Write), `ephemeral_queue` (FIFO).

### 4. `src/p2p/transport_adapter.ts` (або `.py`)
- Налаштувати підписку на DHT-топіки за схемою `/v4/h3/{h3_meso_res7}`.

---

## Формат звіту про виконання
Після збірки та проходження базових тестів відписати підсумковий стан у файл `.v4_gateway/out/EXECUTION_STATE.json` за наступною схемою:

```json
{
  "timestamp": 1700000000,
  "status": "SUCCESS",
  "files_created": [
    "src/geo/h3_vector.ts",
    "src/governor/resource_governor.ts",
    "src/context/stateful_ram.ts",
    "src/p2p/transport_adapter.ts"
  ],
  "tests_passed": true,
  "errors": []
}
```
