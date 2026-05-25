---
doc_id: GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01_INITIAL_PROJECT_DOC
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - journal
  - consolidation
  - family
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_consolidation_targets_and_go_list.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/17_CURRENT_BASELINE_CANONIZATION.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv
  - docs/governance/REPO_ROOT_POLICY.md
---

# 00_INITIAL_PROJECT_DOC

## Objet

Clarifier la famille `journal` entre :

- une ancienne surface operateur `journal_de_bord`
- un moteur `journal_engine`

et fixer si la famille releve encore d'une dualite vivante, ou si l'etat courant est deja tranche par retrait de la surface historique.

## Dependances verifiees

- `GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01` est committe
- `GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01` est committe
- la branche courante est rebasee sur `origin/sot/mainline`
- `secrets/` reste hors perimetre et ne doit pas etre touche

## Perimetre cible

- `modules/journal_de_bord`
- `modules/journal_engine`

## Constat d'entree

Le module `modules/journal_de_bord/` n'est pas present dans le checkout courant.

Les sources canoniques recentes indiquent au contraire qu'il a deja ete retire comme outillage obsolete.

Le GO doit donc :

- confirmer si cette absence suffit pour trancher la famille
- documenter la divergence entre l'audit historique et l'etat repo courant
- eviter toute reouverture artificielle d'une surface deja retiree

## Sources lues

- `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/17_CURRENT_BASELINE_CANONIZATION.md`
- `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv`
- `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md`
- `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_consolidation_targets_and_go_list.md`
- `docs/governance/REPO_ROOT_POLICY.md`
- `modules/journal_engine/README.md`
- `modules/journal_engine/app/journal_engine.py`

## Questions a trancher

1. Quels callers pointent vers `journal_de_bord` ?
2. Quels callers pointent vers `journal_engine` ?
3. `journal_de_bord` est-il surface operateur canonique ?
4. `journal_engine` est-il moteur actif ou historique ?
5. Les deux sont-ils complementaires ?
6. Quelle action registry est necessaire ?
7. Quel GO physique/runtime serait requis ensuite ?

## Contraintes appliquees

- mode `doc-only`
- aucune suppression
- aucun refactor runtime
- aucune mutation registry
- aucun index global ajoute
- machine_owner: `admin-trading`
