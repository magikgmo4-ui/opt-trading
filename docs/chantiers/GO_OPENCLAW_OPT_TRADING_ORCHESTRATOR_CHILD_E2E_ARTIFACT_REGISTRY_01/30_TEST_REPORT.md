---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01_TEST
doc_type: test_report
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01
status: DONE
created_at: 2026-05-26
---

# 30_TEST_REPORT

## Résultats

| Suite | Résultat |
|-------|----------|
| `tests/e2e/test_e2e_artifact_registry.py` (63 tests) | 63/63 PASS |
| `tests/e2e/` complet (282 tests) | 282/282 PASS |

## Classes de tests

| Classe | Tests | Couverture |
|--------|-------|------------|
| `TestModuleImport` | 2 | import + constantes |
| `TestValidateManifest` | 9 | dry_run, live_trade, gate_status, run_id, go_id |
| `TestDuplicateDetection` | 5 | déduplication, lignes malformées |
| `TestHashComputation` | 3 | sha256, déterminisme, contenu différent |
| `TestBuildEntry` | 9 | tous les champs, hashes, chemin absolu, modules |
| `TestRegisterBundle` | 13 | write, append, duplicate, refusals, registry list |
| `TestListRegistry` | 3 | vide, une entrée, deux entrées |
| `TestCLIRegister` | 6 | exit 0/1, duplicate CLI, list CLI |
| `TestBuildAndRegisterIntegration` | 13 | pipeline complet build+register |

## Commandes

```bash
python3 -m pytest tests/e2e/test_e2e_artifact_registry.py -q
python3 -m pytest tests/e2e/ -q
```
