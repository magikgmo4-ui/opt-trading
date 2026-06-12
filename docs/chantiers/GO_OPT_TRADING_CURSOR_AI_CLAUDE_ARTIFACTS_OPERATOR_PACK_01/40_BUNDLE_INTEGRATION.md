---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_40_BUNDLE_INTEGRATION
doc_type: chantier/bundle_integration
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/README.md
  - bundles/CURSOR_AI_BUNDLES_REPRISE.md
  - bundles/claude-artifacts/README.md
---

# 40_BUNDLE_INTEGRATION

Integration du pack Claude artifacts avec le workflow Bundles.

## Lien avec `bundles/README.md`

Le pack `bundles/claude-artifacts/` est un nouveau bundle cote cursor-ai, reference dans l'index Bundles.

Ajout a faire dans `bundles/README.md` :

```text
| Claude artifacts operator pack | cursor-ai | ACTIVE | [README](./claude-artifacts/README.md) |
```

## Lien avec `bundles/CURSOR_AI_BUNDLES_REPRISE.md`

Le pack suit la methode de creation de bundle cursor-ai definie dans la fiche de reprise :

1. `README.md` — objectif, invariants, machine owner
2. `PROMPT_TEMPLATES.md` — prompts standard
3. `REPRISE_TEMPLATE.md` — template de reprise
4. `NO_COMMIT_RULES.md` — regles de securite

## Ou placer les prochains packs

| Type de pack | Emplacement recommande |
| --- | --- |
| Pack operateur cursor-ai | `bundles/<pack-name>/` |
| Pack avec prompts reutilisables | `bundles/<pack-name>/prompts/` |
| Chantier documentaire | `docs/chantiers/<GO_ID>/` |
| Fiche inbox | `docs/index/inbox/<GO_ID>.md` |

## Comment eviter les artefacts sensibles

1. Toujours passer par `NO_COMMIT_RULES.md` avant commit.
2. Utiliser des chemins anonymises (`C:\Users\<user>\opt-trading`).
3. Ne jamais capturer de payload reel dans un bundle.
4. Separer les templates (sans donnees reelles) des instances (avec donnees).
5. Les instances avec donnees reelles restent hors repo.

## Bundles et Claude artifacts — relation

| Claude artifacts | Bundles |
| --- | --- |
| Matiere source (IDE, cowork, live artifacts) | Methode de packaging |
| Prompts et templates operateur | Structure de bundle documentaire |
| Regles de securite (no-commit) | Index et conventions |
| Pack operateur cursor-ai | Workflow de livraison |

## RISKS

- À qualifier.
