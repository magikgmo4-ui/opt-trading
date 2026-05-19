# UI Screenshots — Storage Map

## Zones observées

### A. `desk/snapshots/`
Zone principale visible de captures marchés par actif :
- BTCUSDT.P
- ETHUSDT.P
- SOLUSDT.P
- XAUUSD

Cette zone contient de nombreuses captures `.png` horodatées.

### B. `data/desk_runs/`
Zone probable de runs / exécutions / outputs liés au desk.
À traiter comme **source métier** et non comme UI finale.

### C. `data/logs/desk_pro/`
Zone de statut / logs runtime (`latest_run_id.txt`, `latest_status.txt`).
Utile pour relier les captures à un run, mais pas adaptée à une lecture utilisateur finale.

### D. `shared/`
Zone potentielle de diffusion/export, mais pas nécessairement bonne comme archive canonique de screenshots.

## Lecture initiale
Aujourd’hui :
- les captures existent déjà en volume
- leur stockage est surtout orienté production / backend
- la relation explicite *screenshot ↔ analyse* n’est pas encore normalisée dans une surface UI dédiée

## Besoin cible
Créer plus tard une logique claire de stockage en deux niveaux :
1. **working/daily**
2. **archive/memory**
