---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_BACKFILL_DISCOVERY_01
doc_type: classification_matrix
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 30_CLASSIFICATION_MATRIX

## Matrice de classification détaillée

---

## 1_MATRICE_COMPLÈTE

| Candidat | Code | Doc | Runtime | Registry | Classification |
|---|---|---|---|---|---|
| `SMC_ICT_CHOCH_BOS_RETEST` | Non | Oui | Non | Oui | `STRATEGY_ID_READY` |
| `xau_session_open_v1` | Oui | Oui | Oui | Oui | `STRATEGY_ID_READY` |
| `COINM_SHORT` | Oui (engine) | Non | Paper | Non | `STRATEGY_CANDIDATE` |
| `USDTM_LONG` | Oui (engine) | Non | Paper | Non | `STRATEGY_CANDIDATE` |
| `GOLD_CFD_LONG` | Oui (engine) | Non | Paper | Non | `STRATEGY_CANDIDATE` |
| `range_strategy_v1` | Non | Oui (cadrage) | Non | Non | `STRATEGY_CANDIDATE` |
| `btc_coinm_accumulation` | Non | Oui (draft) | Non | Non | `STRATEGY_CANDIDATE` |
| `TV_TEST` | Oui | Non | Test | Non | `ENGINE_ONLY` |
| `NGROK_TEST` | Oui | Non | Test | Non | `ENGINE_ONLY` |
| `PAPER_TEST` | Oui | Non | Paper | Non | `ENGINE_ONLY` |
| `ECHO_TEST` | Oui | Non | Dummy | Non | `ENGINE_ONLY` |
| `DESK_PRO_TIMER` | Oui | Non | Production | Non | `ENGINE_ONLY` |
| `FIXTURE_SEED` | Oui | Non | Outil | Non | `ENGINE_ONLY` |
| `BITGET_SM_LITE` | Oui | Non | Production | Non | `ENGINE_ONLY` |
| `xauusd_dual_stack_v1` | Oui | Oui | Oui | Non (profile) | `VARIANT_ONLY` |
| `xau_open_sweep_fvg` | Oui | Oui | Oui | Non (variant) | `VARIANT_ONLY` |
| `xau_open_no_sweep_fvg` | Oui | Oui | Oui | Non (variant) | `VARIANT_ONLY` |
| `xau_open_sweep_no_fvg` | Oui | Oui | Oui | Non (variant) | `VARIANT_ONLY` |
| `xau_open_no_sweep_no_fvg` | Oui | Oui | Oui | Non (variant) | `VARIANT_ONLY` |
| `e2e_dry_run` | Oui | Non | Test | Non | `TEST_ONLY` |
| supercycle thesis | Non | Oui | Non | Non | `META_STRATEGY` |

---

## 2_PRIORITÉS_RECOMMANDÉES

| Priorité | Candidat | Justification |
|---|---|---|
| P0 | `COINM_SHORT` | Code engine + logique `strategy_logic.py` active |
| P1 | `USDTM_LONG` | Code engine + logique `strategy_logic.py` active |
| P2 | `GOLD_CFD_LONG` | Code engine + logique `strategy_logic.py` active |
| P3 | `range_strategy_v1` | Cadrage existant, GO dédié, assets identifiés |
| P4 | `btc_coinm_accumulation` | Draft concept + child GOs dédiés |
