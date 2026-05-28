---
doc_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_01_SAFE_QUARANTINE_PLAN
doc_type: plan
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
mode: PLAN_ONLY
source_kind: canonical
updated_at: 2026-05-28
---

# 20 — Safe quarantine plan (PLAN_ONLY)

## Hypothese de securite

Les untracked sur db-layer peuvent contenir :
- secrets re-utilisables (credentials OAuth, tokens)
- donnees d'execution (backtests) potentiellement lourdes
- etat tooling (.claude) non deterministe

Donc :
- aucune action d'ecriture n'est autorisee dans ce GO
- toute execution doit etre isolee dans un GO distinct, avec validation humaine explicite

## Strategie cible (execution future)

Objectif : retrouver un repo `/opt/trading` clean (tracked + untracked), sans perdre de donnees utiles.

Plan en 2 phases (deux GOs) :

1. GO_INVENTORY_ONLY (ce GO) : inventaire + classification + decision humaine.
2. GO_EXECUTION_QUARANTINE (futur) : appliquer les actions approuvees.

## Garde-fous (pour le futur GO d'execution)

Preconditions obligatoires :
- Inventaire exporte (tableau Path/Bytes/MTime/Class/ActionCandidate) et revu.
- Espace disque verifie pour duplication (si backup/quarantine).
- Cible quarantine hors repo definie (ex: `/opt/trading/_quarantine/YYYY-MM-DD/` ou volume externe), mais ne pas la creer ici.
- Regle : ne jamais `rm` un secret sans backup explicite et accord.

Commandes interdites (execution) :
- `git clean -fd`, `git reset --hard`, `git checkout -f` (sur db-layer) tant que secrets/artifacts non traites
- `tar`/`zip` sans chemin de sortie hors repo explicite

## Actions candidates par classe

### SENSITIVE_SECRET

- Action par defaut : `BACKUP_OUTSIDE_REPO_ONLY`
- Option possible : migrer vers un store officiel, puis supprimer du repo local (hors-scope ici)

### ARTIFACT_OUTPUT (backtests)

- Action par defaut : `QUARANTINE_OUTSIDE_REPO`
- Variante : conserver dans un emplacement canonical d'artefacts hors git

### TOOLING_STATE (.claude)

- Action par defaut : `QUARANTINE_OUTSIDE_REPO` ou `REMOVE_AFTER_BACKUP`

## Rollback (execution future)

Rollback minimal : restoration depuis le dossier de quarantine.

Exiger dans le futur GO :
- un manifeste `quarantine_manifest.json` (liste fichiers + hash) avant/apres
- un check `git status --porcelain` final = vide

## Sortie attendue

```text
HYGIENE_PLAN_STATUS = READY_FOR_HUMAN_REVIEW
EXECUTION_ALLOWED = NO
REQUIRED_HUMAN_DECISION = approve quarantine targets + approve handling of secrets
SAFE_EXECUTION_GO_CANDIDATE = GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_EXEC_01
PARENT_CLOSE_GATE_STATUS = CLOSEOUT_BLOCKED (unchanged)
```
