# GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_REVIEW_REALIGN_01

## Verdict source

REALIGN.

La branche historique `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` est doc-only mais trop divergente pour merge direct.

## Decision

Transfert selectif depuis la branche historique vers une branche neuve basee sur `origin/sot/mainline`.

## Transfere

- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/`
- `docs/index/inbox/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01.md`

## Non transfere

- `docs/index/BRANCH_STATE.md`
- index globaux obsoletes de la branche historique

## Invariants

- student uniquement
- pas admin-trading
- pas db-layer
- pas cursor-ai
- pas fantome
- pas runtime trading
- pas secrets

## NEXT_GO

Classifier le parent Local Ollama puis choisir un seul child Student/OpenClaw Lab si necessaire.

## RISKS

- À qualifier.
