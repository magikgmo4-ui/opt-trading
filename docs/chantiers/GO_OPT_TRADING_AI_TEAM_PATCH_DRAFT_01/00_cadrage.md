---
doc_id: GO_OPT_TRADING_AI_TEAM_PATCH_DRAFT_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_PATCH_DRAFT_01
status: open
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/90_PARENT_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/01_architecture_cible.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/92_NEXT_GO_CANDIDATES.md
---

# GO_OPT_TRADING_AI_TEAM_PATCH_DRAFT_01 — 00_cadrage

## 1_MASTER_TARGET

Definir et tester un PATCH_DRAFT strictement borne, produit par le runner AI Team comme proposition documentaire, sans application automatique, sans git write, avec Gatekeeper HITL obligatoire.

## 3_INITIAL_NEED

L'Architecture Canon prevoit PATCH_DRAFT comme 5e task type (Analyzer: "proposer un diagnostic ou un patch draft"). Les 4 autres task types sont deja implementes et smokes. PATCH_DRAFT est le dernier manquant pour completer le set de primitives de l'Architecture Canon.

## 4_MASTER_PROJECT_PLAN

1. Definir le contrat PATCH_DRAFT.
2. Etendre le runner avec le handler PATCH_DRAFT.
3. Creer le task packet `patch_draft.json`.
4. Definir la zone d'ecriture `drafts/patches/`.
5. Implementer les garde-fous : no git write, no file modification, DRAFT_ONLY.
6. Executer le smoke sur un fichier non sensible.
7. Valider Gatekeeper HITL.
8. Mettre a jour les registres.

## 7_CANONICAL_STATE

- Parent AI Team : CLOSED_PHASE_1
- Runner supporte : READ_INVENTORY, DOC_DRAFT, ANALYZE_INVENTORY, ORCHESTRATOR_CHAIN
- 27/27 smokes cumules PASS
- Modele : opencode-go/deepseek-v4-pro
- Type : doc-only + runner avec PATCH_DRAFT (proposal only)

## 11_KEY_DECISIONS

- PATCH_DRAFT est une PROPOSITION, jamais une application.
- Le runner ne modifie JAMAIS le fichier cible.
- Le runner n'execute JAMAIS de commande git.
- La sortie est dans `drafts/patches/` uniquement.
- Le Gatekeeper (humain) doit valider avant toute application manuelle.
- Le fichier cible du smoke doit etre non sensible, sous versionnement.

## 12_INVARIANTS

- Aucun git write depuis le runner.
- Aucune modification de fichier (read-only sur la cible).
- Write limite a drafts/patches/.
- Aucun secret, .env, token, credential.
- Ne pas ouvrir ClickUp.
- Ne pas restaurer ni drop le stash reseau_ssh.

## 16_TODO

1. Rediger `01_patch_draft_contract.md`.
2. Creer `modules/ai_team_mvp/tasks/patch_draft.json`.
3. Creer `modules/ai_team_mvp/drafts/patches/README.md`.
4. Etendre `modules/ai_team_mvp/runner.py` avec PATCH_DRAFT.
5. Executer smoke PATCH_DRAFT.
6. Rediger `02_gatekeeper_validation.md`.
7. Rediger `03_smoke_report.md`.
8. Mettre a jour registries.
9. Rediger `90_CLOSEOUT.md`.

## 17_RESUME_POINT

Reprendre depuis `01_patch_draft_contract.md`, etendre le runner, executer smoke, valider.
