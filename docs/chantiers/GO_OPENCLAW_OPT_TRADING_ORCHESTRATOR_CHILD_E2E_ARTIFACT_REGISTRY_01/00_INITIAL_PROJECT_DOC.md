---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01_INITIAL
doc_type: initial_project_doc
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: DONE
created_at: 2026-05-26
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01

## Objectif

Créer un registre léger des bundles E2E générés par `build_e2e_report_bundle.py`,
sans committer les bundles eux-mêmes — seulement leurs métadonnées.

## Contexte

Les bundles E2E existent localement dans `data/e2e_report_bundles/` (gitignorés).
Sans registre, ils sont difficiles à tracer dans le temps. Ce GO crée
`artifacts/e2e_artifact_registry/e2e_artifact_registry.jsonl` — un fichier JSONL
committé, append-only, contenant les métadonnées auditables de chaque run.

## Structure d'une entrée registry

```json
{
  "registry_version": "1.0",
  "registry_go_id": "GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01",
  "run_id": "20260526_120000",
  "created_at": "...",
  "registered_at": "...",
  "verdict": "PASS",
  "e2e_status": "PASS",
  "gate_status": "APPROVED_PAPER",
  "dry_run": true,
  "live_trade": false,
  "go_id": "...",
  "pf_id": "PF_OPENCLAW_ORCHESTRATOR_FULL",
  "bundle_path": "/opt/trading/data/e2e_report_bundles/20260526_120000",
  "manifest_hash": "sha256:...",
  "summary_hash": "sha256:...",
  "git_sha": "abc1234",
  "modules": { ... },
  "duration_s": 5.0
}
```

## Règles de sécurité

- `RegistryRefused` levée si `dry_run != True`, `live_trade != False`, `gate_status != APPROVED_PAPER`
- Déduplication par `run_id` — double enregistrement refusé
- `bundle_dir` doit exister et contenir `manifest.json`

## Livrables

- `scripts/e2e/register_e2e_bundle.py` — register + list CLI
- `artifacts/e2e_artifact_registry/.gitkeep` — répertoire tracké
- `tests/e2e/test_e2e_artifact_registry.py` — 63 tests
