---
doc_id: GO_GIT_MIMO_MISC_ABSORBED_RECLASS_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
go_id: GO_GIT_MIMO_MISC_ABSORBED_RECLASS_01
status: pass
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - mimo
  - misc
  - absorbed
  - drop-remote
surface: docs
source_kind: canonical
links:
  - docs/chantiers/GO_GIT_MIMO_MISC_ABSORBED_RECLASS_01/00_cadrage.md
  - docs/index/BRANCH_STATE.md
---

# GO_GIT_MIMO_MISC_ABSORBED_RECLASS_01 - Decisions

## 1_SOUS_LOT_AUDITE

Sous-lot Mimo / misc audite en read-only :

| Branche | SHA | Commit | Absorbee | Commit propre vs `origin/sot/mainline` |
| --- | --- | --- | --- | --- |
| `origin/feat/antigravity-binance-v1` | `f4bfc87b` | `Merge pull request #21 from magikgmo4-ui/sot/mainline` | oui | non |
| `origin/feat/cards01` | `b3470013` | `Merge PR #134: Link continuity to PRODUCT_CONTINUITY_HIERARCHY_01` | oui | non |
| `origin/feat/collectors-lifecycle-wrapper-harmonization-01` | `2a73f980` | `feat(collectors): harmonize lifecycle wrapper surface 01` | oui | non |
| `origin/feat/go-openclaw-chain-03-v1` | `a922532a` | `docs: add GO_OPENCLAW_CHAIN_03 standard chain doc` | oui | non |
| `origin/feat/memory-bricks-v2-bricks-list` | `44eb72ee` | `memory_bricks: add V2 read-only /bricks endpoint` | oui | non |
| `origin/feat/mimo-gate-replay` | `002cb5be` | `Add gate_replay command for window-gated MiMo replay` | oui | non |
| `origin/feat/mimo-open-observer-doc-pack-v0-clean` | `fe89b25c` | `mimo_open_observer: add signal replay csv` | oui | non |
| `origin/feat/mimo-open-observer-market-calendar-v1` | `cef0f467` | `Merge origin/sot/mainline into feat/mimo-open-observer-market-calendar-v1` | oui | non |
| `origin/feat/mimo-scheduler-promotion` | `94227314` | `Add minimal MiMo scheduler wrapper and systemd units` | oui | non |
| `origin/feat/openclaw-registry-expose-01` | `e9ffe84c` | `feat(openclaw): expose configure, doctor, and evidence modules in registry` | oui | non |

Preuve Git retenue pour chaque branche :
- `git log --oneline origin/sot/mainline..<branche>` -> vide
- `git merge-base --is-ancestor <branche> origin/sot/mainline` -> vrai

## 2_ROLE_REEL_DU_SOUS_LOT

Le sous-lot porte des travaux Mimo, collectors, memory bricks, OpenClaw et misc deja absorbes dans le canon repo.

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
