---
doc_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01_ROADMAP_AND_NEXT_GO
doc_type: roadmap
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 40_ROADMAP_AND_NEXT_GO

## Roadmap parent

### GO 1 — audit existant

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01
```

But : cartographier ce qui existe vraiment avant toute extension.

Livrables :

```text
10_EXISTING_DATA_CENTER_SURFACES.md
20_EXISTING_DESKPRO_CONSUMERS.md
30_EXISTING_PRODUCERS_AND_CONTRACTS.md
40_EXISTING_VIEWS_AND_PATHS.md
50_PRELIMINARY_GAPS.md
```

### GO 2 — inventaire canonique

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01
```

But : transformer P0-P21 en registry exploitable.

### GO 3 — mapping inventaire -> existant

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01
```

But : produire `PRO_DESK_DATA_GAP_MATRIX.md`.

### GO 4 — scoring source

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01
```

But : creer la methode et les schemas de scoring source.

### GO 5 — best-value resolver

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_BEST_VALUE_RESOLVER_01
```

But : definir et tester la selection de la meilleure valeur disponible.

### GO 6 — DeskPro consumption map

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_PRO_DATA_CONSUMPTION_MAP_01
```

But : documenter les donnees que DeskPro doit consommer depuis les views Data Center.

## NEXT_GO immediat

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01
```

## Close gate parent

Le parent ne peut pas etre ferme tant que :

- audit existant produit ;
- inventaire canonique P0-P21 produit ;
- gap matrix produite ;
- scoring source specifie ;
- resolver policy specifiee ;
- consumption map DeskPro produite.
