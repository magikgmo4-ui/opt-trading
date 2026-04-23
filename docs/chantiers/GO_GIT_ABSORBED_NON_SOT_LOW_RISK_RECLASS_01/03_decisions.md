---
doc_id: GO_GIT_ABSORBED_NON_SOT_LOW_RISK_RECLASS_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
go_id: GO_GIT_ABSORBED_NON_SOT_LOW_RISK_RECLASS_01
status: pass
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - absorbed
  - low-risk
  - drop-remote
surface: docs
source_kind: canonical
links:
  - docs/chantiers/GO_GIT_ABSORBED_NON_SOT_LOW_RISK_RECLASS_01/00_cadrage.md
  - docs/index/BRANCH_STATE.md
---

# GO_GIT_ABSORBED_NON_SOT_LOW_RISK_RECLASS_01 - Decisions

## 1_SOUS_LOT_AUDITE

Sous-lot audite en read-only :

| Branche | SHA | Commit | Absorbee | Commit propre vs `origin/sot/mainline` |
| --- | --- | --- | --- | --- |
| `origin/docs/chatgpt-profile-baseline-index-01` | `06e11ba4` | `docs(index): add chatgpt profile baseline reference` | oui | non |
| `origin/feat/range-strategy-v1-struct` | `b76fb17b` | `docs(chantier): add strategy kernel shared layer closeout` | oui | non |

Preuve Git retenue pour chaque branche :
- `git log --oneline origin/sot/mainline..<branche>` -> vide
- `git merge-base --is-ancestor <branche> origin/sot/mainline` -> vrai

## 2_ROLE_REEL_DU_SOUS_LOT

Le sous-lot porte deux branches absorbees non sensibles dont le contenu est deja preserve dans `origin/sot/mainline`.

Constat retenu :
- aucun commit propre ne subsiste hors canon
- leur maintien en remote n'est plus requis
- elles sont candidates a suppression remote dans un second passage borne

## 3_RECLASSIFICATION

Statut cible retenu pour les deux branches :

`DROP_REMOTE_CANDIDATE`

## 4_VERDICT

- `ABSORBED`
- `DROP_REMOTE_CANDIDATE`

Ce passage reste strictement doc-only.

Aucun delete Git n'est execute ici.
