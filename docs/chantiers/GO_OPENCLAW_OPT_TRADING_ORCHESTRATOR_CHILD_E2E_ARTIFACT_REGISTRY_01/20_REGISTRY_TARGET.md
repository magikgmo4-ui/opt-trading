---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01_TARGET
doc_type: registry_target
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01
status: DONE
created_at: 2026-05-26
---

# 20_REGISTRY_TARGET

## Implémentation

### `scripts/e2e/register_e2e_bundle.py`

| Symbole | Rôle |
|---------|------|
| `RegistryRefused(Exception)` | refus de sécurité |
| `_validate_manifest(manifest)` | dry_run, live_trade, gate_status, run_id, go_id |
| `_check_duplicate(run_id, registry)` | déduplication par run_id |
| `_sha256_file(path)` | empreinte SHA-256 d'un fichier |
| `_get_git_sha()` | `git rev-parse HEAD` (12 chars) |
| `_build_entry(bundle_dir, manifest, registry)` | construit le dict d'entrée |
| `register_bundle(bundle_dir, registry)` | validation + écriture JSONL |
| `list_registry(registry)` | lecture liste depuis JSONL |
| `main()` | CLI : subcommands `register` et `list` |

### CLI

```bash
# Enregistrer un bundle
python3 scripts/e2e/register_e2e_bundle.py register \
  --bundle-dir data/e2e_report_bundles/20260526_120000

# Enregistrer avec registre custom
python3 scripts/e2e/register_e2e_bundle.py register \
  --bundle-dir data/e2e_report_bundles/20260526_120000 \
  --registry artifacts/e2e_artifact_registry/e2e_artifact_registry.jsonl

# Lister tous les bundles enregistrés
python3 scripts/e2e/register_e2e_bundle.py list

# Pipeline complet : build + register
ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/build_e2e_report_bundle.py \
  --run-id my_run_001
python3 scripts/e2e/register_e2e_bundle.py register \
  --bundle-dir data/e2e_report_bundles/my_run_001
```

### Registry file

- Path : `artifacts/e2e_artifact_registry/e2e_artifact_registry.jsonl`
- Format : JSONL append-only (une entrée par ligne)
- Committé dans git (métadonnées seulement, pas le contenu bundle)
- `artifacts/e2e_artifact_registry/.gitkeep` assure le tracking du répertoire vide
