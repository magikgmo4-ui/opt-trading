---
doc_id: GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
go_id: GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01
status: pass
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - openclaw
  - absorbed
  - drop-remote
surface: docs
source_kind: canonical
links:
  - docs/chantiers/GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01/00_cadrage.md
  - docs/index/BRANCH_STATE.md
---

# GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01 - Decisions

## 1_SOUS_LOT_AUDITE

Sous-lot OpenClaw audite en read-only :

| Branche | SHA | Commit | Absorbee | Commit propre vs `origin/sot/mainline` |
| --- | --- | --- | --- | --- |
| `origin/docs/go-openclaw-evidence-01-v1` | `7e209fa2` | `docs: add GO_OPENCLAW_EVIDENCE_01 runbook` | oui | non |
| `origin/docs/openclaw-alignment-decision-07` | `98b54a4e` | `docs(openclaw): add alignment decision GO` | oui | non |
| `origin/docs/openclaw-alignment-exception-08` | `0db3cfb4` | `docs(openclaw): add alignment exception decision note` | oui | non |
| `origin/docs/openclaw-alignment-read-06` | `14606343` | `docs(openclaw): add alignment read GO` | oui | non |
| `origin/docs/openclaw-policy-runtime-alignment-05` | `8c0f31a5` | `docs(openclaw): add policy runtime alignment note` | oui | non |
| `origin/docs/openclaw-state-dir-vigilance-03` | `19df41ee` | `docs(openclaw): add state dir vigilance note` | oui | non |
| `origin/go/openclaw-sync-02-doc` | `2f3a1f6c` | `docs(openclaw): add GO_OPENCLAW_SYNC_02 canonical sync note` | oui | non |

Preuve Git retenue pour chaque branche :
- `git log --oneline origin/sot/mainline..<branche>` -> vide
- `git merge-base --is-ancestor <branche> origin/sot/mainline` -> vrai

## 2_ROLE_REEL_DU_SOUS_LOT

Le sous-lot porte des documents OpenClaw de diagnostic, alignement, vigilance, evidence et sync deja absorbes dans le canon repo.

Constat retenu :
- ces branches ne servent plus de support de reprise Git autonome
- leur contenu documentaire utile est deja preserve dans `origin/sot/mainline`
- leur maintien en remote n'est plus necessaire pour la continuite documentaire

## 3_RECLASSIFICATION

Statut cible retenu pour tout le sous-lot :

`DROP_REMOTE_CANDIDATE`

Motifs :
1. branches absorbees dans `origin/sot/mainline`
2. aucun commit propre restant hors canon
3. valeur documentaire preservee par le contenu deja merge
4. suppression remote possible dans un second passage borne

## 4_VERDICT

Verdict du sous-lot :

- `ABSORBED`
- `DROP_REMOTE_CANDIDATE`

Ce passage reste strictement doc-only.

Aucune suppression Git n'est executee ici.
