# 30_REFINED_MARKDOWN_RENDER_MODEL

## 1_MASTER_TARGET

Definir le modele de rendu Markdown v1 attendu pour le refinement de lisibilite.

## WHY

Le prochain artefact doit pouvoir etre genere depuis le JSON valide sans changer la nature du rendu. Ce document donne le modele de sortie attendu avant production d'un artefact v1.

## 7_CANONICAL_STATE

Source unique :

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01/artifacts/why-runtime-graph-export.real.v0.json
```

Sortie cible future :

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_READABILITY_REFINEMENT_01/artifacts/why-runtime-graph.local-render.v1.md
```

## 8_MARKDOWN_MODEL

Modele v1 recommande :

~~~markdown
# WHY Runtime Graph - Local Render v1

## Source Lock

- JSON source: `docs/chantiers/.../why-runtime-graph-export.real.v0.json`
- Render type: Markdown static refinement
- Data changes: none
- Dashboard: disabled
- Runtime live: disabled

## Graph Summary

- Nodes: 3
- Edges: 3
- Scope: `localcms_tmux_daily_journal_minimal`

## Readable Graph

```mermaid
flowchart LR
  DJ["Daily Journal\nrun context source"]
  LCMS["LocalCMS\nread-only view"]
  TMUX["TMUX\nruntime session spine"]

  DJ -->|"anchors run"| TMUX
  DJ -->|"references view"| LCMS
  LCMS -->|"reads session"| TMUX
```

## Edge Legend

| Short label | JSON relation |
| --- | --- |
| `anchors run` | `run_id_references_tmux_session` |
| `references view` | `journal_reference_points_to_localcms_read_only_view` |
| `reads session` | `localcms_view_reads_or_summarizes_tmux_session` |
~~~

## 9_REQUIRED_TABLES

Le rendu v1 doit aussi inclure :

- `Node Legend` avec type et status JSON ;
- `Node Provenance` par node ;
- `Edge Provenance` par edge ;
- `Readability Gaps Addressed` ;
- `Next Surfaces` avec dashboard toujours bloque ;
- `Limits`.

## 10_NON_GOALS

Le rendu v1 ne doit pas :

- creer un HTML ;
- ajouter un SVG ;
- changer le JSON ;
- ajouter des nodes ou edges ;
- lancer un runtime ;
- devenir une surface LocalCMS.

## 12_INVARIANTS

- Les labels courts ne remplacent pas les relations JSON.
- La provenance ne doit pas etre masquee par la lisibilite.
- Le modele reste reviewable en diff texte.

## 17_RESUME_POINT

Le modele v1 donne une sortie plus lisible tout en conservant strictement le graph v0.
