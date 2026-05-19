# ROADMAP — Magikgmo Trading Infra (annoté)

Note : ce document est un backlog/roadmap historique. Les mentions “Done” ne doivent pas être interprétées comme une preuve de déploiement live ; se référer à `docs/master_pack/00_current_state_and_standards.md` pour l’état canonique versionné.
Pour le statut “kanban / source of truth” des chantiers : `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`.

## Priorités (ordre recommandé)
1) Docs (L0) → 2) Accès Windows/LAN (L2) → 3) Ops (L1) → 4) Schémas (L3) → 5) Risk (L4) → 6) Engines (L5) → 7) CI (L7) → 8) Exécution (L6)

## L0 — Docs (obligatoire)
- README MAIN, INDEX, ROADMAP, RUNBOOK, API, SCHEMAS
**À confirmer:** quickstart reproductible + navigation claire.

## L1 — Robustesse Ops
- services systemd, logrotate, endpoints health
**À confirmer:** reboot machine → services up.

## L2 — Réseau & Access Windows
- bind `0.0.0.0`, firewall LAN, doc de test depuis Windows
**À confirmer:** `/dash` + `/perf/ui` accessibles depuis Windows via IP LAN.

## L3 — Schéma unique Event → Trade → Perf
- JSON Schema + conventions ID/ts
- adaptateur clair `webhook_event → perf_event`
**À confirmer:** OPEN/CLOSE via webhook peut alimenter perf de manière déterministe.

## L4 — Risk Engine central
- un module `risk.py` (qty, risk_usd, steps, garde-fous)
**À confirmer:** pas de logique risk dispersée.

## L5 — Moteurs (plugins)
- `engines/` + registry + router
**À confirmer:** ajout d’un engine = 1 fichier + enregistrement.

## L7 — Qualité/CI
- lint + smoke tests + GitHub Actions
**À confirmer:** tests passent automatiquement.

## L6 — Exécution (plus tard)
- paper trading → live sous flags + kill switch
