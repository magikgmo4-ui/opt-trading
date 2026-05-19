---
doc_id: GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - governance
  - root
  - policy
surface: chantier
source_kind: canonical
updated_at: 2026-04-18
links:
  - docs/governance/REPO_ROLE.md
  - docs/ot/trae/06_REPO_BOUNDARY_POLICY_V1.txt
  - docs/INDEX.md
---

# 00_cadrage — GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01

## Classification
**patch local — doc-only — politique racine**

## Besoin initial
Fixer la politique canonique interne de la racine du repo (objets autorisés, classes, exceptions), sans refaire la frontière repo/hors-repo.

## Cible finale
- `docs/governance/REPO_ROOT_POLICY.md` comme référence de politique racine
- `docs/INDEX.md` et `docs/governance/REPO_ROLE.md` alignés

## Contraintes
- ne pas redéfinir `06_REPO_BOUNDARY_POLICY_V1`
- traiter uniquement la racine interne du repo
- documenter uniquement les changements réels

## REPRISE
Point de reprise local :
- `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/02_journal_technique.md`
