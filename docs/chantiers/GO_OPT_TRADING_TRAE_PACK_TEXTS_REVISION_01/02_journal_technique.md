---
doc_id: GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01_JOURNAL_TECHNIQUE
doc_type: chantier_journal_technique
repo: opt-trading
project: opt-trading
module: docs_trae
go_id: GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01
status: active
lifecycle_stage: journal_technique
topic_keys:
  - opt-trading
  - trae
  - trae_pack_texts
  - docs
  - legacy
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/03_decisions.md
---

# 02_journal_technique — GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01

## 2026-04-24
### Étape 1 — Constat repo-first
- `trae_pack_texts/` existait encore à la racine comme bibliothèque locale de textes Trae
- aucun couplage runtime direct n’a été retenu ; les références observées étaient documentaires
- le pack faisait encore partie de l’ensemble Trae/IDE, mais avec un statut asymétrique : helper legacy, non canonique

### Étape 2 — Move documentaire
- move appliqué : `trae_pack_texts/` -> `docs/ot/trae/trae_pack_texts/`
- but : sortir le pack de la racine sans le supprimer, et l’assumer explicitement comme sous-surface documentaire

### Étape 3 — Réalignement de références
- réalignement des chemins actifs et historiques vers `docs/ot/trae/trae_pack_texts/`
- réalignement des auto-références internes du pack vers le nouveau chemin

### Synthèse de lecture
- `workflow_ai/` : doctrine canonique d’exécution
- `modules/validated_prompt_factory/` : fabrique opératoire de prompts
- `deploy_module_multi_machine/` : outillage de déploiement/continuité terrain
- `docs/ot/trae/trae_pack_texts/` : couche helper legacy, utile pour Trae/IDE, mais non source de vérité

### Étape 4 — Qualification du pack
- lecture fichier par fichier du dossier `docs/ot/trae/trae_pack_texts/trae_pack/`
- constat : le contenu restant est quasi entièrement redondant avec `workflow_ai/WORKFLOW.md`, le starter pack et `docs/ot/trae/12_ORCHESTRATOR_ENTRYPOINT_V1.txt`
- choix conservateur : ne pas déplacer physiquement les `.txt` historiques pour ne pas casser les références déjà publiées dans les rapports et audits

### Étape 5 — Absorption dans le canon repo-first
- `workflow_ai/WORKFLOW.md` enrichi avec la chaîne de responsabilité, les verdicts/statuts et les attentes minimales sur preuves/rollback
- `docs/master_pack/mission_starter_pack/01_mission_template.md` renforcé avec scope autorisé, hors-scope, preuve attendue et rollback prévu
- `docs/master_pack/mission_starter_pack/00_mission_start_guide.md` réaligné sur le quatuor `workflow_ai` / `validated_prompt_factory` / `deploy_module_multi_machine` / `trae_pack_texts`

### Étape 6 — Statut final retenu pour le pack
- `docs/ot/trae/trae_pack_texts/README.md` devient l’entrée documentaire vivante du support Trae legacy
- `docs/ot/trae/trae_pack_texts/trae_pack/` est requalifié en archive de lecture
- aucune dépendance runtime prouvée de `workflow_ai`, `modules/validated_prompt_factory/` ou `deploy_module_multi_machine/` vers `trae_pack_texts/`
- les dépendances observées sont documentaires uniquement

## REPRISE
- poursuivre la qualification fichier par fichier du pack :
  - vérifier après push si le GO peut passer en closeout doc-only
  - sinon maintenir le gel : `README.md` vivant, `trae_pack/` archivé

## RISKS

- À qualifier.
