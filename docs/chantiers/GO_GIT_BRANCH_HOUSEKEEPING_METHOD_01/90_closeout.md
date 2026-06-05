---
doc_id: OPT_TRADING_GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01_CLOSEOUT
doc_type: closeout
repo: opt-trading
project: opt-trading
go_id: GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01
status: pass
lifecycle_stage: closeout
topic_keys:
  - git
  - branches
  - housekeeping
  - governance
  - skill
surface: chantier
source_kind: canonical
updated_at: 2026-04-17
links:
  - docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/00_cadrage.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_branch_trunk_cross_audit_target.md
  - docs/index/GO_INDEX.md
---

# GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01 — closeout

## ETABLI

- la méthode récurrente de ménage des branches Git est désormais figée dans `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- la méthode est explicitement rattachée à la convergence canonique `branches ↔ trunk`
- le tri standard retenu est `DELETE_NOW / KEEP / REVIEW`
- la suppression automatique est interdite pour les familles sensibles (`audit/*`, `inventory/*`, `integ/*`, `save/*`, `GO_*`, branches encore citées par la doc canonique)
- la frontière est figée : **doc canonique d’abord, Skill ensuite**

## TODO

- lancer un audit réel des branches quand le chantier de ménage effectif sera ouvert
- produire un tableau décisionnel branche par branche
- supprimer seulement le lot `DELETE_NOW` validé
- journaliser les suppressions réelles dans le support adapté

## REPRISE

Point de reprise unique :
- `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`

Règle de reprise :
- ne plus redéfinir la méthode depuis une session
- repartir du repo, de l’état Git réel, puis de la fiche de gouvernance

## MEM_CANDIDATE

NO_MEMORY — la règle est maintenant ancrée dans le repo et n’a plus besoin d’être portée par la session.

## Verdict

PASS — méthode canonique figée et sortie de la session.

## RISKS

- À qualifier.
