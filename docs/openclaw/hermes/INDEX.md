---
doc_id: OPENCLAW_HERMES_INDEX
doc_type: hermes_index
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
---

# docs/openclaw/hermes — Index Hermes Bridge (10 docs)

Source : `01_SOURCE_CARTOGRAPHY.md` CLASS 3.

## Table

| Document | Surface | Statut connu |
| --- | --- | --- |
| `docs/hermes/03_bridge_openclaw.md` | Intégration bridge OpenClaw | à vérifier |
| `docs/hermes/GO_HERMES_OPENCLAW_BRIDGE_05*.md` | GO bridge execution | à vérifier |
| `docs/hermes/HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md` | Runbook bridge | à vérifier |
| `docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_*.txt` | Case studies résultats | à vérifier |
| `docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_*.md` | Case studies résultats md | à vérifier |

## Note obsolescence

La cartographie parent signale :

```
Hermes bridge potentiellement obsolète (non maintenu)
```

Vérification requise avant toute réutilisation :

```bash
ls -lt docs/hermes/*openclaw* 2>/dev/null | head -20
git log --oneline -5 -- "docs/hermes/*openclaw*"
```

## Rôle Hermes

Hermes est la couche bridge entre OpenClaw et les surfaces d'exécution externes.
Son état de maintenance conditionne la fiabilité des cas d'usage documentés.
