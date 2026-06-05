---
doc_id: GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01_BRANCH_DISPOSITION_01
doc_type: chantier_branch_disposition
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01
branch: go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01
status: draft
lifecycle_stage: local_disposition
topic_keys:
  - cursor_ai
  - why_layer
  - branch_disposition
  - reference_merged_candidate
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01/10_WHY_LAYER_AUDIT.md
---

# 80_BRANCH_DISPOSITION_01

## 13_ESTABLISHED

- Branche: `go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01`
- Worktree local de reprise: `C:\wla01`
- Branche locale a parite avec `origin/go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01`
- Vs `origin/sot/mainline`: `0 ahead / 971 behind`
- Diff de contenu contre `origin/sot/mainline...HEAD` vide au moment de la reprise
- Dossier chantier deja present sur `sot/mainline`
- Scope confirme: doc-only, aucun runtime, aucun `GO_INDEX`

## 14_HYPOTHESIS

- La branche existe encore comme support Git, mais ne porte plus de delta actif propre.
- Le chantier WHY layer reste reutilisable comme reference documentaire.
- Une suite utile ne doit pas etre menee comme prolongation directe de cette branche, mais comme nouveau child GO doc-only depuis `sot/mainline`.

## 15_REMAINING_GAP

- Le bloc machine `CURSOR_AI` peut encore donner une impression d'activite tant qu'il n'est pas reclassifie explicitement.
- Aucune note de disposition n'etait presente localement avant ce fichier.
- Aucun lot explicite de cleanup branches n'est encore ouvert pour arbitrer suppression ou conservation.

## 16_TODO

1. Conserver cette branche en `REFERENCE_MERGED_CANDIDATE` tant qu'aucun GO cleanup explicite n'est ouvert.
2. Ne pas supprimer la branche sans lot dedie de housekeeping.
3. Ne pas considerer cette branche comme chantier actif sur sa seule existence Git.
4. Si une suite produit est necessaire, ouvrir un nouveau child GO doc-only depuis `sot/mainline`.
5. Ne pas toucher aux index globaux dans ce passage.

## 17_RESUME_POINT

Pour toute reprise future sur le sujet WHY layer cursor-ai:

1. relire cette note de disposition ;
2. verifier de nouveau l'etat Git reel vs `origin/sot/mainline` ;
3. si un nouveau delta est necessaire, l'ouvrir sur une nouvelle branche doc-only issue de `sot/mainline`.

## VERDICT

`REFERENCE_MERGED_CANDIDATE`

La branche `go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01` ne doit pas etre traitee comme chantier actif uniquement parce qu'elle existe encore. Elle doit etre consideree comme reference documentaire mergee candidate, sans suppression de branche dans ce lot.

## RISKS

- À qualifier.
