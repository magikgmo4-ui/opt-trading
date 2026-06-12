# INDEX — OT / TRADING

## RÔLE

Ce fichier est le point d’entrée local de `docs/ot/trading/`.

## DOCUMENTS CANONIQUES ACTUELS

- `docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`
- `docs/ot/trading/01_GO_OT_TRADING_DUAL_STACK_V1_01_REPRISE.md`
- `docs/ot/trading/02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`
- `docs/ot/trading/03_TRADING_LAB_V1_SCHEMA_MATERIALIZATION_01.md`
- `docs/ot/trading/04_TRADING_LAB_V1_SKELETON_01.md`
- `docs/ot/trading/05_TRADING_LAB_V1_FIRST_RUNNER_PASS_01.md`
- `docs/ot/trading/06_TRADING_LAB_V1_MARKET_INPUT_PASS_01.md`
- `docs/ot/trading/07_TRADING_LAB_V1_FEATURE_ENGINE_PASS_01.md`
- `docs/ot/trading/08_TRADING_LAB_V1_BATCH_PASS_01.md`
- `docs/ot/trading/09_TRADING_LAB_V1_BATCH_REPORTING_PASS_01.md`
- `docs/ot/trading/10_TRADING_LAB_V1_REPORT_EXPORT_PASS_01.md`
- `docs/ot/trading/11_TRADING_LAB_V1_COMPARATOR_PASS_01.md`
- `docs/ot/trading/12_TRADING_LAB_V1_LIVE_OBSERVATION_PASS_01.md`
- `docs/ot/trading/13_TRADING_LAB_V1_LIVE_EXPORT_PASS_01.md`

## SCHÉMAS MACHINE-LISIBLES

- `docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml`
- `docs/ot/trading/schemas/trading_event_v1.schema.json`
- `docs/ot/trading/schemas/trading_trade_v1.schema.json`

## MODULES LIÉS

- `modules/trading_lab_v1/` : runner LAB, exporteur LAB, comparateur, live observation, live export, samples et scripts.

## ÉTAT ACTUEL

### Établi
- dual stack Lab + Real-Time cadré ;
- focus V1 = `XAUUSD`, timezone `America/Montreal`, fenêtres `18:00` et `00:00` ;
- schémas V1 matérialisés ;
- squelette LAB V1 posé ;
- runner LAB posé ;
- input marché LAB posé ;
- feature engine LAB posé ;
- batch LAB posé ;
- batch reporting LAB posé ;
- report export LAB posé ;
- comparator LAB/LIVE posé ;
- live observation posée ;
- live export posé.

### Non encore matérialisé ici
- runner REAL-TIME natif.

## ORDRE DE LECTURE RECOMMANDÉ

1. `00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`
2. `01_GO_OT_TRADING_DUAL_STACK_V1_01_REPRISE.md`
3. `02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`
4. `03_TRADING_LAB_V1_SCHEMA_MATERIALIZATION_01.md`
5. `04_TRADING_LAB_V1_SKELETON_01.md`
6. `05_TRADING_LAB_V1_FIRST_RUNNER_PASS_01.md`
7. `06_TRADING_LAB_V1_MARKET_INPUT_PASS_01.md`
8. `07_TRADING_LAB_V1_FEATURE_ENGINE_PASS_01.md`
9. `08_TRADING_LAB_V1_BATCH_PASS_01.md`
10. `09_TRADING_LAB_V1_BATCH_REPORTING_PASS_01.md`
11. `10_TRADING_LAB_V1_REPORT_EXPORT_PASS_01.md`
12. `11_TRADING_LAB_V1_COMPARATOR_PASS_01.md`
13. `12_TRADING_LAB_V1_LIVE_OBSERVATION_PASS_01.md`
14. `13_TRADING_LAB_V1_LIVE_EXPORT_PASS_01.md`

## POINT DE REPRISE COURT

Trigger courant clos : `GO_OT_TRADING_LAB_V1_LIVE_EXPORT_PASS_01`

Trigger naturel suivant : `GO_OT_TRADING_REALTIME_V1_SKELETON_PASS_01`

## RISKS

- À qualifier.
