---
doc_id: GO_GIT_SIMEX_ABSORBED_RECLASS_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
go_id: GO_GIT_SIMEX_ABSORBED_RECLASS_01
status: pass
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - simex
  - absorbed
  - drop-remote
surface: docs
source_kind: canonical
links:
  - docs/chantiers/GO_GIT_SIMEX_ABSORBED_RECLASS_01/00_cadrage.md
  - docs/index/BRANCH_STATE.md
---

# GO_GIT_SIMEX_ABSORBED_RECLASS_01 - Decisions

## 1_SOUS_LOT_AUDITE

Sous-lot Simex audite en read-only :

| Branche | SHA | Commit | Absorbee | Commit propre vs `origin/sot/mainline` |
| --- | --- | --- | --- | --- |
| `origin/docs/index-simex-link-01` | `9727e7f9` | `docs(index): link simex presets doc` | oui | non |
| `origin/docs/simex-presets-01` | `d2be6e43` | `docs(simex): add SIMEX_* presets and run commands` | oui | non |
| `origin/feat/admin-trading-simex-insufficient-candles-evidence-closeout-01` | `637ba5df` | `docs(simex): add insufficient candles evidence closeout for admin-trading` | oui | non |
| `origin/feat/admin-trading-simex-insufficient-candles-hardening-01` | `df0f7a9f` | `simex: harden insufficient candles upstream path` | oui | non |
| `origin/feat/admin-trading-simex-runtime-evidence-closeout-01` | `5d303277` | `docs(simex): add admin-trading runtime evidence closeout` | oui | non |
| `origin/feat/admin-trading-simex-upstream-failure-hardening-01` | `b6ef6784` | `simex: harden upstream failure handling for Bitget fetches` | oui | non |
| `origin/feat/admin-trading-simex-upstream-hardening-evidence-closeout-01` | `89e30551` | `docs(simex): add upstream hardening evidence closeout for admin-trading` | oui | non |
| `origin/feat/admin-trading-simex-upstream-hardening-evidence-upgrade-01` | `ff628e8f` | `docs(simex): upgrade upstream hardening evidence closeout to complete` | oui | non |
| `origin/feat/fantome-simex-module-durable-01` | `4c22c58a` | `simex: extract Bitget bridge into durable module` | oui | non |
| `origin/feat/simex-env-bridge-01` | `970da900` | `simex: make bitget_bridge configurable via SIMEX_* env` | oui | non |
| `origin/feat/simex-units-contract-01` | `bf5086e0` | `simex: add explicit units contract and legacy env bridge` | oui | non |
| `origin/feat/simex-wrappers-01` | `e1b4f600` | `simex: add cmd/menu/sanity wrappers (perf+bitget bridge)` | oui | non |

Preuve Git retenue pour chaque branche :
- `git log --oneline origin/sot/mainline..<branche>` -> vide
- `git merge-base --is-ancestor <branche> origin/sot/mainline` -> vrai

## 2_ROLE_REEL_DU_SOUS_LOT

Le sous-lot porte des documents, closeouts, hardenings et wrappers Simex deja absorbes dans le canon repo.

Constat retenu :
- le contenu utile est deja preserve dans `origin/sot/mainline`
- ces branches ne portent plus de reprise Git autonome necessaire
- leur maintien en remote n'est plus requis pour la continuite documentaire et produit

## 3_RECLASSIFICATION

Statut cible retenu pour tout le sous-lot :

`DROP_REMOTE_CANDIDATE`

Motifs :
1. branches absorbees dans `origin/sot/mainline`
2. aucun commit propre restant hors canon
3. valeur documentaire et produit preservee par le contenu deja merge
4. suppression remote possible dans un second passage borne

## 4_VERDICT

- `ABSORBED`
- `DROP_REMOTE_CANDIDATE`

Ce passage reste strictement doc-only.

Aucun delete Git n'est execute ici.

## RISKS

- À qualifier.
