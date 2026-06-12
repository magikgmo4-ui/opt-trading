---
doc_id: GO_SPACEX_TV_AUTOMATION_MAX_01_INITIAL
doc_type: initial_project_doc
go_id: GO_SPACEX_TV_AUTOMATION_MAX_01
status: draft
created_at: 2026-06-12
---

# GO_SPACEX_TV_AUTOMATION_MAX_01

## [7_CANONICAL_STATE]

TradingView SPCX webhook infrastructure complete:
- Cloudflare tunnel → admin-trading:8000
- /tv/spacex endpoint active
- Alert #4917725195 live on BATS:SPCX
- DOM extraction: Yahoo price + TV OHLCV without OCR

## Deliverables

- `configs/tradingview/spacex_tv_targets.yaml` — source of truth
- `pine_factory/spacex_ipo_master_v1.pine` — 13 alert conditions
- `scripts/ipo/spacex_tv_reconcile.py` — drift detection + job generation
- `jobs/spacex/generated/*.json` — auto-generated alert.create jobs

## Usage

```bash
# Read-only drift check
python3 scripts/ipo/spacex_tv_reconcile.py --dry-run

# Generate missing alert jobs (review required)
python3 scripts/ipo/spacex_tv_reconcile.py --apply --gate-approved

# Run generated jobs via CDP on cursor-ai
for j in modules/tradingview_orchestrator/jobs/spacex/generated/*.json; do
  modules/tradingview_orchestrator/scripts/cmd.sh run "$j" --dry-run
done
```
