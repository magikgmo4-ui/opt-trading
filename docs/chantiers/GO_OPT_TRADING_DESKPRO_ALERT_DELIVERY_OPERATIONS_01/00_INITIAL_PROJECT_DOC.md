---
go_id: GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_OPERATIONS_01
doc_type: initial_project_doc
repo: opt-trading
status: DRAFT
created_at: 2026-05-18
---

# GO_OPT_TRADING_DESKPRO_ALERT_DELIVERY_OPERATIONS_01

## 1_MASTER_TARGET

Stabiliser l'exploitation opérationnelle réelle du pipeline d'alerte Desk Pro après merge PR #557.
Aucun nouveau code. Deliverable : runbook opérationnel complet.

## 10_SCOPE

- Documenter le lancement du serveur
- Lister les variables d'environnement requises et optionnelles
- Documenter le fallback JSONL (comportement et localisation)
- Documenter le smoke test endpoint et l'interprétation des statuts
- Runbook de diagnostic si alert non reçue
- Prouver absence de fuite de secret dans le pipeline

## 13_ESTABLISHED

- `perf/perf_app.py` monte le router Desk Pro (`/desk/*`) sur port `8010`
- `_dispatch_alert` → `_telegram_send` / `_webhook_send` — lire env à chaque appel
- Fallback JSONL : `/opt/trading/tmp/desk_pro_alerts.jsonl` — écrit uniquement sur alerte réelle (degraded/down)
- Smoke test (`POST /desk/alert/test`) ne touche pas JSONL ni `_alert_state`
- `GET /desk/status` expose `destinations.telegram` et `destinations.webhook` (bool, sans valeur)
- Tests : 107/107 PASS

## RISKS

- À qualifier.
