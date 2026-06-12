---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_BACKFILL_DISCOVERY_01
doc_type: candidate_inventory
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 20_STRATEGY_CANDIDATE_INVENTORY

## Inventaire des candidats stratégies

---

## 1_DÉJÀ REGISTRÉES

| # | strategy_id | Version | Lifecycle | Surfaces |
|---|---|---|---|---|
| 1 | `SMC_ICT_CHOCH_BOS_RETEST` | 0.1.0 | CANDIDATE | doc-only |
| 2 | `xau_session_open_v1` | v0.1.0 | CANDIDATE/ACTIVE | runtime, lab, profile |

---

## 2_CANDIDATS_IDENTIFIÉS

### 2.1_Engine Enum → Stratégies potentielles

Ces 3 engines `decision_engine/app/strategy_logic.py` ont une logique propre :

| Candidat | Fichier | Logique existante | Classification |
|---|---|---|---|
| `COINM_SHORT` | `strategy_logic.py:125,198` | Short BTC COIN-M | `STRATEGY_CANDIDATE` |
| `USDTM_LONG` | `strategy_logic.py:157,200` | Long USDT-M | `STRATEGY_CANDIDATE` |
| `GOLD_CFD_LONG` | `strategy_logic.py:183,199` | Long XAU CFD | `STRATEGY_CANDIDATE` |

Ces trois candidats ont du code de logique strat, des entrées dans le
registry engines, et pourraient être promus comme `strategy_id` avec
un spec minimal.

### 2.2_Concepts documentés

| Candidat | Source | Contenu | Classification |
|---|---|---|---|
| `range_strategy_v1` | `GO_RANGE_STRATEGY_V1_STRUCT_01` | Cadrage AUD/NZD, USD/CHF, XAUUSD | `STRATEGY_CANDIDATE` |
| `btc_coinm_accumulation` | `GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01` | DCA accumulation + COIN-M shorts | `STRATEGY_CANDIDATE` |

### 2.3_Engines techniques (pas des stratégies)

| Valeur | Source | Raison |
|---|---|---|
| `TV_TEST` | `registry.py:60` | Engine de test uniquement |
| `NGROK_TEST` | `registry.py:61` | Engine de test réseau |
| `PAPER_TEST` | `registry.py:62` | Mode paper général |
| `ECHO_TEST` | `registry.py:46` | Validation dummy |
| `DESK_PRO_TIMER` | Desk Pro automation | Trigger technique |
| `FIXTURE_SEED` | `tools/perf/` | Fixture de seed |
| `BITGET_SM_LITE` | Simex bridge | Bridge technique |
| `TV_TEST` | `tools/emit_tv_payload.py` | Payload test |

### 2.4_Profils / Variants (pas des stratégies)

| Valeur | Classification |
|---|---|
| `xauusd_dual_stack_v1` (profile_id) | `VARIANT_ONLY` (déjà lié à xau_session_open_v1) |
| 4 variants `xau_open_*` | `VARIANT_ONLY` (déjà liés) |
| `e2e_dry_run` (test pipeline) | `TEST_ONLY` |

### 2.5_Concepts non trouvés

Les candidats suivants de l'hypothèse initiale n'ont **aucune référence**
dans le repo :

| Candidat | Résultat |
|---|---|
| `XAU_M5_SCALP` | **Introuvable** |
| Brent macro / squeeze | **Introuvable** |
| Copy-trading | **Introuvable** |
| Latency / anticipation (comme stratégie) | **Introuvable** (concept mentionné dans roadmap) |
| DNA supercycle (comme stratégie) | **Introuvable** (macro thesis doc only) |
| DXY (comme stratégie) | **Introuvable** (placeholder métrique Desk Pro) |
| Watchlist IA (comme stratégie) | **Introuvable** (dataset layer stock universe) |

---

## 3_RÉSUMÉ_QUANTITATIF

| Catégorie | Nombre |
|---|---|
| Déjà registrées | 2 |
| Candidats `STRATEGY_CANDIDATE` | 5 |
| `ENGINE_ONLY` | 8 |
| `VARIANT_ONLY` | 5 |
| `TEST_ONLY` | 10+ |
| `WORKFLOW_ONLY` | 0 |
| `META_STRATEGY` | 1 (supercycle thesis) |
| Non trouvés (hypothèse infirmée) | 6 |

## RISKS

- À qualifier.
