---
doc_id: OPENCLAW_HERMES_INDEX
doc_type: hermes_index
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
statut_hermes: FROZEN — dernière activité 2026-04-09
---

# docs/openclaw/hermes — Index Hermes Bridge

## Statut global

```
FROZEN / INACTIVE
Dernière activité git : 2026-04-09
Case 01 closée le 2026-04-09 (HERMES_OPENCLAW_BRIDGE_05_CLOSEOUT_2026-04-09.md présent)
Aucun commit hermes/openclaw depuis cette date.
```

> Note : le parent `01_SOURCE_CARTOGRAPHY.md` signalait déjà Hermes comme
> "potentiellement obsolète (non maintenu)". Le scan git confirme : frozen depuis avril 2026.

## Documents (10)

| Document | Rôle | Statut |
| --- | --- | --- |
| `docs/hermes/03_bridge_openclaw.md` | Intégration bridge OpenClaw (spec) | FROZEN |
| `docs/hermes/GO_HERMES_OPENCLAW_BRIDGE_05.md` | GO bridge — définition | FROZEN |
| `docs/hermes/GO_HERMES_OPENCLAW_BRIDGE_05_EXEC_01.md` | GO bridge — exécution | FROZEN |
| `docs/hermes/HERMES_OPENCLAW_BRIDGE_05_CLOSEOUT_2026-04-09.md` | Closeout bridge case 01 | CLOSED 2026-04-09 |
| `docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_PROMPT.txt` | Prompt case 01 | FROZEN |
| `docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_2026-04-09.txt` | Résultat case 01 | FROZEN |
| `docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_TEMPLATE.txt` | Template résultat | FROZEN |
| `docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_V1.txt` | Résultat V1 | FROZEN |
| `docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_V1.md` | Case 01 V1 | FROZEN |
| `docs/hermes/HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md` | Runbook bridge V1 | FROZEN |

## Qu'est-ce que Hermes bridge ?

Hermes était la couche bridge entre OpenClaw et les surfaces d'exécution externes.
Le Bridge Case 01 a été exécuté et closé le 2026-04-09. Aucune suite n'a été lancée.

## Règle d'usage

```
Ne pas réutiliser Hermes bridge pour de nouveaux cas d'usage sans vérification
préalable de la compatibilité avec le runtime OpenClaw actuel.
Le runbook V1 date d'avant la stabilisation du gateway 127.0.0.1:18789.
```

## Vérification

```bash
git log --oneline -- "docs/hermes/*openclaw*" | head -10
ls -lt docs/hermes/*openclaw* | head -15
```
