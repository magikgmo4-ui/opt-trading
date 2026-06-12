---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_BACKFILL_DISCOVERY_01
doc_type: discovery_method
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 10_DISCOVERY_METHOD

## Méthode de découverte

---

## 1_GREP_PATTERNS

```text
strategy_id       → occurrences explicites
profile_id        → profils de trading
variant_id        → variantes opérationnelles
setup_type        → types de setup
Engine.COINM_SHORT → enum engine ( = stratégie potentielle )
Engine.USDTM_LONG
Engine.GOLD_CFD_LONG
COINM_SHORT / USDTM_LONG / GOLD_CFD_LONG  → engine strings
XAU, XAUUSD, GOLD  → actif XAU
BTC, BTCUSDT, COINM, USDTM  → actif BTC
BRENT, BRN         → actif BRENT
SMC, ICT, CHOCH, BOS, FVG, OB  → SMC/ICT
range, accumulation, session_open, DXY, watchlist
latency, anticipation, copy-trading, supercycle
```

---

## 2_SURFACES_SCANNÉES

```text
modules/decision_engine/app/strategy_logic.py       → Engine enum
modules/engines/registry.py                          → Engine string registry
modules/trading_realtime_v1/app/*.py                 → runtime
modules/trading_lab_v1/app/*.py                      → lab
docs/ot/trading/schemas/*                            → profiles, schemas
docs/ot/trading/*.md                                 → specs, core docs
docs/chantiers/*/                                     → GO chantiers
scripts/**/*.py                                       → scripts
tools/**/*.py                                         → tools
modules/signal_router/**                              → signal pipeline
modules/proposition_engine/**                         → proposition pipeline
modules/notification_dispatcher/**                    → notification pipeline
```

---

## 3_CLASSIFICATION

Chaque candidat reçoit une étiquette :

| Label | Définition |
|---|---|
| `STRATEGY_ID_READY` | Peut être enregistré tel quel |
| `STRATEGY_CANDIDATE` | Nécessite un spec minimal |
| `ENGINE_ONLY` | Engine technique, pas une stratégie |
| `VARIANT_ONLY` | Variante d'une stratégie existante |
| `PRESET_ONLY` | Preset de simulation/test |
| `TEST_ONLY` | Valeur de test uniquement |
| `WORKFLOW_ONLY` | Checklist/workflow, pas une stratégie |
| `META_STRATEGY` | Concept macro/portefeuille |
| `REJECT_NOT_STRATEGY` | Hors scope stratégie trading |

## RISKS

- À qualifier.
