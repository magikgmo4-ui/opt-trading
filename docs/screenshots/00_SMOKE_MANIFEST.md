# Smoke Manifest — UI Visual Regression Baseline

Generated: 2026-05-19
Branch: sot/mainline
Server: http://127.0.0.1:8010 (modules.perf.app:app)

## HTTP Smoke — All endpoints 200

| Endpoint | HTTP | Content |
|----------|------|---------|
| /desk/ui | 200 | 18 914 bytes HTML |
| /desk/toolbox | 200 | 5 360 bytes HTML |
| /desk/health | 200 | `{"ok":true}` |
| /desk/status | 200 | 3 183 bytes JSON |
| /desk/errors | 200 | `{"ok":true,"count":0,"errors":[]}` |
| /desk/alerts | 200 | JSON destinations + state |
| /desk/logs/latest | 200 | text/plain |

## HTML Captures

| Fichier | Taille | SHA-256 |
|---------|--------|---------|
| desk_ui.html | 18 914 B | `9e6d8a913978345c0f84c3da1df47d575a11eaf3e43019ff82c87a462c2bd8af` |
| desk_toolbox.html | 5 360 B | `1d099aeb484c427567de3ea3c79af2af8ea75ede0e010ceef50b55dcd1e498c7` |
| desk_status.json | 3 183 B | live — varie selon runtime |
| desk_errors.json | 33 B | `{"ok":true,"count":0,"errors":[]}` |
| desk_health.json | 51 B | `{"ok":true,"module":"desk_pro","mode":"step2_mock"}` |

## État runtime au moment de la capture

| Check | État |
|-------|------|
| desk_pro | ok=true, mode=step2_mock |
| webhook | unreachable (port 8000 arrêté — attendu) |
| perf | ok, 7 trades fixture, equity 10540 |
| webhook_activity | warn — no events yet (attendu en dev) |
| health global | DOWN (webhook unreachable — attendu sans signal TradingView) |
| errors count | 0 |

## Note sur les captures visuelles pixel

Les captures HTML (`*.html`) sont des snapshots structurels — ils prouvent le rendu HTML mais pas l'apparence pixel.  
Pour des captures pixel, utiliser Playwright ou un navigateur headless :
```bash
python3 -m playwright screenshot http://127.0.0.1:8010/desk/ui docs/screenshots/desk_ui.png
```
(Playwright non installé dans cet environnement — captures HTML suffisantes pour la validation de structure.)

## Régression : éléments clés attendus dans desk_ui.html

Voir `GO_OPT_TRADING_UI_VISUAL_REGRESSION_SMOKE_01/10_EXPECTED_STATE_MATRIX.md`
