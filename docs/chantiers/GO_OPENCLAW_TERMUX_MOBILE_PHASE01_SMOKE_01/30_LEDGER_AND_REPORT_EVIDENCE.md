---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01_LEDGER_AND_REPORT_EVIDENCE
doc_type: ledger_and_report_evidence
go_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01
status: active
updated_at: 2026-05-23
---

# 30_LEDGER_AND_REPORT_EVIDENCE

## Rapports JSON (reports/ai/mobile_control/)

Les rapports suivants ont été générés lors du smoke test :

- `20260523T200302Z_status_all_9467a331.json`
- `20260523T200303Z_list-jobs_all_9fdfbbc7.json`
- `20260523T200303Z_preflight_repo-status-check_7f05d361.json`
- `20260523T200303Z_run-dry_repo-status-check_b72acae2.json`

Chaque rapport contient les métadonnées Git (`branch`, `commit`), l'action, le statut, et les données de sortie (`stdout`/`stderr`).

## Entrées Ledger (data/runtime_health/ledger/events.jsonl)

Le ledger enregistre chaque action effectuée par le wrapper sous le type d'événement `MOBILE_CONTROL`.

Exemple d'entrée pour `run-dry` :
```json
{
  "event_id": "5bacf589-3771-43d6-a3db-722184e36c5b",
  "event_type": "MOBILE_CONTROL",
  "actor_id": "mobile-control",
  "surface_id": "openclaw",
  "action": "run-dry",
  "timestamp": "2026-05-23T20:03:03.406831+00:00",
  "status": "PASS",
  "payload": {
    "action": "run-dry",
    "phase": "PHASE_01",
    "job_id": "repo-status-check",
    "evidence_path": "reports/ai/mobile_control/20260523T200303Z_run-dry_repo-status-check_b72acae2.json",
    "blocked_reason": null
  }
}
```

## Verdict Evidence

```text
LEDGER_AND_REPORTS_SYNCHRONIZED_PASS
```
