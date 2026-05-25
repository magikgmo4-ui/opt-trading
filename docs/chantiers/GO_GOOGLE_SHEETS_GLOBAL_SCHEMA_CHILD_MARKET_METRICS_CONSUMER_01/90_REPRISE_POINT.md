---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 90_REPRISE_POINT — Point de reprise

## État livré

| Fichier | Status |
|---|---|
| `modules/google_sheets_global_schema/market_metrics_consumer.py` | CRÉÉ |
| `tests/test_google_sheets_market_metrics_consumer.py` | CRÉÉ — 21 tests PASS |
| `docs/chantiers/GO_.../00_INITIAL_PROJECT_DOC.md` | CRÉÉ |
| `docs/chantiers/GO_.../10_EXISTING_SURFACE_READ.md` | CRÉÉ |
| `docs/chantiers/GO_.../20_MARKET_METRICS_CONSUMER_TARGET.md` | CRÉÉ |
| `docs/chantiers/GO_.../30_FAKE_CLIENT_PROOF.md` | CRÉÉ |
| `docs/chantiers/GO_.../40_GAPS_AND_NEXT_GO.md` | CRÉÉ |
| `docs/chantiers/GO_.../90_REPRISE_POINT.md` | CE FICHIER |
| `docs/index/inbox/GO_...01.md` | CRÉÉ |
| `FILE_SCOPE.txt` | CRÉÉ |

## Validation locale

```bash
python3 -m pytest tests/test_google_sheets_market_metrics_consumer.py -v
# 21 tests PASS, 0 FAIL

python3 -m pytest tests/test_google_sheets*.py -q
# 103 tests PASS, 0 FAIL
```

## Commande de reprise

```bash
python3 -c "
import json, tempfile
from pathlib import Path
from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
from modules.google_sheets_global_schema.sheets_writer import SheetsWriter
from modules.google_sheets_global_schema.market_metrics_consumer import write_market_metrics_to_sheets

payload = {
    'input_class': 'market_metrics.v1',
    'symbol': 'BTCUSDT',
    'metrics_ts': '2026-05-25T09:00:00Z',
    'provider_coverage': {'collectable_metrics': ['open_interest', 'funding_rate'], 'missing_metrics': []},
    'metrics': {'open_interest': 1e10, 'funding_rate': 0.0001},
    'provider_id': 'bitget',
    'freshness_state': 'fresh',
}
with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / 'latest.json'
    p.write_text(json.dumps(payload))
    writer = SheetsWriter(client=FakeSheetsClient())
    result = write_market_metrics_to_sheets(writer, source_path=p)
    print(result)
"
```

## Prochain GO immédiat

**GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01** ou **GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01**
