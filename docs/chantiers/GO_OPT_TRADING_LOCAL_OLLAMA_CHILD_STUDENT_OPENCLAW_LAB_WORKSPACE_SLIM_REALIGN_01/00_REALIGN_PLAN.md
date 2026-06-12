# GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_REALIGN_01

## Verdict source

REALIGN.

Les branches historiques Student/OpenClaw Lab sont doc-only mais trop divergentes pour merge direct.

## Child retenu

`WORKSPACE_SLIM_01`

Raison :
- dernier PASS utile de la chaine
- reduit le prompt / workspace
- enleve les timeouts
- meilleur point de reprise fonctionnel

## Dependances minimales transferees

- `MODEL_PULL_EVAL_04_RETRY`
- `OLLAMA_E2E_SMOKE_01`

## Non transfere

- index globaux historiques
- BRANCH_STATE historique
- runtime
- secrets
- `.env`

## Invariants

- student uniquement
- pas admin-trading
- pas db-layer
- pas cursor-ai
- pas fantome
- pas de merge direct des branches historiques
- un seul child repris

## NEXT_GO

Apres merge :
valider le statut runtime actuel sur student avant toute reprise OpenClaw/Ollama operationnelle.

## RISKS

- À qualifier.
