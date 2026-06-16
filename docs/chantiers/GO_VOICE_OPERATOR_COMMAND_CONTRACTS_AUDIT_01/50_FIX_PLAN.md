# 50_FIX_PLAN — Plan de correction execute

## Phase 1: Bugs P0 (main.py)

1. `_get_vision_markets()` → definir comme closure dans _handle_composite qui lit vision_analysis/by_symbol/
2. `params` → ajouter `params: dict = None` comme parametre de _handle_composite, passer depuis /voice/query
3. whats_new duplique → supprimer deuxieme definition (ligne ~2734)

## Phase 2: Enrichissement composites (main.py)

4. gold_full → lire vision_analysis OANDA:XAUUSD pour prix/trend/DXY
5. exec_summary → restructurer: 3 faits, 1 risque, 1 prochaine action
6. priorities → ajouter raison par item (score/fraicheur/impact)
7. attention → ajouter cause explicite par item
8. top_movers → ajouter market_metrics prix/variation
9. market_view → ajouter prix a spoken_text si dispo
10. btc_full → utiliser _get_vision_markets corrigee

## Phase 3: Enrichissement /read API (routes.py)

11. /read/system → ajouter data_center_contracts, data_center_status
12. /read/score → gerer BTC/XAUUSD via true_value DC views
13. /read/report → ajouter integration true_value daily

## Phase 4: Tests

14. test_intent_router_all_buttons.py
15. test_voice_command_contracts.py
16. test_voice_missing_fields.py

## Phase 5: Verification

17. syntax check + verify_all.sh
