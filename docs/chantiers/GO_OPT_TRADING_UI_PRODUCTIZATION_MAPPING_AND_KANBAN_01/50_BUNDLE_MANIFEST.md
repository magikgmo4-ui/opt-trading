# 50_BUNDLE_MANIFEST

Generated: 2026-05-19

## Contenu du bundle GO_OPT_TRADING_UI_PRODUCTIZATION_MAPPING_AND_KANBAN_01

| Fichier | Rôle | Présent |
|---------|------|---------|
| `00_INITIAL_PROJECT_DOC.md` | Cadrage canonique, contraintes, découvertes | ✓ |
| `10_UI_CURRENT_MAPPING.md` | Carte complète des surfaces UI et endpoints | ✓ |
| `20_GAP_ANALYSIS.md` | Gaps produit par surface, priorités, critères | ✓ |
| `30_PRODUCTIZATION_KANBAN.md` | Kanban 10 GOs + définitions de DONE | ✓ |
| `40_VISUAL_AND_HUMAN_VALIDATION_PLAN.md` | Plan screenshots + checklists humaines | ✓ |
| `50_BUNDLE_MANIFEST.md` | Ce fichier | ✓ |

## Ce qui n'est PAS dans ce bundle

| Élément | Raison d'exclusion |
|---------|-------------------|
| `secrets/` | Invariant — jamais dans Git |
| Fichiers `.env` | Invariant — jamais dans Git |
| Logs runtime (`tmp/`) | Données ephémères non versionnées |
| Screenshots | Non générés à ce stade (GO suivant) |
| Checklists remplies | Validation humaine future |

## État baseline capturé

| Métrique | Valeur |
|---------|--------|
| Date audit | 2026-05-19 |
| Branche | `sot/mainline` @ `ea3d447d` |
| Tests | 172/172 PASS |
| Endpoints Desk Pro mappés | 10 |
| Endpoints localcms mappés | 16 |
| Gaps identifiés | 13 (7 Desk Pro, 3 localcms, 6 transverses) |
| Gaps P0 | 7 |
| Gaps P1 | 6 |
| GOs planifiés | 10 |

## Prochaine étape

```
GO_OPT_TRADING_DESKPRO_UI_PRODUCT_SHELL_REVIEW_01
```

Objectif : ouvrir `/desk/ui` dans le navigateur, capturer l'état actuel,
annoter les cards, identifier les gaps visuels concrets avant toute modification.
