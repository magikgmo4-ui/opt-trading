# WHY Runtime Graph Local Render v0 Report

## Verdict

PASS / LOCAL_BOUNDED_MARKDOWN_RENDER

## Source

- JSON source: `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01/artifacts/why-runtime-graph-export.real.v0.json`
- Source graph: `why_runtime_graph_minimal_v1`
- Source export: `why-runtime-graph-export.real.v0`
- Source GO: `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01`

## Render Artifact

- `why-runtime-graph.local-render.v0.md`

## Render Content

- Nodes rendered: 3
- Edges rendered: 3
- Render format: Markdown with static Mermaid graph block and review tables
- Dashboard: not created
- Runtime live view: not created
- Runtime mutation: not performed

## Checks

- Source JSON exists.
- Source JSON parseable with `python -m json.tool`.
- Render output is bounded to the GO `artifacts/` folder.
- Render output uses only `nodes[]`, `edges[]` and provenance already present in the JSON source.
- No CI, validator or global index file modified.

## Limits

- The Mermaid block is a static Markdown representation for local review.
- No runtime session, LocalCMS view, log, snapshot or external source was queried.
- No extra node, edge, overlay or dashboard control was inferred.

## RISKS

- À qualifier.
