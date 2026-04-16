---
doc_id: GO_OPT_TRADING_JOURNAL_FULL_READING_03_FREEZE_AFTER_BLOCK_15
doc_type: chantier_decision
repo: opt-trading
project: opt-trading
module: journal
go_id: GO_OPT_TRADING_JOURNAL_FULL_READING_03
status: active
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - journal
  - continuity
  - freeze
surface: chantier
source_kind: canonical
updated_at: 2026-04-16
links:
  - docs/chantiers/GO_OPT_TRADING_JOURNAL_FULL_READING_03/00_cadrage.md
  - docs/index/REPRISE.md
  - docs/index/ACTIVE_STREAMS.md
---

# 03_decision_freeze_after_block_15 — GO_OPT_TRADING_JOURNAL_FULL_READING_03

## Besoin initial

Figer proprement la continuité du chantier de lecture du journal sans laisser `BLOCK_16` et `BLOCK_17` dériver dans la base canonique courante.

## Décision retenue

- la base canonique courante est figée à `JOURNAL_MD_BLOCK_15`
- `JOURNAL_MD_BLOCK_16` et `JOURNAL_MD_BLOCK_17` ne sont **pas** retenus dans la continuité canonique active
- ces blocs sont considérés comme lus hors base canonique stabilisée et devront être relus ou requalifiés plus tard si le chantier est rouvert explicitement

## ETABLI

- le chantier reste `active`
- le point de reprise canonique retenu n’est plus au-delà de `BLOCK_15`
- la reprise future se fera à `BLOCK_16`, soit à partir de la ligne `4421` de `journal.md`
- aucun commit des blocs `16` et `17` n’est pris ici comme vérité canonique du chantier

## Pourquoi

- les segments au-delà de `BLOCK_15` ont surtout densifié de la preuve d’exécution
- l’apport en arbitrages nouveaux, doctrine explicite ou architecture clarifiée n’est pas encore suffisant pour les conserver comme base canonique stable
- il est donc préférable de figer la continuité utile plutôt que de prolonger artificiellement la lecture canonique

## TODO

- ne pas considérer `BLOCK_16` et `BLOCK_17` comme base canonique courante
- reprendre plus tard à `BLOCK_16` uniquement si le chantier est rouvert explicitement
- à la reprise, requalifier d’abord la valeur réelle du bloc avant tout append supplémentaire

## REPRISE

- dernier bloc canonique retenu : `JOURNAL_MD_BLOCK_15`
- blocs explicitement non retenus à ce stade : `JOURNAL_MD_BLOCK_16`, `JOURNAL_MD_BLOCK_17`
- prochain point de reprise si réouverture : `journal.md` ligne `4421`
