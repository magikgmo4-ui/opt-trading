# GO_OT_TRAE_CONTINUATION_DEFAULT_DECISION_01 — DÉCISION CANONIQUE (CONTINUITÉ PAR DÉFAUT)

Date (America/Montreal) : 2026-04-10

## 1. Objet
Canoniser la suite principale du plan Trae après la reprise neutre, en remplaçant le point actif `GO_OT_NEXT_MISSION_SELECTION_01` par une continuité doc-only imposée, sans ouvrir les missions ni exécuter runtime/code.

## 2. Éléments établis (contexte)
- Le chantier prioritaire Trae a été clôturé (pré‑V1, CONTRADICTOIRE, runtime/snapshot, adoption proof) et la reprise neutre `GO_OT_NEXT_MISSION_SELECTION_01` était conservée comme point actif.
- Le kanban reste la source de vérité ; les extractions de continuité ne sont que des supports secondaires.
- Le backlog post‑V1 est explicitement réservé pour après le freeze minimal V1.

## 3. Décision canonique (suite imposée)
La continuité principale Trae est désormais :
1) `GO_OT_TRAE_STARTERPACK_GATING_PROOF_01`
2) `GO_OT_TRAE_RULES_V1_OPEN_01`
3) `GO_OT_TRAE_POST_V1_BACKLOG_CADRAGE_01`

## 4. Règles d’interprétation (bornes)
- Cette décision fixe un ordre canonique de continuité ; elle ne constitue pas l’ouverture effective des 3 missions.
- La mission `GO_OT_TRAE_STARTERPACK_GATING_PROOF_01` est doc-only et vise uniquement la preuve de pratique du gating GO/STOP (sans runtime/code).
- La mission `GO_OT_TRAE_RULES_V1_OPEN_01` est une ouverture explicite V1 (Rules uniquement) ; elle ne doit pas être lancée automatiquement.
- La mission `GO_OT_TRAE_POST_V1_BACKLOG_CADRAGE_01` est réservée au post‑V1 ; elle ne doit pas être ouverte tant que le freeze minimal V1 n’est pas explicitement terminé.

## 5. Conséquences (synchronisation)
- Le point actif canoniquement affiché par le kanban devient `GO_OT_TRAE_STARTERPACK_GATING_PROOF_01`.
- La suite logique après cette mission est `GO_OT_TRAE_RULES_V1_OPEN_01`, puis `GO_OT_TRAE_POST_V1_BACKLOG_CADRAGE_01` (post‑V1).

## 6. Artefacts doc-only requis
- Décision : `docs/ot/trae/OT_TRAE_CONTINUATION_DEFAULT_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_CONTINUATION_DEFAULT_DECISION_01_CLOSING.txt`
- Alignement kanban :
  - `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
  - `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`
- Reprise de session :
  - `docs/ot/trae/OT_TRAE_SESSION_REPRISE.md`

## 7. Point de reprise
- `GO_OT_TRAE_STARTERPACK_GATING_PROOF_01`

## RISKS

- À qualifier.
