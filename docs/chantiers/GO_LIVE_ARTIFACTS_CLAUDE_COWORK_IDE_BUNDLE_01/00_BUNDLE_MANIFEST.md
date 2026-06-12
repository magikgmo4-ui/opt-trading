---
doc_id: GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01_MANIFEST
doc_type: bundle_manifest
repo: opt-trading
project: opt-trading
module:
  go_id: GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01
status: open
lifecycle_stage: bundle_delivery
surface: docs
source_kind: canonical
updated_at: 2026-04-26
---

# GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01 — manifest

## 1_MASTER_TARGET

Fournir un bundle IDE complet pour cadrer, installer et exécuter la préparation des Live Artifacts Claude Cowork dans le workflow `opt-trading`, sans modifier le runtime et sans remplacer la vérité canonique du repo.

## 2_INITIAL_PROJECT_DOC

Ce bundle dérive du chantier parent local annoncé :

- `GO_LIVE_ARTIFACTS_CLAUDE_COWORK_PARENT_DOC_01`
- branche locale annoncée : `go/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_PARENT_DOC_01`
- worktree local annoncé : `C:\Users\ghost\opt-trading\.codex_tmp\live_artifacts_parent_doc_01`

Ce bundle est livré sur une branche séparée pour éviter toute collision avec la branche locale non pushée.

## 3_INITIAL_NEED

L’utilisateur demande un bundle IDE complet déposé dans le repo pour poursuivre le chantier Live Artifacts Claude Cowork.

## 4_MASTER_PROJECT_PLAN

1. Déposer un bundle autonome dans `docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/`.
2. Maintenir le lot strictement documentaire.
3. Fournir les prompts IDE et Claude Cowork.
4. Fournir les règles de sécurité source/connecteurs.
5. Fournir le plan de workspace et snapshot read-only.
6. Fournir les tests d’acceptation.
7. Fournir un point de reprise.

## Contenu du bundle

| Fichier | Rôle |
|---|---|
| `00_BUNDLE_MANIFEST.md` | manifest et contexte canonique |
| `01_IDE_HANDOFF.md` | instructions pour Trae / Claude / OpenCode |
| `02_REPO_INSTALL_PLAN.md` | plan de dépôt local dans le worktree dédié |
| `03_CLAUDE_COWORK_LIVE_ARTIFACT_PROMPTS.md` | prompts prêts à coller dans Claude Cowork |
| `04_WORKSPACE_SNAPSHOT_PLAN.md` | workspace Claude + snapshot repo read-only |
| `05_SOURCE_SECURITY_MATRIX.md` | matrice sécurité connecteurs / sources |
| `06_ACCEPTANCE_TESTS.md` | tests PASS/FAIL des artifacts |
| `BRANCH_STATE.md` | état branche remote bundle |
| `GAP_INDEXATION.md` | indexation non appliquée pour éviter conflit avec branche locale parent |
| `SESSION_REPRISE.txt` | reprise opérationnelle |

## 12_INVARIANTS

- Live Artifacts Claude Cowork = cockpit dynamique read-only.
- Repo / docs / commits / closeouts = vérité canonique.
- Claude Cowork = opérateur assisté, pas source canonique.
- OpenClaw = orchestrateur local / runtime potentiel, mais NO_GO_INITIAL tant que sécurité non cadrée.
- Aucun accès large au disque.
- Aucun `computer use` sur repo/trading au départ.
- Aucun MCP OpenClaw avant cadrage sécurité.
- Aucun merge / push / delete sans GO explicite.

## 17_RESUME_POINT

Lire dans l’ordre :

1. `00_BUNDLE_MANIFEST.md`
2. `01_IDE_HANDOFF.md`
3. `02_REPO_INSTALL_PLAN.md`
4. `05_SOURCE_SECURITY_MATRIX.md`
5. `03_CLAUDE_COWORK_LIVE_ARTIFACT_PROMPTS.md`
6. `06_ACCEPTANCE_TESTS.md`
7. `SESSION_REPRISE.txt`

## RISKS

- À qualifier.
