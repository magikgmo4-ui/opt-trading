---
doc_id: GO_GIT_RUNTIME_ENGINE_HELPERS_ABSORBED_RECLASS_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
go_id: GO_GIT_RUNTIME_ENGINE_HELPERS_ABSORBED_RECLASS_01
status: pass
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - runtime
  - engine
  - helpers
  - absorbed
  - drop-remote
surface: docs
source_kind: canonical
links:
  - docs/chantiers/GO_GIT_RUNTIME_ENGINE_HELPERS_ABSORBED_RECLASS_01/00_cadrage.md
  - docs/index/BRANCH_STATE.md
---

# GO_GIT_RUNTIME_ENGINE_HELPERS_ABSORBED_RECLASS_01 - Decisions

## 1_SOUS_LOT_AUDITE

Sous-lot Runtime / engine / helpers audite en read-only :

| Branche | SHA | Commit | Absorbee | Commit propre vs `origin/sot/mainline` |
| --- | --- | --- | --- | --- |
| `origin/feat/engines-plugin` | `da9ed195` | `refactor(engines): validate engine names via registry` | oui | non |
| `origin/feat/execution-engine` | `3e5e7634` | `feat(execution): wire PAPER_TEST to paper executor` | oui | non |
| `origin/feat/persistent-state` | `e6b62c30` | `feat(position): persist positions to state/positions.json` | oui | non |
| `origin/feat/position-engine` | `38e34773` | `feat(position): track PAPER_TEST positions after execution` | oui | non |
| `origin/feat/position-guard` | `1960ddf8` | `feat(position): use guard in PAPER_TEST path` | oui | non |
| `origin/feat/student-ops-helpers-01` | `8353cc9c` | `feat(student_ops): add student helpers and sanity tooling 01` | oui | non |
| `origin/feat/trading-realtime-v1-event-bridge` | `55ade42f` | `feat(trading): add realtime v1 event bridge with backups and docs update` | oui | non |
| `origin/feat/trading-realtime-v1-export` | `91ea1463` | `feat(trading): add realtime v1 export with backups and docs update` | oui | non |
| `origin/feat/trading-realtime-v1-guardrails` | `9500fa0c` | `feat(trading): add realtime v1 guardrails with backups and docs update` | oui | non |
| `origin/feat/trading-realtime-v1-reporting` | `225e83ca` | `feat(trading): add realtime v1 reporting with backups and docs update` | oui | non |
| `origin/feat/trading-realtime-v1-runtime-loop` | `ff5160db` | `feat(trading): add realtime v1 runtime loop with backups and docs update` | oui | non |
| `origin/feat/trading-realtime-v1-timer` | `fcff4252` | `feat(trading): add realtime v1 timer with backups and docs update` | oui | non |
| `origin/feature/hf-publish-helper-fix-01` | `fd99b4ed` | `hf_free_platform: keep publish helper clone for manual review` | oui | non |
| `origin/feature/hf-tools-private-config-fix-01` | `40a8fdc3` | `hf_free_platform: fix tools_private HF metadata` | oui | non |

Preuve Git retenue pour chaque branche :
- `git log --oneline origin/sot/mainline..<branche>` -> vide
- `git merge-base --is-ancestor <branche> origin/sot/mainline` -> vrai

## 2_ROLE_REEL_DU_SOUS_LOT

Le sous-lot porte des features runtime, moteurs, garde-fous et helpers deja absorbes dans le canon repo.

Constat retenu :
- le contenu utile est deja preserve dans `origin/sot/mainline`
- ces branches ne portent plus de reprise Git autonome necessaire
- leur maintien en remote n'est plus requis pour la continuite produit et outillage

## 3_RECLASSIFICATION

Statut cible retenu pour tout le sous-lot :

`DROP_REMOTE_CANDIDATE`

Motifs :
1. branches absorbees dans `origin/sot/mainline`
2. aucun commit propre restant hors canon
3. valeur produit et outillage preservee par le contenu deja merge
4. suppression remote possible dans un second passage borne

## 4_VERDICT

- `ABSORBED`
- `DROP_REMOTE_CANDIDATE`

Ce passage reste strictement doc-only.

Aucun delete Git n'est execute ici.
