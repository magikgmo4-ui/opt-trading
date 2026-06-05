---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01_PRODUCT_USAGE_ATLAS_SPEC
doc_type: specification
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
---

# 02_PRODUCT_USAGE_ATLAS_SPEC - Modele d'entree produit

## Structure canonique

```yaml
product_id:
product_name:
parent_branch:
reason_to_exist:
final_usage_target:
current_state:
usable_now:
usage_mode:
user_guide:
canonical_sources:
remaining_gaps:
next_go:
do_not_use_notes:
```

## Regles par champ

| Champ | Regle |
| --- | --- |
| `product_id` | Identifiant stable, lisible et court. |
| `product_name` | Nom humain de la surface. |
| `parent_branch` | Branche parent canonique quand elle existe. |
| `reason_to_exist` | Raison d'etre dans le setup, pas un resume technique du code. |
| `final_usage_target` | Role final attendu si le produit atteint sa cible. |
| `current_state` | Statut produit borne par la taxonomie, avec overlay de chantier si necessaire. |
| `usable_now` | `yes`, `limited`, `read_only`, `test_only` ou `no`. |
| `usage_mode` | Facon correcte d'utiliser la surface aujourd'hui. |
| `user_guide` | Chemin du guide si un guide est autorise. Sinon `none_yet`. |
| `canonical_sources` | Liste de chemins repo qui prouvent le statut ou le gap. |
| `remaining_gaps` | Gaps restants vers le role final. |
| `next_go` | GO actif, GO propose, ou condition d'ouverture explicite. |
| `do_not_use_notes` | Interdits, limites de securite, ou confusion a eviter. |

## Regles globales

1. Toute entree doit pouvoir etre relue sans consulter une app externe.
2. Toute surface suivie doit dire si elle est utilisable maintenant ou non.
3. Toute surface suivie doit dire ce qu'il ne faut pas supposer.
4. Tout gap doit pointer vers une suite actionnable.
5. Une surface non validee ne recoit pas de guide live.

## Sorties attendues

Le modele doit alimenter :
- `docs/product/PRODUCT_USAGE_ATLAS.md` ;
- `docs/product/PRODUCT_USAGE_MATRIX.md` ;
- `docs/product/FINAL_TARGET_GAPS.md` ;
- `docs/product/guides/*` ;
- `docs/product/PRODUCT_USAGE_GRAPH.mmd`.

## RISKS

- À qualifier.
