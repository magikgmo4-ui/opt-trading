---
doc_id: GO_OPT_TRADING_JOURNAL_FULL_READING_03_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: journal
go_id: GO_OPT_TRADING_JOURNAL_FULL_READING_03
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - journal
  - human_layer
  - reading
surface: chantier
source_kind: canonical
updated_at: 2026-04-18
links:
  - journal/canon/JOURNAL_CANON_FULL_20260301_071931.md
  - journal.md
  - docs/governance/JOURNAL_HIERARCHY.md
---

# 00_cadrage — GO_OPT_TRADING_JOURNAL_FULL_READING_03

## Identité
- GO : GO_OPT_TRADING_JOURNAL_FULL_READING_03
- Repo : opt-trading
- Branche : sot/mainline
- Statut : active
- Type de travail : lecture complète du journal canon et extraction de la couche humaine utile

## État de départ retenu
- état repo retenu : le cadre inter-repos est posé, mais la couche humaine vivante n’est pas encore réinjectée proprement dans la continuité stable
- source canon retenue : `journal/canon/JOURNAL_CANON_FULL_20260301_071931.md` (archive de lecture ; voir `docs/governance/JOURNAL_HIERARCHY.md`)
- limites connues : le journal contient à la fois du contexte humain utile, des commandes, des décisions et des éléments possiblement obsolètes

## Objectif du lot
- objectif principal : relire le journal canon complet et produire ensuite des blocs de validation humaine fidèles, courts et exploitables
- résultat attendu : extraction triée entre établi, à revalider, obsolète et candidats de doc humaine

## Non-objectifs
- injecter le brut du journal directement dans la doc stable
- réécrire maintenant tout le journal historique

## Critères PASS / FAIL
- PASS si : les blocs extraits sont fidèles à la source et présentables bloc par bloc pour validation
- FAIL si : l’extraction mélange le brut, l’obsolète et le validé sans séparation claire
