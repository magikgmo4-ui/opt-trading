# ROADMAP — Magikgmo Trading Infra (annoté)

## Priorités (ordre recommandé)
1) Docs (L0) → 2) Accès Windows/LAN (L2) → 3) Ops (L1) → 4) Schémas (L3) → 5) Risk (L4) → 6) Engines (L5) → 7) CI (L7) → 8) Exécution (L6)

## L0 — Docs (obligatoire)
- README MAIN, INDEX, ROADMAP, RUNBOOK, API, SCHEMAS
**Done:** quickstart reproductible + navigation claire.

## L1 — Robustesse Ops
- services systemd, logrotate, endpoints health
**Done:** reboot machine → services up.

## L2 — Réseau & Access Windows
- bind `0.0.0.0`, firewall LAN, doc de test depuis Windows
**Done:** `/dash` + `/perf/ui` accessibles depuis Windows via IP LAN.

## L3 — Schéma unique Event → Trade → Perf
- JSON Schema + conventions ID/ts
- adaptateur clair `webhook_event → perf_event`
**Done:** OPEN/CLOSE via webhook peut alimenter perf de manière déterministe.

## L4 — Risk Engine central
- un module `risk.py` (qty, risk_usd, steps, garde-fous)
**Done:** pas de logique risk dispersée.

## L5 — Moteurs (plugins)
- `engines/` + registry + router
**Done:** ajout d’un engine = 1 fichier + enregistrement.

## L7 — Qualité/CI
- lint + smoke tests + GitHub Actions
**Done:** tests passent automatiquement.

## L6 — Exécution (plus tard)
- paper trading → live sous flags + kill switch
