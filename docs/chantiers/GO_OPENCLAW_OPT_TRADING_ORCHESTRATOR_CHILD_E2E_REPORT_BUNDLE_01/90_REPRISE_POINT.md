---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01_REPRISE
doc_type: reprise_point
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01
status: closed
created_at: 2026-05-26
---

# 90_REPRISE_POINT

## État au closeout

GO fermé. Aucun travail en suspens.

## Branche

`go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01`

## Fichiers créés

- `scripts/e2e/build_e2e_report_bundle.py` — générateur de bundle complet
- `tests/e2e/test_e2e_report_bundle.py` — 65 tests

## Fichiers modifiés

- `.gitignore` — entrée explicite `data/e2e_report_bundles/`

## Pour reproduire le bundle

```bash
# Run complet (pipeline + bundle)
ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/build_e2e_report_bundle.py

# Depuis un rapport existant
ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/build_e2e_report_bundle.py \
  --pipeline-output /path/to/e2e_report.json

# Tests
python3 -m pytest tests/e2e/test_e2e_report_bundle.py -q
```

## Invariants à maintenir

- `ALLOW_E2E_LIVE_DRY_RUN=1` + `DRY_RUN=1` requis
- `ALLOW_LIVE_TRADE`, `ALLOW_GOOGLE_SHEETS_API_WRITE`, `ALLOW_TELEGRAM_SEND` interdits
- `gate_status=APPROVED_PAPER` requis pour bundler
- `live_trade=False` requis dans le rapport
- `dry_run=True` requis dans le rapport
- `data/e2e_report_bundles/` git-ignoré
