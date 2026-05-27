---
doc_id: GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01_REGISTRY_ACTIONS
doc_type: registry_actions
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - journal
  - registry
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01/40_SURVIVOR_DECISION.md
---

# 50_REGISTRY_ACTIONS

## Invariant du lot

Aucune mutation de `registry/modules_registry.yaml` n'est executee dans ce GO.

## Etat registry actuel

- aucune entree `journal_engine` detectee dans `registry/modules_registry.yaml`
- aucune entree `journal_de_bord` detectee non plus

## Gap registry etabli

Le survivant courant de la famille `journal` n'est pas represente dans la registry modules.

## Actions registry requises ensuite

### Action R1

Ajouter `journal_engine` en registry comme module actif de journalisation structuree.

### Action R2

Ne pas recreer `journal_de_bord` comme module actif dans la registry.

### Action R3

Si un besoin de trace historique est juge utile, documenter `journal_de_bord` uniquement comme surface legacy retiree, pas comme module courant.

## Actions registry a ne pas faire

- ne pas rouvrir `journal_de_bord` comme surface active
- ne pas traiter l'absence de `journal_de_bord` comme un blocker runtime

## GO suivant necessaire pour mutation registry

`GO_OPT_TRADING_JOURNAL_FAMILY_REGISTRY_REALIGNMENT_01`

Objet attendu:

- ajouter `journal_engine`
- aligner la registry avec le parc courant
- conserver `journal_de_bord` hors surfaces actives
