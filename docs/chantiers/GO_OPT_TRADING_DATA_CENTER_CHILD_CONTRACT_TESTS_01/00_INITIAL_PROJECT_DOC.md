---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: CONTRACT_TESTS_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
topic_keys:
  - opt-trading
  - data_center
  - contract_tests
  - smoke_tests
  - registry_alignment
  - writer_chain
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_STORAGE_RECONCILE_01/00_INITIAL_PROJECT_DOC.md
  - modules/data_center/tests/test_contract_tests.py
  - modules/data_center/registry/producers.json
  - modules/data_center/registry/consumers.json
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01

## Objet

Valider par tests smoke la chaîne complète :

```
producer registry → market_metrics_writer → data/data_center/ → consumer registry → Desk Pro
```

Aucun appel API externe, aucune DB, aucun Telegram. Tests contractuels uniquement.

## 1_MASTER_TARGET

*(hérité)* Data Center opérationnel : rule `producer <> registry data <> consumer`.

## 6_FINAL_TARGET

28 tests contract passent en CI sur la chaîne :

1. `producers.json` auto-consistent (unicité, coverage_status, full→empty missing_metrics, 4-part output_path_root)
2. `consumers.json` auto-consistent (unicité, fallback valide, impl_status valide, migration_needed→read_path_current)
3. Alignement cross-registry (consumer.contract_class ∈ producer.contract_class, au moins un consumer par famille, aucun consumer ne lit depuis raw/)
4. Writer → DC paths (chemin écrit = registry output_path_root, Binance ≠ Bitget, full coverage dans le fichier)
5. Chain end-to-end (publish_market_metrics + Desk Pro reader trouve les métriques, validate() passe, graceful degradation)

## 7_CANONICAL_STATE — après livraison

### `modules/data_center/tests/test_contract_tests.py`

| Classe | Tests | Couvre |
|---|---|---|
| `TestProducerRegistryConsistency` | 8 | Intégrité producers.json |
| `TestConsumerRegistryConsistency` | 8 | Intégrité consumers.json |
| `TestRegistryAlignment` | 4 | Cohérence croisée producer ↔ consumer |
| `TestWriterToDataCenterChain` | 5 | Writer → DC paths + contenu |
| `TestDeskProChain` | 3 | Chain end-to-end smoke |
| **Total** | **28** | |

### Correction apportée

`test_consumer_read_path_is_reachable_after_write` : utilisait `str.lstrip()` (strip caractères, pas préfixe) et le mauvais provider (binance vs read_path bitget). Corrigé : provider `bitget` + `td / desk_pro["read_path"]`.

## 11_KEY_DECISIONS

- Tests smoke uniquement — pas d'intégration live, pas de fixtures externes.
- Aucune modification des modules testés (writer, layout, registries).
- `TestDeskProChain` importe `read_market_metrics` depuis `modules.desk_pro.service.market_metrics_reader` — ce module existait déjà.

## 12_INVARIANTS

- Aucun appel API externe.
- Aucune modification de `market_metrics_writer.py`, `layout.py`, ni des registries.
- Tests existants (42 writer + 11 layout = 53) non cassés.

## BUNDLE_TARGET — CONTRACT_TESTS_V1

- [x] `test_contract_tests.py` créé : 28 tests
- [x] 1 bug corrigé (lstrip + wrong provider)
- [x] 28/28 PASS
- [x] Total cumulatif : 53 + 28 = **81 PASS**
