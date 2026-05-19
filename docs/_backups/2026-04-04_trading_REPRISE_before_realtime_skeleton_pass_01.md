# GO_OT_TRADING_DUAL_STACK_V1_01 — REPRISE

Date (America/Montreal) : 2026-04-03

## OBJET
Point de reprise opératoire court pour la suite du chantier trading dual stack.

## BASE
- `docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`
- `docs/ot/trading/02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`
- `docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml`
- `docs/ot/trading/schemas/trading_event_v1.schema.json`
- `docs/ot/trading/schemas/trading_trade_v1.schema.json`
- `modules/trading_lab_v1/`

## ÉTABLI
- dual stack Lab + Real-Time cadré ;
- noyau partagé exigé ;
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

## COUVERT
- schéma commun ;
- config V1 ;
- schéma event V1 ;
- schéma trade V1 ;
- squelette LAB V1 ;
- runner LAB ;
- input marché LAB ;
- feature engine LAB ;
- batch LAB ;
- batch reporting LAB ;
- report export LAB ;
- comparator LAB/LIVE ;
- live observation avec `live_observations_v1.jsonl` et `live_observation_runs_v1.jsonl` ;
- live export en `.json` et `.md` dans `state/trading_lab_v1/live_exports/`.

## SUITE
Suite recommandée immédiate : ouvrir une passe **REALTIME skeleton** pour matérialiser le vrai socle runtime sans exécution d’ordres.

## TRIGGER NATUREL SUIVANT
`GO_OT_TRADING_REALTIME_V1_SKELETON_PASS_01`

## FORMULE COURTE
Reprendre depuis les docs `docs/ot/trading/`, les fichiers `schemas/`, puis `modules/trading_lab_v1/`, et ouvrir le skeleton REALTIME avant toute exécution plus poussée.
