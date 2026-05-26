---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01_INITIAL
doc_type: initial_project_doc
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: DONE
created_at: 2026-05-26
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01

## Objectif

Créer un générateur de bundle transportable `scripts/e2e/build_e2e_report_bundle.py` qui transforme
un run `dry_run_pipeline.py` en un bundle auditabl contenant 5 fichiers structurés.

## Contexte

Suite au GO précédent (GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01),
le pipeline produit maintenant un `e2e_post_gate_status` structuré. Ce GO capitalise ce résultat
en le capturant dans un bundle transportable et versionné.

## Règles de sécurité

- `ALLOW_E2E_LIVE_DRY_RUN=1` + `DRY_RUN=1` requis
- `ALLOW_LIVE_TRADE=1` interdit
- `ALLOW_GOOGLE_SHEETS_API_WRITE=1` interdit
- `ALLOW_TELEGRAM_SEND=1` interdit
- `live_trade=True` dans le rapport → refus `BundleRefused`
- `gate_status != APPROVED_PAPER` → refus
- `dry_run != True` → refus

## Structure du bundle

```
data/e2e_report_bundles/<RUN_ID>/
  manifest.json          # GO/PF metadata, run identity, verdict
  e2e_report.json        # full pipeline JSON output
  environment_flags.json # flags env utilisés
  payload_refs.json      # identifiants clés de chaque étape
  summary.md             # résumé human-readable
```

## Livrables

- `scripts/e2e/build_e2e_report_bundle.py`
- `tests/e2e/test_e2e_report_bundle.py`
- `.gitignore` — entrée explicite `data/e2e_report_bundles/`
