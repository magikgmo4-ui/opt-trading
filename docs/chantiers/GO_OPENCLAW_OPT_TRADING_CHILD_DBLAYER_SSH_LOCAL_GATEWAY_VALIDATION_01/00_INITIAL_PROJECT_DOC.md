---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01
parent_go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_CLI_LOCAL_DRYRUN_INVOCATION_01
machine: fantome
status: blocked
lifecycle_stage: ssh_gate_validation
topic_keys:
  - openclaw
  - db-layer
  - ssh
  - gateway
  - builder
source_kind: canonical
updated_at: 2026-05-14
---

# GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01

## 1_MASTER_TARGET

Utiliser `fantome` comme poste operateur et SSH comme transport controle vers `db-layer`, puis verifier localement sur `db-layer` : identite machine, presence du repo `opt-trading`, etat git, presence du CLI `openclaw`, etat Gateway V2, etat orchestrateur, puis un dry-run builder borne.

## 2_STATE (entree)

```text
base = origin/sot/mainline @ fb890c4 (>= 67521a5)
fantome = poste operateur
db-layer = cible runtime OpenClaw
CLI openclaw sur fantome = ABSENT
remote/SSH = autorisable uniquement via GO dedie
```

## 3_CADRE

```text
- SSH utilise uniquement comme transport controle vers db-layer
- aucune commande destructive
- aucun sudo
- aucune installation sans approval humain explicite
- aucun secret
- aucun live trading
- aucun write libre
```

## 4_CONSTAT INITIAL

Le repo documente `db-layer` comme cible canonique OpenClaw runtime, avec IP documentee `192.168.0.100` et utilisateur historique `ghost`.

Le hostname `db-layer` n'est pas resolu sur `fantome` au moment du GO. Le transport a donc ete tente directement vers `ghost@192.168.0.100` avec verification de cle hote stricte via un fichier temporaire `known_hosts` dans `/tmp/opencode/`.

## 5_RESULTAT

```text
Reachability SSH = PARTIAL_PASS
Host key scan = PASS
Authentication = BLOCKED (publickey)

Consequence:
- impossible d'entrer dans une session shell db-layer
- impossible de verifier repo/git/openclaw/gateway/orchestrateur
- impossible d'executer un dry-run builder local db-layer
```

## 6_NEXT

Pour reprendre ce GO, il faut au minimum :

1. un principal SSH valide pour `db-layer` depuis `fantome` ;
2. une cle publique autorisee cote `db-layer` ;
3. idealement un alias SSH canonique `db-layer` present sur `fantome`.
