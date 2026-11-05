# 🏛️ DIRECTIVE: Initializing Imperia v4 Python Math Engine Core

- **Target Role:** Local Senior Python Engineer / System Architect
- **Context Baseline:** `SYSTEM_ENVIRONMENT.md`, `MEDIA_AND_MATH_ENGINE_SPEC.md`, `ARCHITECTURE_DECISIONS.md`
- **Output Target:** `core/math_engine/`
- **Execution Mode:** Isolated Atomic Refactoring & Mandatory Pre-Commit Validation

---

## 📐 1. Мета Завдання
Створити модульний каркас Математичного Ядра Imperia v4 у каталозі `core/math_engine/`. Модулі повинні забезпечувати геопросторову H3-деталізацію, розрахунок добротності $Q$-фактора, обчислення 4D-вектора середовища $\vec{E}$ та хвильові інваріанти 6D просторово-часової фізики.

---

## 📁 2. Цільова Структура Файлів
Створити наступні компоненти у `core/math_engine/`:
1. `__init__.py` — фасадна точка входу ядра.
2. `h3_grid.py` — модуль просторової кластеризації та H3-індексації.
3. `coherence_q.py` — модуль розрахунку $Q$-фактора та ефективної потужності $P_{eff}$.
4. `vectors_e.py` — модуль 4D-вектора середовища $\vec{E}$.
5. `wave_physics.py` — модуль 6D фізики $(3L, 3T)$, Джиттербагу та фазового затягування.
6. `test_engine.py` — скрипт модульного тестування.

---

## ⚙️ 3. Специфікація Модулів

### 🔹 `h3_grid.py`
- Використовуй стандартизовану бібліотеку `h3`.
- Реалізуй мапінг між октавами масштабно-частотної осі $M-f$ ($M_0 \dots M_6$) та деталізацією Uber H3 (від H3 Res 15 до H3 Res 0).
- Створи функцію `latlng_to_h3(lat: float, lng: float, resolution: int) -> str`.

### 🔹 `coherence_q.py`
- Реалізуй розрахунок $Q$-фактора за диференційним рівнянням:
  $$\frac{dQ}{dt} = \alpha \cdot (Q_{target} - Q) - \beta \cdot Jitter + \gamma \cdot Feedback$$
- Додай класифікацію зон когерентності: Зелена ($Q \ge 0.90$), Жовта ($0.75 \le Q < 0.90$), Червона ($Q < 0.75$).
- Реалізуй розрахунок ефективної потужності поля: $P_{eff} = \|\vec{E}\| \times Q$.

### 🔹 `vectors_e.py`
- Створи структуру 4D-вектора $\vec{E} = [E_{lang}, E_{geo}, E_{hist}, E_{soc}]^T$ із нормалізацією компонент у $[0.0, 1.0]$.
- Надай функцію обчислення норми $\|\vec{E}\|$.
- Створи реєстр канонічних регіональних хабів (Київ, Львів, Одеса, Харків, Дніпро).

### 🔹 `wave_physics.py`
- Реалізуй обчислення 6D інваріанта потужності $[L^5 T^{-5}] = \text{Const}$.
- Реалізуй функцію траєкторії кута повороту Джиттербагу Фуллера $\theta \in [0^\circ, 70.53^\circ]$ між Out-Wave (Кубоктаедр) та In-Wave (Тетраедр).
- Реалізуй рівняння Адлера для фазового затягування: $\frac{d(\Delta \phi)}{dt} = \Delta \omega - K \sin(\Delta \phi)$.

---

## 🧪 4. Валідація та Контроль Якості
1. Використовуй виключно open-source пакети (`h3`, `numpy`, `scipy`).
2. Проведи перевірку синтаксису: `python -m py_compile core/math_engine/*.py`.
3. Запусти тестування: `python core/math_engine/test_engine.py`.
4. Запечатай репозиторій:
   ```bash
   git add .
   git commit -m "feat(math_engine): initialize Python core mathematical modules via gateway directive"
   git push origin main
   ```
