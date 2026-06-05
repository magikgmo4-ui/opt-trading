---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01_REMAINING_GAPS
doc_type: remaining_gaps
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 50_REMAINING_GAPS - Remaining Gaps

## Gaps classés

### Upstream (non bloquants)

| Gap | Description | Severity | Status | GO dédié |
| --- | --- | --- | --- | --- |
| G-UP-01 | Playwright absent — headless capture failed à chaque trigger | HIGH | OPEN | `BOT_VISION_HEADLESS_PLAYWRIGHT_SETUP_01` |
| G-UP-02 | headless_capture en quarantaine `/tmp/opt-trading-quarantine/` | MEDIUM | DOCUMENTED | — |

### Runtime freshness (à traiter séparément)

| Gap | Description | Severity | Status | GO dédié |
| --- | --- | --- | --- | --- |
| G-RF-01 | `desk/state/latest.json` stale depuis 2026-03-03 | HIGH | OPEN | relancer `desk_state.py` |
| G-RF-02 | `desk/inputs/tv_inputs_latest.json` stale depuis 2026-03-03 | HIGH | OPEN | relancer `extract_tv_inputs.py` |
| G-RF-03 | `/shared/desk_pro/latest/` stale depuis 2026-04-04 | MEDIUM | OPEN | relancer dashboard export |

### Automation (à traiter après merge)

| Gap | Description | Severity | Status | GO dédié |
| --- | --- | --- | --- | --- |
| G-AU-01 | Desk Pro non automatisé (manuel uniquement) | MEDIUM | DOCUMENTED | `DESK_PRO_AUTOMATION_PLAN_01` |
| G-AU-02 | Pas de service systemd pour Desk Pro | LOW | DOCUMENTED | design choice |

### Integration smoke (non exécuté)

| Gap | Description | Severity | Status | GO dédié |
| --- | --- | --- | --- | --- |
| G-IS-01 | Smoke runtime réel non exécuté | MEDIUM | DOCUMENTED | `LIVE_RUNTIME_SMOKE_GATED_01` |
| G-IS-02 | Pas de smoke webhook → capture → Desk Pro end-to-end | MEDIUM | DOCUMENTED | `LIVE_RUNTIME_SMOKE_GATED_01` |

### Merge (décision séparée)

| Gap | Description | Severity | Status | GO dédié |
| --- | --- | --- | --- | --- |
| G-MG-01 | Merge/PR non finalisé vers `sot/mainline` | MEDIUM | OPEN | `SEQUENCE_PR_MERGE_01` |

### Symbol normalization

| Gap | Description | Severity | Status | GO dédié |
| --- | --- | --- | --- | --- |
| G-SN-01 | `BTCUSDT` (webhook) vs `BTCUSDT.P` (capture) — mismatch | MEDIUM | DOCUMENTED | adapter fix ou normalization layer |

### Enrichissement futur

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-EF-01 | `visual_context_ref` non produit par webhook | LOW | FUTURE |
| G-EF-02 | `desk_snapshot_ref` non produit par webhook | LOW | FUTURE |
| G-EF-03 | `signal_event_ref` non produit par capture | LOW | FUTURE |
| G-EF-04 | `payload_hash` non produit par visual_context | LOW | FUTURE |

## Verdict global

**Aucun gap bloquant.** Tous les gaps sont soit upstream, soit des enrichissements futurs, soit des décisions séparées (merge, automation).

## RISKS

- À qualifier.
