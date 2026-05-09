---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01_MERGE_PLAN
doc_type: merge_plan
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 10_MERGE_PLAN - Merge Plan

## Stratégie de merge

### Option recommandée: squash-merge séquentiel

La séquence admin-trading est une chaîne linéaire de 12 commits sur une seule branche. Le merge le plus propre est un **squash-merge** de la branche finale vers `sot/mainline`, qui regroupe tous les commits en un seul commit canonique.

### Branche source

```
go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01
```

Cette branche contient les 12 commits de la séquence complète (voir 20_BRANCH_AND_COMMIT_MAP.md).

### Branche cible

```
sot/mainline
```

### État actuel

| Métrique | Valeur |
| --- | --- |
| Commits ahead (séquence → mainline) | 12 |
| Commits behind (mainline → séquence) | 12 |
| Fichiers modifiés | 68 |
| Lignes ajoutées | ~6111 |
| Conflits attendus | AUCUN (fichiers indépendants) |

## Contenu du merge

### Fichiers code (2)

| Fichier | Type | Description |
| --- | --- | --- |
| `modules/desk_pro/signal_event_adapter.py` | Python | Adapter V0→V1 (4 fonctions) |
| `tests/test_signal_event_adapter.py` | Python | 30 tests adapter |

### Fichiers test (5)

| Fichier | Type | Description |
| --- | --- | --- |
| `tests/test_admin_trading_contract_compatibility_smoke.py` | Python | 10 smoke tests |
| `tests/fixtures/admin_trading_contract_smoke/signal_event_v0_minimal.json` | JSON | Fixture V0 |
| `tests/fixtures/admin_trading_contract_smoke/signal_event_v0_complete.json` | JSON | Fixture V0 |
| `tests/fixtures/admin_trading_contract_smoke/visual_context_v1_minimal.json` | JSON | Fixture V1 |
| `tests/fixtures/admin_trading_contract_smoke/desk_snapshot_minimal.json` | JSON | Fixture snapshot |

### Fichiers documentation (~61)

Tous sous `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_*` — documentation chantier, aucun impact runtime.

## Risques

| Risque | Probabilité | Impact | Mitigation |
| --- | --- | --- | --- |
| Conflit avec mainline | FAIBLE | LOW | fichiers indépendants (nouveaux) |
| Cassage tests existants | NULLE | — | aucun test existant modifié |
| Cassage runtime | NULLE | — | aucun fichier runtime modifié |
| Cassage imports | NULLE | — | adapter isolé, pas d'imports croisés |

## Pré-requis merge

1. ✅ Tous les GOs de la séquence: PASS
2. ✅ Tests adapter: 30/30 passed
3. ✅ Tests smoke: 40/40 passed
4. ✅ Aucun side effect runtime
5. ✅ Documentation complète
6. ⏳ PR créée et revue
7. ⏳ `GO_MERGE` explicite de l'opérateur
