---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
status: draft_canonical
lifecycle_stage: opening
surface: chantier
source_kind: canonical
updated_at: 2026-05-22
topic_keys:
  - opt-trading
  - doc_ops
  - patch
  - zip
  - openclaw
  - strict_workers
  - evidence
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Appliquer le patch, valider la spec V2, puis ouvrir un GO test avec sidecar zip si necessaire."
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PATCH_ZIP_EXECUTION_FORMAT_V2_01.md
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
  - docs/chantiers/GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01/20_BRIDGE_CONTRACTS.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir un chantier doc-ops pour formaliser le format V2 des artefacts `.patch` et `.zip`, avec execution end-to-end possible par OpenClaw, strict workers, workers app externes, IDE et operateur humain.

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche initiale du chantier. Il fige le besoin, le plan, les decisions et le point de reprise.

## 3_INITIAL_NEED

Clarifier le format optimal des artefacts produits par l'assistant pour les chantiers GitHub :

- ne plus produire deux formats redondants ;
- utiliser `.patch` comme support canonique Git ;
- reserver `.zip` aux charges lourdes et temporaires ;
- inclure le maximum de jobs deja presents dans le repo ;
- integrer les strict workers et workers app externes ;
- rendre le tout executable par OpenClaw ;
- documenter prompts, steps operatoires, preuves, checklists et closeout.

## 4_MASTER_PROJECT_PLAN

1. Produire une regle de gouvernance `PATCH_ZIP_EXECUTION_FORMAT_V2_01`.
2. Documenter le contexte de session et les decisions.
3. Definir un runbook OpenClaw E2E.
4. Definir un graph de jobs reutilisant les strict workers existants.
5. Definir les workers app externes et leurs gates.
6. Definir le contrat de preuves.
7. Definir la checklist humaine / Claude cowork.
8. Ouvrir une entree courte `docs/index/inbox/<GO_ID>.md`.
9. Ajouter des job packets plats sous `scripts/ai/workers/job_packets/`.
10. Ne modifier aucun index global.

## 5_GO_PLAN

Ce chantier est doc-only au sens runtime : il ne lance aucune execution externe et ne modifie aucune configuration runtime.

Le patch ajoute :

- une regle de gouvernance ;
- un dossier chantier complet ;
- une entree inbox ;
- des job packets de reference DRAFT_ONLY.

## 6_FINAL_TARGET

Avoir un format V2 pret a etre utilise comme standard pour les prochains bundles IDE/OpenClaw :

- patch autoporteur ;
- zip optionnel ;
- job graph ;
- evidence contract ;
- checklists ;
- delegation workers ;
- closeout target.

## 7_CANONICAL_STATE

Etat courant au demarrage :

- `opt-trading` reste le repo canonique ;
- `sot/mainline` reste la base de depart ;
- le format patch-first est retenu comme direction ;
- le zip est optionnel et non canonique ;
- les strict workers existants doivent etre reutilises avant toute creation de job ;
- OpenClaw orchestre, gate et collecte les preuves ;
- les index globaux restent proteges.

## 8_VALIDATED_PLAN

Plan valide pour ce patch :

1. ajouter les docs ;
2. ajouter job packets DRAFT_ONLY ;
3. appliquer avec `git apply --check` ;
4. appliquer avec `git apply` ;
5. valider fichiers ajoutes ;
6. commit ;
7. push branche dediee ;
8. PR review ;
9. evaluer target atteint.

## 9_SELECTED_SOLUTION

`PATCH_FIRST + ZIP_OPTIONAL + OPENCLAW_E2E + STRICT_WORKERS_MAX_REUSE + EVIDENCE_CONTRACT`.

## 10_SELECTED_SETUP

- Branche recommandee : `go/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01`.
- Patch unique : `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01.patch`.
- Pas de zip pour ce chantier d'ouverture.
- Zip a tester dans un GO ulterieur avec scripts ou payloads reels.

## 11_KEY_DECISIONS

- Tout fichier durable va dans le patch.
- Le zip ne transporte que le lourd, temporaire ou hors repo.
- Les job packets doivent rester compatibles avec `tasks.index.json`.
- Les modeles utilises doivent etre verifies dans `models.registry.json`.
- Les workers app externes doivent suivre leurs contrats.
- Aucune modification des index globaux dans ce GO.

## 12_INVARIANTS

- Pas de secrets.
- Pas de `.env`.
- Pas de token.
- Pas de write externe.
- Pas de commit/push par worker strict.
- Pas de modification runtime.
- Pas de global index sauf nouveau besoin explicite.

## 13_ESTABLISHED

Le format V1 etait utile mais insuffisant : il separait parfois documentation et patch alors que le patch peut porter tous les fichiers destines au repo.

## 14_HYPOTHESIS

Un futur GO peut tester le niveau `LEVEL_2_PATCH_PLUS_ZIP` avec payloads reels, scripts smoke temporaires et preuves externes.

## 15_REMAINING_GAP

- Valider le patch dans un repo local.
- Confirmer si les job packets plats sont acceptes par le validateur actuel.
- Tester un vrai run OpenClaw sur un prochain GO.

## 16_TODO

- Appliquer ce patch.
- Ouvrir PR.
- Review doc-only.
- Fermer le GO si la spec V2 est acceptee.

## 17_RESUME_POINT

Reprendre depuis `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/20_OPENCLAW_E2E_RUNBOOK.md` pour execution.
