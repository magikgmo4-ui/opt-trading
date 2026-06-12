---
doc_id: GO_GIT_GITHUB_PARK_CLOSEOUT_ABSORBED_RECLASS_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
go_id: GO_GIT_GITHUB_PARK_CLOSEOUT_ABSORBED_RECLASS_01
status: pass
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - github-park
  - closeout
  - drop-remote
surface: docs
source_kind: canonical
links:
  - docs/chantiers/GO_GIT_GITHUB_PARK_CLOSEOUT_ABSORBED_RECLASS_01/00_cadrage.md
  - docs/index/BRANCH_STATE.md
---

# GO_GIT_GITHUB_PARK_CLOSEOUT_ABSORBED_RECLASS_01 - Decisions

## 1_SOUS_LOT_AUDITE

Sous-lot GitHub park / closeout audite en read-only :

| Branche | SHA | Commit | Absorbee | Commit propre vs `origin/sot/mainline` |
| --- | --- | --- | --- | --- |
| `origin/closeout/collectors-lifecycle-compat-01` | `09b1b1b8` | `docs(collectors): add lifecycle compat closeout 01` | oui | non |
| `origin/docs/github-park-audit-expansion-closeout-01` | `b2f38f7a` | `docs(reprise): remove github park parent from active matrix` | oui | non |
| `origin/docs/github-park-branch-trunk-cross-audit-01` | `783b141d` | `docs(chantiers): add github park branch trunk cross audit target` | oui | non |

Preuve Git retenue pour chaque branche :
- `git log --oneline origin/sot/mainline..<branche>` -> vide
- `git merge-base --is-ancestor <branche> origin/sot/mainline` -> vrai

## 2_ROLE_REEL_DU_SOUS_LOT

Le sous-lot porte des closeouts et documents GitHub park deja absorbes dans le canon repo.

Constat retenu :
- le contenu utile est deja preserve dans `origin/sot/mainline`
- ces branches ne portent plus de reprise Git autonome necessaire
- leur maintien en remote n'est plus requis pour la continuite documentaire

## 3_RECLASSIFICATION

Statut cible retenu pour tout le sous-lot :

`DROP_REMOTE_CANDIDATE`

Motifs :
1. branches absorbees dans `origin/sot/mainline`
2. aucun commit propre restant hors canon
3. valeur documentaire preservee par le contenu deja merge
4. suppression remote possible dans un second passage borne

## 4_VERDICT

- `ABSORBED`
- `DROP_REMOTE_CANDIDATE`

Ce passage reste strictement doc-only.

Aucun delete Git n'est execute ici.

## RISKS

- À qualifier.
