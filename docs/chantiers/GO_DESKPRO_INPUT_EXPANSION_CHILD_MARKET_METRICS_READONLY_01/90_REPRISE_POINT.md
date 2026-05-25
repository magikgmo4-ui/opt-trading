---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01
status: open
created_at: 2026-05-25
updated_at: 2026-05-25
---

# 90_REPRISE_POINT

## État au merge

- Branche : `go/GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01`
- Tests : **90/90 PASS** sur suites ciblées (+8 nouveaux)
- Runtime modifié : **OUI** — `dry_run.py` (non bloquant)
- Verdict : ACCEPTED

## Fichiers créés / modifiés

```text
modules/desk_pro/dry_run.py                                              ← market_metrics param + summary.market_metrics_present
tests/fixtures/admin_trading_contract_smoke/market_metrics_v1_minimal.json  ← NOUVEAU — fixture canonique
tests/test_desk_pro_dry_run.py                                           ← +5 tests
tests/test_desk_pro_market_metrics_reader.py                             ← +4 tests (fixture proof)
docs/chantiers/...                                                       ← 7 fichiers docs
docs/index/inbox/...                                                     ← inbox entry
```

## Gap parent fermé

```text
GO_DESKPRO_INPUT_EXPANSION_01 / 40_GAPS : "market_metrics absent — scoring incomplet"
→ FERMÉ — read-only + fixture proof
```

## Gaps restants dans GO_DESKPRO_INPUT_EXPANSION_01

```text
vision_analysis.v1    — dépend survivant canonique vision/headless
telegram_claim.v1     — dépend registry channels Telegram
refs/timestamps       — producers doivent remplir refs
```

## Prochaine étape

```text
PF_DESK_PRO  : GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01
PF_DATA_CENTER : GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01
```
