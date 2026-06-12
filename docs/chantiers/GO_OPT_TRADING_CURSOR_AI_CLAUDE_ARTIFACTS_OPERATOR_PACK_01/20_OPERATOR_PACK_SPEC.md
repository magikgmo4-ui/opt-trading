---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_20_OPERATOR_PACK_SPEC
doc_type: chantier/spec
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
machine: cursor-ai
status: active
links:
  - bundles/claude-artifacts/README.md
  - bundles/ACTIVE_WORKFLOW.md
  - bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md
---

# 20_OPERATOR_PACK_SPEC

## Finalite

Le pack operateur Claude artifacts sert a fournir a `cursor-ai` un socle stable pour :

- reprendre un GO doc-only ;
- appliquer les prompts operateur standards ;
- produire un handoff lisible ;
- verifier les limites no-runtime / no-secret avant commit, push et PR.

## Perimetre en scope

| Surface | Role |
| --- | --- |
| `bundles/claude-artifacts/` | Artefacts operateur reutilisables |
| `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01/` | Dossier chantier canonique |
| `docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01.md` | Entree courte de reprise |

## Hors scope

- Toute modification runtime hors `docs/` et `bundles/`
- Toute ouverture `admin-trading`
- Toute reouverture TradingView MCP deja fermee / mergee
- Toute action sur `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`
- Toute donnee live, secret, `.env`, token, payload reel

## Artefacts attendus cote bundle

| Fichier | Obligation |
| --- | --- |
| `README.md` | Oui |
| `PROMPT_TEMPLATES.md` | Oui |
| `REPRISE_TEMPLATE.md` | Oui |
| `NO_COMMIT_RULES.md` | Oui |
| `CHECKLIST_EXECUTION.md` | Oui |
| `bundle_meta/manifest.json` | Oui |

## Artefacts attendus cote chantier

| Fichier | Obligation |
| --- | --- |
| `00_GO_OPEN.md` | Oui |
| `10_SOURCE_STATE.md` | Oui |
| `20_OPERATOR_PACK_SPEC.md` | Oui |
| `30_ARTIFACTS_INDEX.md` | Oui |
| `40_USAGE_WORKFLOW.md` | Oui |
| `90_CLOSEOUT.md` | Oui |

## Criteres de PASS

- Le diff reste doc-only.
- Le dossier expose une ouverture, un etat source, une spec, un index d'artefacts, un workflow et un closeout.
- Le bundle `claude-artifacts` pointe vers ses 6 artefacts reels.
- Les limites `no runtime`, `no admin-trading`, `no secrets`, `no DOC_OPS blocked` restent explicites.
- Les traces legacy restent lisibles sans casser les references deja mergees.

## RISKS

- À qualifier.
