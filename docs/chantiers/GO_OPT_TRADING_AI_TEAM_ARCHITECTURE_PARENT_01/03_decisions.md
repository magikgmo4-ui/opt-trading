---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01_DECISIONS
doc_type: decisions
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
status: open
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - ai_team
  - architecture
  - parent
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
point_de_reprise: "5. Point de reprise"
updated_at: 2026-04-28
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/02_journal_technique.md
---

# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 — 03_decisions

## 1. État de départ retenu

Le chantier parent est ouvert pour cadrer une architecture d’équipe d’agents spécialisée. Le besoin est documentaire et conceptuel. Aucun setup technique final n’est encore verrouillé. Le parent doit être autonome, canonique et indépendant de la session.

## 2. Décisions

- Le nom canonique du chantier parent est `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`.
- La branche dédiée de référence est `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`.
- Le set documentaire d’ouverture du parent comprend :
  - `00_cadrage.md`
  - `01_initial_project_doc.md`
  - `02_journal_technique.md`
  - `03_decisions.md`
- La fiche `01_initial_project_doc.md` est reconnue comme la fiche dédiée pour `2_INITIAL_PROJECT_DOC`.
- Le journal technique est borné au factuel exécuté uniquement.
- Le parent reste doc-only jusqu’à ouverture d’un GO enfant spécifique.

## 3. Exclusions

- aucune implémentation runtime ;
- aucune stack finale imposée ;
- aucune décision définitive de framework ;
- aucun GO enfant ouvert implicitement.

## 4. Verdict

- `PASS_DOC_OPENING_SET_COMPLETE`
- set d’ouverture parent complet, cohérent et exploitable hors session ;
- ouverture d’un GO enfant désormais autorisable sous réserve de bornage explicite du nouveau chantier.

## 5. Point de reprise

Reprendre sur la branche `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, utiliser `7_CANONICAL_STATE` comme base de continuité, puis ouvrir le premier GO enfant documentaire ou d’architecture avec bornage explicite et sans réinterpréter les hypothèses comme des faits.

## RISKS

- À qualifier.
