# 18_REMEDIATION_SANDBOX_BLOCKER_REPORT

## Objectif

Documenter le blocage persistant de la remediation sandbox Phase 6 AI_TEAM db-layer/OpenClaw remote exec.

Ce document sert de cloture conditionnelle du child avec statut `REVIEW_REQUIRED`, pas de cloture `PASS`.

## Verdict

```text
PHASE_6_CLOSEOUT_REVIEW_REQUIRED
RUNTIME_BLOCKED
SANDBOX_SCHEMA_UNKNOWN
```

## Etat final des gates

| Surface | Status | Evidence |
|:--------|:-------|:---------|
| SSH alias sous `ghost` | VALIDATED | `ssh -G fantome` resout host `192.168.0.191`, user `fantome`, identity `id_ed25519_fantome` |
| SSH alias sous `openclaw` | VALIDATED_NON_CONNECTIVE | `sudo -u openclaw ssh -G fantome` resout host `192.168.0.191`, user `fantome`, `IdentitiesOnly yes` |
| Key material sous `openclaw` | BLOCKED_SECRET_SAFE | `/home/openclaw/.ssh/id_ed25519_fantome` absent ; aucune cle privee copiee |
| Sandbox OpenClaw | BLOCKED_SCHEMA_UNKNOWN | seule valeur trouvee : `sandbox.mode = "all"` ; aucun schema local prouve |
| Runtime OpenClaw | BLOCKED | runtime interdit tant que sandbox et key material restent non resolus |

## Preuve sandbox

Audit `17_REMEDIATION_SANDBOX_MODE_SUPPORT_AUDIT.md` :

- seule valeur locale trouvee : `"all"` ;
- occurrence : `modules/openclaw_config_modulaire/app/agents.json5:20` ;
- aucun fichier de schema ou validation trouve ;
- aucune preuve locale pour des valeurs telles que `none`, `basic`, `network`, `restricted`, `ssh`, ou equivalent ;
- patch sans documentation externe = risqué.

## Raisonnement

La strategie retenue etait :

```text
identity = A
sandbox = B
SSH alias = A
```

Les parties `identity` et `SSH alias` ont progresse, mais `sandbox = B — config OpenClaw` ne peut pas etre appliquee de maniere sure sans connaitre les valeurs supportees de `sandbox.mode`.

Modifier `sandbox.mode = "all"` a l'aveugle violerait les invariants :

- pas d'ouverture globale non prouvee ;
- pas de patch non documente ;
- pas de runtime avant gate ;
- pas de contournement du sandbox.

## Decision

Ne pas appliquer de patch sandbox dans cette Phase 6.

Statut retenu :

```text
SANDBOX_REMEDIATION_BLOCKED_PENDING_EXTERNAL_SCHEMA
```

## Runtime lock final

```text
RUNTIME_REMAINS_BLOCKED
NO_OPENCLAW_JOB_ALLOWED
NO_REMOTE_EXEC_ALLOWED
```

## Actions non realisees volontairement

- Aucun runtime OpenClaw lance.
- Aucune connexion SSH reelle lancee.
- Aucune cle privee copiee.
- Aucun secret ecrit dans le repo.
- Aucun patch `agents.json5` applique sans schema.
- Aucun index global modifie.

## Conditions de reprise future

La Phase 6 pourra etre reprise seulement si une des preuves suivantes est obtenue :

1. documentation officielle ou canonique des valeurs supportees de `sandbox.mode`;
2. code source local validant explicitement les valeurs possibles ;
3. exemple canonique OpenClaw approuve avec reseau/SSH autorise ;
4. decision explicite de creer une nouvelle surface de config sandbox documentee.

## NEXT_GO possible

Creer un nouveau child separe si necessaire :

```text
GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_SANDBOX_SCHEMA_DISCOVERY_01
```

Objectif :

- trouver ou produire la documentation canonique du schema sandbox ;
- definir les valeurs supportees ;
- decider si SSH/network peut etre autorise sans desactiver le sandbox ;
- revenir ensuite a la remediation runtime.

## Closeout status

```text
CHILD_STATUS = REVIEW_REQUIRED
REASON = SANDBOX_SCHEMA_UNKNOWN
RUNTIME = BLOCKED
```
