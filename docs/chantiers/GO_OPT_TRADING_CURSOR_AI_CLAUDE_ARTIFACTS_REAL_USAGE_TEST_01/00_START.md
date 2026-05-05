---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01
machine: cursor-ai
status: active
lifecycle_stage: real_usage_test
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - bundles/operator-export/README.md
  - bundles/operator-export/EXPORT_MANIFEST.json
  - bundles/operator-export/HANDOFF.md
  - bundles/claude-artifacts/README.md
  - bundles/claude-artifacts/CHECKLIST_EXECUTION.md
  - bundles/claude-artifacts/bundle_meta/manifest.json
---

# 00_START — GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01

## Objet

Test d'usage reel operateur du pack Claude artifacts (`bundles/claude-artifacts/`).
Validation que le pack est fonctionnel pour un operateur cursor-ai en conditions reelles de reprise, lecture, execution de checklists et handoff.

## Point de depart

- **Base** : `sot/mainline` synchronise, post-merge PR #214 (Option D — cleanup branches).
- **Machine** : cursor-ai.
- **Sequence cursor-ai** : positions 1-4 + Options A, B, C, D terminees.

## Documents de reference

| Document | Role |
| --- | --- |
| `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` | Routage machine anti-conflit, bloc CURSOR_AI |
| `bundles/operator-export/README.md` | Point d'entree operateur |
| `bundles/operator-export/EXPORT_MANIFEST.json` | Inventaire structure de l'export |
| `bundles/operator-export/HANDOFF.md` | Instructions handoff operateur |
| `bundles/claude-artifacts/README.md` | Pack Claude artifacts — survol |
| `bundles/claude-artifacts/CHECKLIST_EXECUTION.md` | Checklist d'execution standard |
| `bundles/claude-artifacts/bundle_meta/manifest.json` | Manifest technique du bundle |

## Livrables

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier — demarrage |
| `10_PRECHECK_STATE.md` | Pre-check : etat des artefacts avant test |
| `20_REAL_USAGE_PROCEDURE.md` | Procedure de test d'usage reel |
| `30_ARTIFACT_VALIDATION.md` | Validation individuelle de chaque artefact du pack |
| `40_HANDOFF_CHECKLIST.md` | Checklist handoff verifiee |
| `50_LIMITS_AND_ROLLBACK.md` | Limites du test et plan de rollback |
| `90_CLOSEOUT.md` | Cloture : verdict PASS/FAIL, diff stat, point de reprise |

## Invariants

- Machine : cursor-ai uniquement.
- Doc-only : fichiers dans `docs/` ou `bundles/` uniquement.
- Aucun runtime trading.
- Aucun admin-trading (ferme sans phrase d'activation).
- Aucun secret, endpoint externe.
- Ne pas rouvrir les PR #205 a #214.
- Patch minimal.

## Verdict attendu

PASS si tous les artefacts du pack sont valides et utilisables en conditions reelles.
FAIL avec raison explicite sinon.
