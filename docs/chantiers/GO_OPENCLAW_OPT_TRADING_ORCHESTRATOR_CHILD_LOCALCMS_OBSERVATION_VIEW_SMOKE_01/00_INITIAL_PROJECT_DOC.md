---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_SMOKE_01
doc_type: initial_project_doc
repo: opt-trading
status: closed
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
created_at: 2026-05-17
surface: smoke / validation
scope: GET /metrics/daily — observation block + last_run étendu
---

# 00_INITIAL_PROJECT_DOC
## GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_SMOKE_01

---

## 1_MASTER_TARGET

```text
Valider en runtime que _build_metrics() post-PR #527 expose bien
le bloc observation et les extensions last_run sur le code mergé.
```

---

## 2_CONTEXTE_ETABLI

| Fait | Valeur |
| --- | --- |
| `PR #527` | MERGED — `c62a0c0f` |
| Merge confirmé | `git log --oneline -1` = `c62a0c0f feat(localcms): expose observation Phase 1 block` |
| LocalCMS HTTP | non actif en local (normal — machine db-layer) |
| Test mode | appel direct `_build_metrics()` via Python |

---

## 3_METHODE

```bash
python3 -c "
import json, sys
sys.path.insert(0, '/opt/trading')
from modules.localcms.app.main import _build_metrics
print(json.dumps(_build_metrics(), indent=2))
"
```

Exécuté depuis `sot/mainline @ c62a0c0f` — 2026-05-17T23:21:42Z.

## RISKS

- À qualifier.
