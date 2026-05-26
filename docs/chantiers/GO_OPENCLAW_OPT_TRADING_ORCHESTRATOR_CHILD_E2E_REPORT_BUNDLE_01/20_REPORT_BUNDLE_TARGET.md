---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01_TARGET
doc_type: bundle_target
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01
status: DONE
created_at: 2026-05-26
---

# 20_REPORT_BUNDLE_TARGET

## Implémentation

### `scripts/e2e/build_e2e_report_bundle.py`

**Constantes**

| Constante | Valeur |
|-----------|--------|
| `BUNDLE_VERSION` | `"1.0"` |
| `GO_ID` | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01` |
| `PF_ID` | `PF_OPENCLAW_ORCHESTRATOR_FULL` |
| `PARENT_GO` | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01` |
| `DEFAULT_OUTPUT_ROOT` | `data/e2e_report_bundles/` |

**Classes**

- `BundleRefused(Exception)` — levée si refus de sécurité

**Fonctions**

| Fonction | Rôle |
|----------|------|
| `_validate_env()` | vérifie les flags env requis/interdits |
| `_validate_report(report)` | vérifie live_trade, gate_status, dry_run |
| `_run_pipeline()` | lance dry_run_pipeline.py en subprocess |
| `_build_manifest(run_id, report, env_flags)` | construit manifest.json |
| `_build_payload_refs(report)` | extrait identifiants des 7 étapes |
| `_build_summary_md(run_id, manifest, payload_refs)` | génère summary.md |
| `write_bundle(report, env_flags, output_root, run_id)` | écrit les 5 fichiers |
| `build_bundle(pipeline_output_path, output_root, run_id)` | orchestrateur principal |
| `main()` | CLI entry point |

**CLI**

```bash
ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/build_e2e_report_bundle.py
ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/build_e2e_report_bundle.py \
  --pipeline-output /path/to/e2e_report.json \
  --output-root /tmp/bundles \
  --run-id custom_run_001
```

**Sortie JSON nominale**

```json
{
  "status": "BUNDLED",
  "bundle_dir": "data/e2e_report_bundles/20260526_120000",
  "run_id": "20260526_120000",
  "verdict": "PASS",
  "gate_status": "APPROVED_PAPER",
  "dry_run": true,
  "live_trade": false,
  "modules": { ... }
}
```
