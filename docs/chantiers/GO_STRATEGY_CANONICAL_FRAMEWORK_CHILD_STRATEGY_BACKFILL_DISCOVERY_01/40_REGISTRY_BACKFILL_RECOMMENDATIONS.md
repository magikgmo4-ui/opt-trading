---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_BACKFILL_DISCOVERY_01
doc_type: registry_backfill_recommendations
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 40_REGISTRY_BACKFILL_RECOMMENDATIONS

## Recommandations pour le backfill registry

---

## 1_RECOMMANDATION_PRINCIPALE

Créer un GO dédié pour chaque `STRATEGY_CANDIDATE` avant de les ajouter
à la registry. Ne pas backfiller automatiquement.

| Candidat | Action recommandée |
|---|---|
| `COINM_SHORT` | Ouvrir child GO avec spec minimal + audit engine → registry |
| `USDTM_LONG` | Ouvrir child GO avec spec minimal + audit engine → registry |
| `GOLD_CFD_LONG` | Ouvrir child GO avec spec minimal + audit engine → registry |
| `range_strategy_v1` | Ouvrir child GO reprenant le cadrage → registry |
| `btc_coinm_accumulation` | Ouvrir child GO si le concept est validé → registry |

---

## 2_NE_PAS_BACKFILLER

| Item | Raison |
|---|---|
| `TV_TEST`, `NGROK_TEST`, `PAPER_TEST`, `ECHO_TEST` | Engines techniques uniquement |
| `DESK_PRO_TIMER` | Trigger automation, pas stratégie |
| `FIXTURE_SEED`, `BITGET_SM_LITE` | Outillage infra |
| `xauusd_dual_stack_v1` | Profile, déjà lié à xau_session_open_v1 |
| 4 variants `xau_open_*` | Variants, déjà liés |
| `e2e_dry_run` | Pipeline test uniquement |
| `breakout_v2`, `test_v1`, `s1`, `t`, `v1`, `test` | Tests uniquement |

---

## 3_IMPACT_SUR_LE_VALIDATEUR

Après backfill, le validateur `validate_strategy_registry.py` passera de :

```text
WARNINGS=6 (test_only)
```

à (selon les GOs ouverts) :

```text
REGISTERED=5 (si les 3 engines + range + BTC sont ouverts)
```

Les 6 valeurs test-only resteront en WARNING, ce qui est correct.

## RISKS

- À qualifier.
