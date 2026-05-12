---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01_ROADMAP
doc_type: implementation_roadmap
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 60_IMPLEMENTATION_ROADMAP - Implementation Roadmap

## 1. `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01`

- But: implementer un runner Desk Pro dry-run base sur `desk_snapshot` + `signal_event` V1
- Fichiers probables: `modules/desk_pro*/**`, tests dry-run, docs chantier
- Tests attendus: unit tests IO + smoke local sans runtime
- Risques: stale handling, symbol normalization, format output
- Sortie: PASS si runner manuel reproductible sans side effect

## 2. `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01`

- But: specifier l'unite service/timer sans l'activer
- Fichiers probables: docs systemd, template unit files, operator notes
- Tests attendus: validation documentaire, chemins, user, cadence, rollback
- Risques: mauvais trigger, overlap runs
- Sortie: PASS si spec complete et safe

## 3. `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01`

- But: implementer les unit files et le wiring timer, sans live side effects non gates
- Fichiers probables: `scripts/**`, `systemd/**` ou equivalents, tests docs
- Tests attendus: syntaxe unit files, one-shot dry-run, no-trade guarantee
- Risques: lancer trop tot, overlap, stale loops
- Sortie: PASS si timer dry-run installe proprement

## 4. `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01`

- But: definir status output, logs, freshness metrics, traces operateur
- Fichiers probables: docs, wrappers, report schema
- Tests attendus: schema output, stale/error statuses, operator readability
- Risques: logs trop verbeux, fuite d'information
- Sortie: PASS si observabilite suffisante pour run unattended dry-run

## 5. `GO_OPT_TRADING_ADMIN_TRADING_LIVE_RUNTIME_SMOKE_GATED_01`

- But: valider en conditions reelles, explicitement gate, la chaine automatisee
- Fichiers probables: runbook, smoke evidence docs, event fixtures si besoin
- Tests attendus: preflight strict + smoke runtime reel limite
- Risques: side effects runtime, faux signaux, bruit operateur
- Sortie: PASS si smoke live confirme sans incident
