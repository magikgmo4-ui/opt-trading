---
doc_id: GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01_CLASSIFICATION
doc_type: chantier_note
repo: opt-trading
project: opt-trading
module: naming_normalizer
go_id: GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01
status: open
lifecycle_stage: analyse
topic_keys:
  - opt-trading
  - naming
  - inventory
  - classification
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/NAMING_CANON_POLICY_01.md
point_de_reprise: "Tableau de classification"
updated_at: 2026-04-29
links:
  - modules/naming_normalizer/output/naming_audit_report.json
  - docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/02_inventory_results.md
---

# 03_classification_matrix

## Tableau de classification

| surface | path | classe | proposition | justification |
| --- | --- | --- | --- | --- |
| `go_dirs` | `docs/chantiers/GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS` | `LEGACY_TOLERE` | `GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS__MANUAL_REVIEW_REQUIRED` | lot historique ferme en suffixe `_CLOS`, conserve comme trace canonique fermee sans besoin de renommage reel immediat |
| `go_dirs` | `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01` | `LEGACY_TOLERE` | `GO_UNIFORM_CONTINUITY_HARDENING_01__MANUAL_REVIEW_REQUIRED` | famille historique fermee anterieure a la granularite naming actuelle, conservee comme heritage stable |
| `go_dirs` | `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02` | `LEGACY_TOLERE` | `GO_UNIFORM_CONTINUITY_HARDENING_02__MANUAL_REVIEW_REQUIRED` | meme rationale que le lot frere `_01`, heritage conserve sans lot de correction |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_BRANCH_ARBITRATION_DELETE_AND_BRANCH_STATE_03/delete_branches.ps1` | `REFERENCE_ONLY` | `delete_branches.ps1` | script de preuve loge dans un dossier chantier historique ; support de trace, pas document canonique a renommer dans ce lot |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_BRANCH_ARBITRATION_DELETE_AND_BRANCH_STATE_03/delete_results.txt` | `REFERENCE_ONLY` | `delete_results.txt` | resultat de suppression historise, conserve comme piece de preuve |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_BRANCH_ARBITRATION_DELETE_AND_BRANCH_STATE_03/remote_delete_final_status.txt` | `REFERENCE_ONLY` | `remote_delete_final_status.txt` | piece de preuve de statut distant, usage reference seulement |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_BRANCH_ARBITRATION_DELETE_AND_BRANCH_STATE_03/status_before_closeout.txt` | `REFERENCE_ONLY` | `status_before_closeout.txt` | snapshot de verification avant closeout, hors besoin de renommer |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/06_registry_derived_pilot.yaml` | `REFERENCE_ONLY` | `06_registry_derived_pilot.yaml` | artefact pilote derive historise dans un lot ferme, conserve pour reference |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/08_registry_derived_pilot_delta.yaml` | `REFERENCE_ONLY` | `08_registry_derived_pilot_delta.yaml` | artefact delta derive, conserve comme reference d'audit |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_POST_ALIGNMENT_VERIFY_04/local_go_opt_trading_branches_post_alignment.txt` | `REFERENCE_ONLY` | `local_go_opt_trading_branches_post_alignment.txt` | export de verification locale, hors canon de nommage des docs ordonnees |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_POST_ALIGNMENT_VERIFY_04/remote_go_opt_trading_branches_post_alignment.txt` | `REFERENCE_ONLY` | `remote_go_opt_trading_branches_post_alignment.txt` | export de verification distante, reference seulement |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_POST_ALIGNMENT_VERIFY_04/source_BRANCH_STATE.post_alignment.md` | `REFERENCE_ONLY` | `source_branch_state.post_alignment.md` | capture source post-alignment conservee comme piece de comparaison, pas comme doc ordonnee canonique |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_POST_ALIGNMENT_VERIFY_04/source_GO_INDEX.post_alignment.md` | `REFERENCE_ONLY` | `source_go_index.post_alignment.md` | meme rationale : capture de comparaison historisee |
| `chantier_docs` | `docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_POST_ALIGNMENT_VERIFY_04/source_MATRICE_DOC_OPS_MASTER_MATRIX_01.post_alignment.md` | `REFERENCE_ONLY` | `source_matrice_doc_ops_master_matrix_01.post_alignment.md` | capture source de preuve, non destinee a devenir un doc ordonne actif |
| `module_scripts` | `modules/shared_sshfs_permanent/INSTALL.sh` | `A_CORRIGER_PLUS_TARD` | `install.sh` | script direct de module non aligne sur `lower_snake_case`, mais correction a traiter seulement dans un lot dedie pour ne pas casser d'usage implicite |
| `local_branches` | `branch:GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | `REVIEW_REQUIRED` | `chore/go-opt-trading-ai-team-architecture-parent-01` | branche locale GO sans prefixe de famille ni alignement `go/<GO_ID>` ; arbitrage Git necessaire hors de ce lot naming doc-only |
| `local_branches` | `branch:backup/pre_push_2026_03_14` | `LEGACY_TOLERE` | `backup/pre-push-2026-03-14` | branche de sauvegarde locale ancienne, utile comme reference de rollback et non candidate a correction immediate |
| `local_branches` | `branch:codex/doc-ops-child-branch-cleanup-01` | `REFERENCE_ONLY` | `codex/doc-ops-child-branch-cleanup-01` | branche de travail locale outil, hors canon de branch naming publie pour le repo et sans impact produit |
| `local_branches` | `branch:codex/doc-ops-child-open-work-control-01` | `REFERENCE_ONLY` | `codex/doc-ops-child-open-work-control-01` | meme rationale, branche locale de travail hors surface canonique produit |
| `local_branches` | `branch:codex/module-canonical-consolidation-01` | `REFERENCE_ONLY` | `codex/module-canonical-consolidation-01` | branche locale outil, conservee pour contexte local seulement |
| `local_branches` | `branch:codex/repo-directory-synthesis-parent-01` | `REFERENCE_ONLY` | `codex/repo-directory-synthesis-parent-01` | branche locale outil, non candidate a correction dans ce lot |
| `local_branches` | `branch:codex/reseau-share-transfer-consolidation-01` | `REFERENCE_ONLY` | `codex/reseau-share-transfer-consolidation-01` | branche locale de travail, hors perimetre de normalisation repo publiee |
| `local_branches` | `branch:codex/reseau-ssh-runtime-compat-retirement-01` | `REFERENCE_ONLY` | `codex/reseau-ssh-runtime-compat-retirement-01` | branche locale outil, reference de session uniquement |
| `local_branches` | `branch:codex/root-surface-reclass-01` | `REFERENCE_ONLY` | `codex/root-surface-reclass-01` | branche locale technique, pas un objet naming a corriger dans ce lot |
| `local_branches` | `branch:codex/sot-mainline-backup-a885f0b-prepublish-2026-04-22` | `REFERENCE_ONLY` | `codex/sot-mainline-backup-a885f0b-prepublish-2026-04-22` | sauvegarde locale outillee, conservee comme reference |
| `local_branches` | `branch:codex/winscp-transfer-wrapper-alignment-01` | `REFERENCE_ONLY` | `codex/winscp-transfer-wrapper-alignment-01` | branche locale outil, hors besoin de correction repo-first |
| `local_branches` | `branch:feat/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01` | `LEGACY_TOLERE` | `feat/go-continuite-produit-multi-chantier-canon-01` | branche historique heritee utilisant un identifiant GO uppercase, conservee comme trace sans action naming immediate |
| `local_branches` | `branch:go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01_ISOLATED` | `REVIEW_REQUIRED` | `go/go-opt-trading-doc-ops-child-open-work-control-01-isolated` | suffixe `_ISOLATED` hors forme `go/<GO_ID>` ; decision Git/documentaire a arbitrer dans un lot branche dedie |
| `local_branches` | `branch:main` | `REFERENCE_ONLY` | `chore/main` | tronc historique secondaire local, reference seulement et non cible naming de ce lot |
| `local_branches` | `branch:rescue/derivatives-local-2026-04-09` | `REFERENCE_ONLY` | `rescue/derivatives-local-2026-04-09` | branche rescue locale explicite, utilite de reference / rollback |
| `local_branches` | `branch:rescue/sot-mainline-local-2964fea` | `REFERENCE_ONLY` | `rescue/sot-mainline-local-2964fea` | branche rescue locale explicite, reference seulement |

## Cas sans ecart
- `docs/governance/` : `53` fichiers `CANON`
- scripts racine et `scripts/` : `156` items `CANON`
- aucune proposition d'audit ne demande de correction reelle dans ce lot

## RISKS

- À qualifier.
