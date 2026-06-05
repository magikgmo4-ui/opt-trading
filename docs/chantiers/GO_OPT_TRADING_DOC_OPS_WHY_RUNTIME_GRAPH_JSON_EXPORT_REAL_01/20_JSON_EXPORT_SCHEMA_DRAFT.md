# 20_JSON_EXPORT_SCHEMA_DRAFT

## 1_MASTER_TARGET

Definir le schema JSON minimal du premier export reel du WHY runtime graph.

## WHY

Le schema doit etre assez petit pour etre auditable rapidement, mais assez riche pour prouver que le passage `mapping documentaire -> export JSON reel` fonctionne deja sur la spine centrale.

## 7_CANONICAL_STATE

Structure minimale retenue :

```json
{
  "graph_id": "why_runtime_graph_minimal_v1",
  "generated_at": "ISO-8601",
  "scope": "localcms_tmux_daily_journal_minimal",
  "sources": [
    {
      "doc_path": "docs/chantiers/...",
      "doc_role": "source_surface|mapping|inventory"
    }
  ],
  "nodes": [
    {
      "id": "surface:localcms",
      "type": "runtime_surface",
      "label": "LocalCMS",
      "provenance": ["docs/chantiers/..."]
    }
  ],
  "edges": [
    {
      "id": "edge:run_id_to_tmux_session",
      "type": "run_link",
      "from": "surface:daily_journal",
      "to": "surface:tmux",
      "provenance": ["docs/chantiers/..."]
    }
  ],
  "export_notes": [
    "read_only",
    "no_render",
    "bounded_scope"
  ]
}
```

## 8_FIELD_RULES

| Champ | Obligation | Regle minimale |
| --- | --- | --- |
| `graph_id` | REQUIRED | identifiant stable du premier export borne |
| `generated_at` | REQUIRED | timestamp de generation de l'artefact |
| `scope` | REQUIRED | doit expliciter le perimetre restreint |
| `sources` | REQUIRED | provenance documentaire de l'export |
| `nodes` | REQUIRED | uniquement les surfaces centrales et leur contexte minimal |
| `edges` | REQUIRED | uniquement les relations documentees en amont |
| `export_notes` | REQUIRED | rappelle les invariants de lecture seule |

## 9_EXCLUDED_FIELDS

Champs exclus du premier export :

- `warnings_overlay` ;
- `security_overlay` ;
- `governance_snapshot_full` ;
- `runtime_state_live` ;
- `graph_render_hints`.

## 12_INVARIANTS

- Le schema ne doit pas supposer de moteur de rendu.
- Le schema ne doit pas supposer de traversal autonome.
- Le schema doit rester versionnable en diff texte simple.
- La provenance documentaire doit etre visible sans resolution externe.

## 17_RESUME_POINT

Le premier schema JSON reel est volontairement reduit a `sources`, `nodes`, `edges` et notes d'export, sans overlays ni donnees live.

## RISKS

- À qualifier.
