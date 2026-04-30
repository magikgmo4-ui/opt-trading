---
doc_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01_RULE
doc_type: chantier_rule
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01
status: draft
lifecycle_stage: rule_definition
topic_keys:
  - opt-trading
  - parent_chantier
  - local_continuity
  - index_inbox
  - global_indexes
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01/00_CADRAGE.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01/REPRISE.md
updated_at: 2026-04-30
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_01/00_CADRAGE.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# REGLE — Continuite locale des parents

## Regle canonique proposee

Pour tout nouveau chantier parent :

1. La continuite de travail courante est conservee dans `docs/chantiers/<GO_PARENT>/`.
2. Le parent contient au minimum un cadrage, un plan ou etat courant, un point de reprise et, si branche dediee, un `BRANCH_STATE.md` local.
3. Une entree courte et atomique est creee dans `docs/index/inbox/<GO_PARENT>.md`.
4. Les index globaux ne sont pas modifies a chaque micro-avancement.
5. Les index globaux sont mis a jour seulement par batch d'agregation, ouverture/fermeture significative, changement de statut global ou changement de next GO global.

## Structure minimale recommandee

```text
docs/chantiers/<GO_PARENT>/
  00_CADRAGE.md
  01_MASTER_PLAN.md ou 01_PARENT_STATE.md
  REPRISE.md ou section 17_RESUME_POINT dans le plan
  BRANCH_STATE.md si branche dediee

docs/index/inbox/<GO_PARENT>.md
```

## Decision tree

### Modifier seulement le parent si

- nouvelle note locale ;
- TODO local ;
- hypothese locale ;
- preuve locale ;
- point de reprise local ;
- child ajoute sans impact global immediat.

### Modifier l'inbox si

- le resume court du parent change ;
- un child est ajoute ;
- le next local devient utile pour l'agregation future ;
- une decision locale doit etre visible au prochain batch.

### Modifier les index globaux si

- le parent devient officiellement actif dans la liste globale ;
- le parent est ferme ;
- le statut global change ;
- le next GO global change ;
- un batch explicite `INDEX_AGGREGATION` est ouvert.

## Interdits

- Ne pas utiliser `GO_INDEX.md` comme journal de micro-avancement.
- Ne pas utiliser `ACTIVE_STREAMS.md` comme todo local.
- Ne pas utiliser `NEXT_GO_CANDIDATES.md` pour chaque sous-etape.
- Ne pas modifier `REPRISE.md` global si le dossier parent suffit.

## Effet attendu

- Moins de conflits sur les gros index globaux.
- Meilleure isolation par parent.
- Reprise plus fiable par chantier.
- Agregation plus propre par batch.
