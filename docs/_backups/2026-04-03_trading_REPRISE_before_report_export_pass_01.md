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
- premier runner LAB posé ;
- première passe input marché LAB posée ;
- première passe feature engine LAB posée ;
- première passe batch LAB posée ;
- première passe batch reporting LAB posée.

## COUVERT
- schéma commun ;
- config V1 ;
- schéma event V1 ;
- schéma trade V1 ;
- squelette LAB V1 ;
- premier runner LAB ;
- input marché LAB ;
- feature engine LAB et `features_v1.jsonl` ;
- batch LAB et `batch_runs_v1.jsonl` ;
- batch reporting LAB et `batch_reports_v1.jsonl`.

## SUITE
Suite recommandée immédiate : ouvrir une passe **report export** pour produire un rendu ou un export plus lisible à partir des rapports batch.

## TRIGGER NATUREL SUIVANT
`GO_OT_TRADING_LAB_V1_REPORT_EXPORT_PASS_01`

## FORMULE COURTE
Reprendre depuis les docs `docs/ot/trading/`, les fichiers `schemas/`, puis `modules/trading_lab_v1/`, et ouvrir la passe report export LAB avant toute implémentation REAL-TIME.

## RISKS

- À qualifier.
