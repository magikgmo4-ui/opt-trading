---
doc_id: GO_GIT_PRODUCT_CARDS_SESSION_ABSORBED_RECLASS_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
go_id: GO_GIT_PRODUCT_CARDS_SESSION_ABSORBED_RECLASS_01
status: pass
lifecycle_stage: classification
updated_at: 2026-04-22
topic_keys:
  - git
  - branches
  - product
  - cards
  - session
  - absorbed
  - drop-remote
surface: docs
source_kind: canonical
links:
  - docs/chantiers/GO_GIT_PRODUCT_CARDS_SESSION_ABSORBED_RECLASS_01/00_cadrage.md
  - docs/index/BRANCH_STATE.md
---

# GO_GIT_PRODUCT_CARDS_SESSION_ABSORBED_RECLASS_01 - Decisions

## 1_SOUS_LOT_AUDITE

Sous-lot Product / cards / session audite en read-only :

| Branche | SHA | Commit | Absorbee | Commit propre vs `origin/sot/mainline` |
| --- | --- | --- | --- | --- |
| `origin/feat/product-target-canon` | `3dde74fc` | `docs(product): add canonical product targets + runtime mapping` | oui | non |
| `origin/feat/project-card-bot-vision-ingestion-01` | `20089ac8` | `docs(bot-vision): add bot vision ingestion project card closing 01` | oui | non |
| `origin/feat/project-card-trading-analytics-chain-01` | `a3681d52` | `docs(analytics): add trading analytics chain project card closing 01` | oui | non |
| `origin/feat/project-cards-canonical-alignment-01` | `58d83f0b` | `docs(ot): close GitHub park file role cartography 01` | oui | non |
| `origin/feat/project-cards-gate-alignment-01` | `58d83f0b` | `docs(ot): close GitHub park file role cartography 01` | oui | non |
| `origin/feat/project-portfolio-validated-plans-freeze-01` | `016ec999` | `docs(portfolio): add closeout for validated plans freeze` | oui | non |
| `origin/feat/session-documentation-gate` | `784c4cde` | `docs(governance): add session documentation gate reference` | oui | non |
| `origin/feat/docs-index-chantier-inventory-sync-01` | `d8e1bd97` | `docs(index): include all documented chantiers in GO_INDEX` | oui | non |
| `origin/feat/OT_DESKPRO_RELEASE_OPS_DRILL_01` | `2899945d` | `desk_pro: close release ops drill and clarify runbook scope` | oui | non |

Preuve Git retenue pour chaque branche :
- `git log --oneline origin/sot/mainline..<branche>` -> vide
- `git merge-base --is-ancestor <branche> origin/sot/mainline` -> vrai

## 2_ROLE_REEL_DU_SOUS_LOT

Le sous-lot porte des documents produit, project cards, gouvernance de session et closeouts deja absorbes dans le canon repo.

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
