# 17_RESUME_POINT

## Branche

`go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01`

## Etat ancre

Chantier parent ouvert pour documenter et cadrer l'integration de travail entre :

- tmux comme cockpit operateur
- OpenClaw comme orchestrateur local
- MCP comme bus d'outils
- LONA comme laboratoire de strategie et de backtest
- opt-trading comme systeme canonique de validation et de journalisation

## Fichiers deja ancres

- `00_PARENT_CHECKPOINT.md`
- `README_BUNDLE.md`
- `01_SESSION_DOCUMENTATION_INTEGRALE.md`
- `17_RESUME_POINT.md`

## Etat du bundle

Le bundle IDE local a ete genere dans la session ChatGPT sous forme ZIP. Son injection GitHub a commence, mais n'est pas encore complete.

## Reste a injecter

- notes de recherche
- plan d'execution controlee
- garde-fous securite
- plan tmux
- branch state local
- gap indexation
- prompts GO
- scripts sandbox
- schemas
- module `openclaw_lona_lab`

## Prochain GO

`GO_PUSH_FULL_BUNDLE`

## Invariants

- pas de secret dans Git
- pas de connexion sensible dans cette passe
- pas de promotion automatique
- LONA reste une surface de recherche et validation
- opt-trading reste l'autorite finale
- risk engine reste obligatoire avant toute phase avancee

## Reprise minimale

```bash
cd /opt/trading
git fetch origin
git checkout go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01
git pull --rebase
git status --short --branch
```

Ensuite reprendre par `GO_PUSH_FULL_BUNDLE` pour completer l'injection du bundle.
