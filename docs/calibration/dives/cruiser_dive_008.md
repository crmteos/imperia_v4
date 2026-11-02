# Крейсерське Занурення 08: Декомпозиція UI та Просторові Дашборди

## 1. архітектура інтерфейсу

UI декомпозиція на треті рівні фільтрів:
- Кountry (країна) -> Region (регіон) -> Module (модуль)

Просторові дашборди з Leaflet.js integration:
- Full-widthLeaflet map як dominant visual center
- H3 geo-matrix module options
- Regional passport rows with 4D ecology vectors E = [E_lang, E_geo, E_hist, E_soc]^T

## 2. Каталог модулів

- Module A: Cartographic projections
- Module B: Spatial indexing (H3)
- Module C: Territory passport visualization

## 3. Інтеграція з wave_core

API endpoints для UI-данних:
- `/api/spatial-dashboard/:region`
- `/api/passport/:h3-index`