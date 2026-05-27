---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01_INBOX
doc_type: inbox_entry
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
pf_id: PF_STRATEGY_FRAMEWORK_REGISTRY
status: DONE
created_at: 2026-05-27
closed_at: 2026-05-27
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01

**Objectif** : Connecter `trading_lab_v1` à une source de données réaliste XAUUSD M1 pour couvrir les 4 variants et préparer l'activation broker réelle.

**Résultat** : PASS_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01

## Ce qui a été fait

- Audit sources: sample existant trop limité (2 dates, 1 variant uniquement)
- Ajout `modules/trading_lab_v1/data/sample_xauusd_m1_real_like.csv`: 60 lignes, 10 sessions, 6 dates, 4/4 variants, 5 bullish + 5 bearish
- Contrat CSV broker documenté: format canonique, sources compatibles, règles de placement
- Runbook complet: comment activer avec données broker réelles sans committer de données sensibles
- Run de validation: 10/10 sessions, toutes `sequence_complete=True`

## Résultats tests

| Suite | Résultat |
|---|---|
| `tests/test_strategy_adapter.py` | 27/27 PASS |
| `modules/trading_lab_v1/tests/test_strategy_id_adapter_readonly.py` | 4/4 PASS |
| `validate_strategy_registry.py` | WARNINGS (UNREGISTERED=0) |

## Décision registry

`perf_status` reste `UNMEASURED` — pas d'exits, pas de données broker réelles.

## REMAINING_GAP

Prochain GO prioritaire: implémenter le mécanisme d'exit dans `trading_lab_v1` pour enregistrer win/loss/breakeven sur données OHLCV post-entrée.

## Chantier

`docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01/`
